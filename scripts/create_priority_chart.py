"""
Create a better district priority visualization with inverted priority scale
Since many districts have IFI near 0, we'll show them as HIGH PRIORITY (reversed scale)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("🔧 CREATING IMPROVED DISTRICT PRIORITY CHART")
print("=" * 70)

# Load data
BASE_PATH = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

# Load all datasets
enrol_files = list((BASE_PATH / 'data' / 'raw' / 'Enrolment').glob('*.csv'))
enrolment_df = pd.concat([pd.read_csv(f, on_bad_lines='skip') for f in enrol_files], ignore_index=True)
enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']

demo_files = list((BASE_PATH / 'data' / 'raw' / 'Demographic').glob('*.csv'))
demographic_df = pd.concat([pd.read_csv(f, on_bad_lines='skip') for f in demo_files], ignore_index=True)
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']

bio_files = list((BASE_PATH / 'data' / 'raw' / 'Biometric').glob('*.csv'))
biometric_df = pd.concat([pd.read_csv(f, on_bad_lines='skip') for f in bio_files], ignore_index=True)
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

print(f"✓ Loaded data")

# Calculate district-level metrics
enrol_dist = enrolment_df.groupby(['state', 'district'])['total_enrolments'].sum().reset_index()
demo_dist = demographic_df.groupby(['state', 'district'])['total_demo_updates'].sum().reset_index()
bio_dist = biometric_df.groupby(['state', 'district'])['total_bio_updates'].sum().reset_index()

district_df = enrol_dist.merge(demo_dist, on=['state', 'district'], how='left')
district_df = district_df.merge(bio_dist, on=['state', 'district'], how='left').fillna(0)
district_df['total_updates'] = district_df['total_demo_updates'] + district_df['total_bio_updates']
district_df['ifi'] = district_df['total_updates'] / district_df['total_enrolments'].replace(0, np.nan)
district_df = district_df.dropna()

# Filter for significant districts (1000+ enrolments)
district_df = district_df[district_df['total_enrolments'] >= 1000]
print(f"✓ {len(district_df)} significant districts (1000+ enrolments)")

# Sort by IFI (lowest first = highest priority)
district_df = district_df.sort_values('ifi', ascending=True)

# Calculate Priority Score (inverse of IFI for visualization)
max_ifi = district_df['ifi'].quantile(0.95)  # Use 95th percentile to handle outliers
district_df['priority_score'] = 100 * (1 - (district_df['ifi'] / max_ifi).clip(upper=1))

# Top 20
top20 = district_df.head(20).copy()

# Create comprehensive visualization
fig, ax = plt.subplots(figsize=(14, 12))

# Priority Score bars (100 = Most Urgent, 0 = Low Priority)
colors = ['#dc3545' if p > 90 else ('#ff6b35' if p > 70 else ('#ffc107' if p > 50 else '#28a745')) 
          for p in top20['priority_score']]

bars = ax.barh(range(20), top20['priority_score'], color=colors, edgecolor='white', height=0.7)

# Labels
labels = [f"{row['district']}, {row['state'][:12]}" for _, row in top20.iterrows()]
ax.set_yticks(range(20))
ax.set_yticklabels([f"{i+1}. {label[:35]}" for i, label in enumerate(labels)], fontsize=10)

# Add annotations on bars
for i, (idx, row) in enumerate(top20.iterrows()):
    ax.text(row['priority_score'] + 2, i, 
            f"IFI={row['ifi']:.1f} | {row['total_enrolments']:,.0f} citizens",
            va='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Priority Score (100 = Most Urgent)', fontsize=12, fontweight='bold')
ax.set_xlim(0, 120)
ax.invert_yaxis()

# Title
ax.set_title('🚨 TOP 20 PRIORITY DISTRICTS FOR AADHAAR DATA REFRESH\n(High Score = Highest Staleness Risk = Immediate Action Needed)', 
             fontsize=14, fontweight='bold')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#dc3545', label='CRITICAL (90-100)'),
    Patch(facecolor='#ff6b35', label='HIGH (70-90)'),
    Patch(facecolor='#ffc107', label='MEDIUM (50-70)'),
    Patch(facecolor='#28a745', label='LOW (<50)')
]
ax.legend(handles=legend_elements, loc='lower right', title='Priority Level')

plt.tight_layout()
plt.savefig(BASE_PATH / 'visualizations' / 'district_priority.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"\n✅ Saved: district_priority.png")
print(f"\nTop 5 Districts Needing Immediate Attention:")
for i, (_, row) in enumerate(top20.head(5).iterrows()):
    print(f"  {i+1}. {row['district']}, {row['state']} - {row['total_enrolments']:,.0f} citizens affected")
