"""
Fix district priority visualization with better data and scaling
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("🔧 FIXING DISTRICT PRIORITY VISUALIZATION")
print("=" * 70)

# Load data
BASE_PATH = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

# Load all datasets
enrol_path = BASE_PATH / 'data' / 'raw' / 'Enrolment'
enrol_files = list(enrol_path.glob('*.csv'))
enrol_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in enrol_files]
enrolment_df = pd.concat(enrol_dfs, ignore_index=True)
enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']

demo_path = BASE_PATH / 'data' / 'raw' / 'Demographic'
demo_files = list(demo_path.glob('*.csv'))
demo_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in demo_files]
demographic_df = pd.concat(demo_dfs, ignore_index=True)
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']

bio_path = BASE_PATH / 'data' / 'raw' / 'Biometric'
bio_files = list(bio_path.glob('*.csv'))
bio_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in bio_files]
biometric_df = pd.concat(bio_dfs, ignore_index=True)
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

print(f"✓ Loaded data")

# Calculate district-level IFI
enrol_dist = enrolment_df.groupby(['state', 'district']).agg({
    'total_enrolments': 'sum',
    'age_5_17': 'sum'
}).reset_index()

demo_dist = demographic_df.groupby(['state', 'district'])['total_demo_updates'].sum().reset_index()
bio_dist = biometric_df.groupby(['state', 'district'])['total_bio_updates'].sum().reset_index()

district_df = enrol_dist.merge(demo_dist, on=['state', 'district'], how='left')
district_df = district_df.merge(bio_dist, on=['state', 'district'], how='left').fillna(0)

district_df['total_updates'] = district_df['total_demo_updates'] + district_df['total_bio_updates']
district_df['ifi'] = district_df['total_updates'] / district_df['total_enrolments'].replace(0, np.nan)
district_df = district_df.dropna(subset=['ifi'])

# Filter for meaningful districts (minimum 500 enrolments for significance)
district_df = district_df[district_df['total_enrolments'] >= 500]
print(f"✓ {len(district_df)} districts with 500+ enrolments")

# Sort by IFI (lowest = highest priority)
district_df = district_df.sort_values('ifi', ascending=True)

# Top 20 priority districts
top20 = district_df.head(20).copy()
top20['rank'] = range(1, 21)
top20['label'] = top20.apply(lambda x: f"{x['district']}, {x['state'][:12]}", axis=1)

print(f"\n📊 Top 20 Priority Districts:")
for _, row in top20.iterrows():
    print(f"   {row['rank']:2}. {row['label'][:30]:30} IFI={row['ifi']:.2f}, Enrol={row['total_enrolments']:,.0f}")

# Visualization 1: Horizontal bar with IFI values
fig, ax = plt.subplots(figsize=(14, 12))

# Color by IFI using log scale for better visibility
colors = plt.cm.RdYlGn(top20['ifi'] / top20['ifi'].max())

# Plot horizontal bars
bars = ax.barh(range(20), top20['ifi'], color=colors, edgecolor='white', linewidth=0.5)

# Add IFI value labels at end of bars
for i, (idx, row) in enumerate(top20.iterrows()):
    ax.text(row['ifi'] + 0.5, i, f"IFI: {row['ifi']:.1f}", va='center', fontsize=9, fontweight='bold')

# Set y-labels
ax.set_yticks(range(20))
ax.set_yticklabels([f"{i+1}. {label}" for i, label in enumerate(top20['label'])], fontsize=10)

ax.set_xlabel('Identity Freshness Index (IFI)', fontsize=12, fontweight='bold')
ax.set_title('Top 20 Priority Districts for Aadhaar Data Refresh\n(Lowest IFI = Highest Staleness Risk)', 
             fontsize=14, fontweight='bold')

# Add reference lines
ax.axvline(x=top20['ifi'].median(), color='orange', linestyle='--', linewidth=2, 
           label=f'Median: {top20["ifi"].median():.1f}')
ax.legend(loc='lower right')

ax.invert_yaxis()  # Highest priority at top
plt.tight_layout()
plt.savefig(BASE_PATH / 'visualizations' / 'district_priority.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"\n✓ Saved: district_priority.png")

# Visualization 2: Combined view with enrolment volume
fig, axes = plt.subplots(1, 2, figsize=(16, 10))

# Left: IFI bars
ax1 = axes[0]
colors = ['#dc3545' if ifi < 5 else ('#ffc107' if ifi < 15 else '#28a745') for ifi in top20['ifi']]
ax1.barh(range(20), top20['ifi'], color=colors, edgecolor='white')
for i, (idx, row) in enumerate(top20.iterrows()):
    ax1.text(row['ifi'] + 0.3, i, f"{row['ifi']:.1f}", va='center', fontsize=9)
ax1.set_yticks(range(20))
ax1.set_yticklabels([f"{i+1}. {row['district'][:15]}" for i, (_, row) in enumerate(top20.iterrows())], fontsize=9)
ax1.set_xlabel('IFI Score', fontweight='bold')
ax1.set_title('Lowest IFI Districts', fontweight='bold')
ax1.invert_yaxis()

# Right: Enrolment volume (shows scale of problem)
ax2 = axes[1]
ax2.barh(range(20), top20['total_enrolments'], color='#1a73e8', alpha=0.7, edgecolor='white')
for i, (idx, row) in enumerate(top20.iterrows()):
    ax2.text(row['total_enrolments'] + 100, i, f"{row['total_enrolments']:,.0f}", va='center', fontsize=9)
ax2.set_yticks(range(20))
ax2.set_yticklabels([row['state'][:12] for _, row in top20.iterrows()], fontsize=9)
ax2.set_xlabel('Total Enrolments', fontweight='bold')
ax2.set_title('Affected Population', fontweight='bold')
ax2.invert_yaxis()

fig.suptitle('District Priority Matrix: Where to Focus Aadhaar Data Refresh', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(BASE_PATH / 'visualizations' / 'district_priority_matrix.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"✓ Saved: district_priority_matrix.png")

print("\n" + "=" * 70)
print("✅ District visualizations fixed!")
