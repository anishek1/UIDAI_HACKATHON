"""
Update the notebook to use the improved District Priority Matrix visualization code
"""
import json
from pathlib import Path

notebook_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb')

# Load existing notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The code for the improved visualization (from fix_district_viz.py)
# We need to adapt it to run inside the notebook environment where variables like district_df exist
new_source_code = [
    "# ============================================\n",
    "# DISTRICT-LEVEL PRIORITY MATRIX\n",
    "# ============================================\n",
    "\n",
    "print(\"=\"*70)\n",
    "print(\"🎯 DISTRICT-LEVEL PRIORITY ANALYSIS\")\n",
    "print(\"=\"*70)\n",
    "\n",
    "# Calculate district-level metrics\n",
    "enrol_dist = enrolment_df.groupby(['state', 'district'])['total_enrolments'].sum().reset_index()\n",
    "demo_dist = demographic_df.groupby(['state', 'district'])['total_demo_updates'].sum().reset_index()\n",
    "bio_dist = biometric_df.groupby(['state', 'district'])['total_bio_updates'].sum().reset_index()\n",
    "\n",
    "district_df = enrol_dist.merge(demo_dist, on=['state', 'district'], how='left')\n",
    "district_df = district_df.merge(bio_dist, on=['state', 'district'], how='left').fillna(0)\n",
    "\n",
    "district_df['total_updates'] = district_df['total_demo_updates'] + district_df['total_bio_updates']\n",
    "district_df['ifi'] = district_df['total_updates'] / district_df['total_enrolments'].replace(0, np.nan)\n",
    "district_df = district_df.dropna()\n",
    "\n",
    "# Filter for significant districts (1000+ enrolments)\n",
    "district_df = district_df[district_df['total_enrolments'] >= 1000]\n",
    "\n",
    "# Sort by IFI (lowest first = highest priority)\n",
    "district_df = district_df.sort_values('ifi', ascending=True)\n",
    "\n",
    "# Calculate Priority Score (inverse of IFI for visualization)\n",
    "max_ifi = district_df['ifi'].quantile(0.95)  # Use 95th percentile to handle outliers\n",
    "district_df['priority_score'] = 100 * (1 - (district_df['ifi'] / max_ifi).clip(upper=1))\n",
    "\n",
    "# Top 20 Priority Districts\n",
    "top20 = district_df.head(20).copy()\n",
    "\n",
    "print(f\"\\n🚨 TOP 20 DISTRICTS REQUIRING IMMEDIATE INTERVENTION:\")\n",
    "display(top20[['state', 'district', 'ifi', 'total_enrolments', 'priority_score']].head(10))\n",
    "\n",
    "# Visualization: Combined Priority Matrix\n",
    "fig, axes = plt.subplots(1, 2, figsize=(16, 10))\n",
    "\n",
    "# Left: Priority Score (Inverted IFI)\n",
    "ax1 = axes[0]\n",
    "colors = ['#dc3545' if p > 90 else ('#ff6b35' if p > 70 else ('#ffc107' if p > 50 else '#28a745')) \n",
    "          for p in top20['priority_score']]\n",
    "\n",
    "ax1.barh(range(20), top20['priority_score'], color=colors, edgecolor='white')\n",
    "\n",
    "# Add labels\n",
    "for i, (idx, row) in enumerate(top20.iterrows()):\n",
    "    ax1.text(row['priority_score'] + 1, i, f\"IFI: {row['ifi']:.2f}\", va='center', fontsize=9, fontweight='bold')\n",
    "\n",
    "ax1.set_yticks(range(20))\n",
    "ax1.set_yticklabels([f\"{i+1}. {row['district'][:15]}, {row['state'][:10]}\" for i, (_, row) in enumerate(top20.iterrows())], fontsize=10)\n",
    "ax1.set_xlabel('Staleness Risk Score (100 = Critical)', fontweight='bold')\n",
    "ax1.set_title('Risk Level (Low IFI)', fontweight='bold', color='#dc3545')\n",
    "ax1.set_xlim(0, 115)\n",
    "ax1.invert_yaxis()\n",
    "\n",
    "# Right: Affected Population (Enrolment Volume)\n",
    "ax2 = axes[1]\n",
    "ax2.barh(range(20), top20['total_enrolments'], color='#1a73e8', alpha=0.7, edgecolor='white')\n",
    "\n",
    "for i, (idx, row) in enumerate(top20.iterrows()):\n",
    "    ax2.text(row['total_enrolments'] + 100, i, f\"{row['total_enrolments']:,.0f}\", va='center', fontsize=9)\n",
    "\n",
    "ax2.set_yticks(range(20))\n",
    "ax2.set_yticklabels([]) # Hide labels on second chart\n",
    "ax2.set_xlabel('Total Enrolments', fontweight='bold')\n",
    "ax2.set_title('Affected Population Scale', fontweight='bold', color='#1a73e8')\n",
    "ax2.invert_yaxis()\n",
    "\n",
    "plt.suptitle('District Priority Matrix: Where to Focus Aadhaar Data Refresh', fontsize=16, fontweight='bold', y=0.95)\n",
    "plt.tight_layout()\n",
    "plt.savefig('../visualizations/district_priority.png', dpi=300, bbox_inches='tight', facecolor='white')\n",
    "plt.show()\n",
    "\n",
    "print(\"\\n✅ District Priority Matrix chart saved.\")"
]

# Find and replace the old district priority cell
found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'DISTRICT-LEVEL PRIORITY ANALYSIS' in source:
            cell['source'] = new_source_code
            found = True
            print("✓ Updated notebook code with improved visualization")
            break

if not found:
    print("⚠️ Could not find target cell in notebook")

# Save updated notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)
