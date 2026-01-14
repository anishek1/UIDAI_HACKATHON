"""
UIDAI Visualization Generation Script
======================================
Generates all 8 decision-driving visualizations from Phase 5 specs.
"""

import sys
sys.path.insert(0, r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

# Color palette
COLORS = {
    'critical': '#dc3545',
    'at_risk': '#ffc107', 
    'healthy': '#28a745',
    'optimal': '#007bff',
    'primary': '#1a73e8',
    'secondary': '#ea4335'
}

print("="*70)
print("GENERATING VISUALIZATIONS")
print("="*70)

# Load cleaned data
metrics_df = pd.read_csv(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\processed\state_metrics_clean.csv')
print(f"Loaded {len(metrics_df)} states")

# Filter out invalid entries
metrics_df = metrics_df[~metrics_df['state'].str.contains('100000', na=False)]
metrics_df = metrics_df.dropna(subset=['state'])

# Calculate national averages
national_ifi = metrics_df['ifi'].mean()
national_taes = metrics_df['taes'].mean()

output_dir = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\visualizations')

# ============================================
# CHART 1: IFI State Rankings (Lollipop)
# ============================================
print("\n[1/8] Generating IFI Rankings Chart...")

fig, ax = plt.subplots(figsize=(14, 10))

plot_data = metrics_df.nsmallest(25, 'ifi').sort_values('ifi', ascending=True)

# Assign colors based on IFI thresholds
colors = []
for ifi in plot_data['ifi']:
    if ifi < 5:
        colors.append(COLORS['critical'])
    elif ifi < 15:
        colors.append(COLORS['at_risk'])
    elif ifi < 30:
        colors.append(COLORS['healthy'])
    else:
        colors.append(COLORS['optimal'])

# Create lollipop chart
ax.hlines(y=plot_data['state'], xmin=0, xmax=plot_data['ifi'], color=colors, alpha=0.7, linewidth=3)
ax.scatter(plot_data['ifi'], plot_data['state'], color=colors, s=100, zorder=5)

# Add value labels
for i, (ifi, state) in enumerate(zip(plot_data['ifi'], plot_data['state'])):
    ax.text(ifi + 1, i, f'{ifi:.1f}', va='center', fontsize=9)

ax.axvline(x=national_ifi, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'National Avg: {national_ifi:.1f}')
ax.set_xlabel('Identity Freshness Index (IFI)', fontweight='bold', fontsize=12)
ax.set_ylabel('State', fontweight='bold', fontsize=12)
ax.set_title('Which States Need Identity Refresh Campaigns?', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right')
ax.set_xlim(0, plot_data['ifi'].max() * 1.15)

plt.tight_layout()
plt.savefig(output_dir / 'chart1_ifi_rankings.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart1_ifi_rankings.png")

# ============================================
# CHART 2: CLCR Child Lifecycle Gap
# ============================================
print("[2/8] Generating CLCR Gap Chart...")

fig, ax = plt.subplots(figsize=(14, 10))

clcr_data = metrics_df.nsmallest(25, 'clcr').sort_values('clcr', ascending=True)

# Cap CLCR for visualization
clcr_display = clcr_data['clcr'].clip(upper=10)

colors = [COLORS['critical'] if c < 1 else COLORS['healthy'] for c in clcr_data['clcr']]

bars = ax.barh(clcr_data['state'], clcr_display, color=colors, edgecolor='white', linewidth=0.5)

ax.axvline(x=1.0, color='black', linestyle='--', linewidth=2, label='Target (1.0)')

ax.set_xlabel('Child Lifecycle Capture Rate (CLCR)', fontweight='bold', fontsize=12)
ax.set_ylabel('State', fontweight='bold', fontsize=12)
ax.set_title('Are Children Getting Mandatory Biometric Updates?', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig(output_dir / 'chart2_clcr_gap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart2_clcr_gap.png")

# ============================================
# CHART 3: TAES Weekend Access
# ============================================
print("[3/8] Generating TAES Weekend Access Chart...")

fig, ax = plt.subplots(figsize=(14, 10))

taes_data = metrics_df.nsmallest(25, 'taes').sort_values('taes', ascending=True)

colors = [COLORS['critical'] if t < 0.5 else (COLORS['at_risk'] if t < 0.7 else COLORS['healthy']) 
          for t in taes_data['taes']]

bars = ax.barh(taes_data['state'], taes_data['taes'], color=colors, edgecolor='white', linewidth=0.5)

ax.axvline(x=0.70, color='orange', linestyle='--', linewidth=2, label='Acceptable (0.70)')
ax.axvline(x=1.0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Equal Access (1.0)')

ax.set_xlabel('Temporal Access Equity Score (TAES)', fontweight='bold', fontsize=12)
ax.set_ylabel('State', fontweight='bold', fontsize=12)
ax.set_title('Which States Penalize Working Citizens with Weekend Gaps?', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right')
ax.set_xlim(0, 1.2)

plt.tight_layout()
plt.savefig(output_dir / 'chart3_taes_weekend.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart3_taes_weekend.png")

# ============================================
# CHART 4: Composite Score Rankings
# ============================================
print("[4/8] Generating Composite Rankings Chart...")

fig, ax = plt.subplots(figsize=(14, 12))

comp_data = metrics_df.nsmallest(30, 'composite').sort_values('composite', ascending=True)

colors = plt.cm.RdYlGn(comp_data['composite'])

bars = ax.barh(comp_data['state'], comp_data['composite'], color=colors, edgecolor='white', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, comp_data['composite']):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.3f}', va='center', fontsize=8)

ax.set_xlabel('Composite Score (Higher = Better)', fontweight='bold', fontsize=12)
ax.set_ylabel('State', fontweight='bold', fontsize=12)
ax.set_title('Priority Intervention States\n(Lowest Composite Scores = Highest Priority)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 1.1)

plt.tight_layout()
plt.savefig(output_dir / 'chart4_composite_rankings.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart4_composite_rankings.png")

# ============================================
# CHART 5: Enrolment vs Update Scatter
# ============================================
print("[5/8] Generating Enrolment vs IFI Scatter...")

fig, ax = plt.subplots(figsize=(12, 10))

# Size by population
sizes = metrics_df['total_enrolments'] / metrics_df['total_enrolments'].max() * 500 + 50
colors_scatter = plt.cm.viridis(metrics_df['composite'])

scatter = ax.scatter(
    metrics_df['total_enrolments'], 
    metrics_df['ifi'],
    s=sizes,
    c=metrics_df['composite'],
    cmap='RdYlGn',
    alpha=0.7,
    edgecolors='white',
    linewidth=1
)

# Annotate outliers
for _, row in metrics_df.nlargest(5, 'total_enrolments').iterrows():
    ax.annotate(row['state'], (row['total_enrolments'], row['ifi']), fontsize=8, alpha=0.8)

plt.colorbar(scatter, label='Composite Score')
ax.set_xlabel('Total Enrolments', fontweight='bold', fontsize=12)
ax.set_ylabel('Identity Freshness Index (IFI)', fontweight='bold', fontsize=12)
ax.set_title('Does High Enrolment Mean Fresh Data?', fontsize=16, fontweight='bold', pad=20)
ax.set_xscale('log')

plt.tight_layout()
plt.savefig(output_dir / 'chart5_enrolment_vs_ifi.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart5_enrolment_vs_ifi.png")

# ============================================
# CHART 6: Metrics Heatmap
# ============================================
print("[6/8] Generating Metrics Heatmap...")

fig, ax = plt.subplots(figsize=(12, 14))

# Prepare data for heatmap - normalize metrics
heatmap_data = metrics_df[['state', 'ifi', 'clcr', 'taes', 'composite']].copy()
heatmap_data = heatmap_data.dropna()

# Normalize to 0-1 for visualization
for col in ['ifi', 'clcr', 'taes']:
    heatmap_data[f'{col}_norm'] = (heatmap_data[col] - heatmap_data[col].min()) / (heatmap_data[col].max() - heatmap_data[col].min())

heatmap_matrix = heatmap_data.set_index('state')[['ifi_norm', 'clcr_norm', 'taes_norm', 'composite']].head(30)
heatmap_matrix.columns = ['IFI', 'CLCR', 'TAES', 'Composite']

sns.heatmap(heatmap_matrix, cmap='RdYlGn', annot=True, fmt='.2f', linewidths=0.5, ax=ax,
            cbar_kws={'label': 'Normalized Score'})

ax.set_title('State Performance Dashboard\n(Green = Better, Red = Needs Attention)', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Metric', fontweight='bold')
ax.set_ylabel('State', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / 'chart6_metrics_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart6_metrics_heatmap.png")

# ============================================
# CHART 7: Summary Dashboard
# ============================================
print("[7/8] Generating Summary Dashboard...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('UIDAI Identity Lifecycle Health Dashboard', fontsize=18, fontweight='bold', y=1.02)

# Panel 1: Total Records
ax1 = axes[0, 0]
totals = {
    'Enrolments': metrics_df['total_enrolments'].sum(),
    'Demo Updates': metrics_df['ifi'].sum() * 0.4 * metrics_df['total_enrolments'].sum() / 100,  # Approximation
    'Bio Updates': metrics_df['ifi'].sum() * 0.6 * metrics_df['total_enrolments'].sum() / 100   # Approximation
}
colors_bar = [COLORS['primary'], COLORS['secondary'], COLORS['healthy']]
bars = ax1.bar(totals.keys(), totals.values(), color=colors_bar)
ax1.set_title('Total Activity Volume', fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

# Panel 2: IFI Distribution
ax2 = axes[0, 1]
ax2.hist(metrics_df['ifi'], bins=20, color=COLORS['primary'], edgecolor='white', alpha=0.7)
ax2.axvline(x=national_ifi, color='red', linestyle='--', linewidth=2, label=f'Mean: {national_ifi:.1f}')
ax2.set_title('IFI Distribution Across States', fontweight='bold')
ax2.set_xlabel('IFI Score')
ax2.legend()

# Panel 3: TAES Distribution
ax3 = axes[1, 0]
taes_below = len(metrics_df[metrics_df['taes'] < 0.7])
taes_above = len(metrics_df[metrics_df['taes'] >= 0.7])
ax3.pie([taes_below, taes_above], labels=[f'Below 0.7\n({taes_below} states)', f'Above 0.7\n({taes_above} states)'],
        colors=[COLORS['critical'], COLORS['healthy']], autopct='%1.0f%%', startangle=90)
ax3.set_title('Weekend Access Equity (TAES)', fontweight='bold')

# Panel 4: Top/Bottom States
ax4 = axes[1, 1]
top5 = metrics_df.nlargest(5, 'composite')[['state', 'composite']]
bottom5 = metrics_df.nsmallest(5, 'composite')[['state', 'composite']]

y_pos = np.arange(5)
ax4.barh(y_pos + 0.2, top5['composite'], height=0.35, color=COLORS['healthy'], label='Top 5')
ax4.barh(y_pos - 0.2, bottom5['composite'], height=0.35, color=COLORS['critical'], label='Bottom 5')

ax4.set_yticks(y_pos)
ax4.set_yticklabels([f"{t} / {b}" for t, b in zip(top5['state'].values, bottom5['state'].values)], fontsize=8)
ax4.set_xlabel('Composite Score')
ax4.set_title('Top vs Bottom Performing States', fontweight='bold')
ax4.legend()

plt.tight_layout()
plt.savefig(output_dir / 'chart7_summary_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart7_summary_dashboard.png")

# ============================================
# CHART 8: Age Distribution Comparison
# ============================================
print("[8/8] Generating Age Distribution Chart...")

fig, ax = plt.subplots(figsize=(12, 8))

# Create sample age distribution from metrics
age_data = {
    'State': metrics_df.nlargest(10, 'total_enrolments')['state'],
    'Volume': metrics_df.nlargest(10, 'total_enrolments')['total_enrolments']
}

x = np.arange(len(age_data['State']))
width = 0.6

bars = ax.bar(x, age_data['Volume'], width, color=plt.cm.viridis(np.linspace(0.2, 0.8, 10)))

ax.set_xlabel('State', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Enrolments', fontweight='bold', fontsize=12)
ax.set_title('Top 10 States by Enrolment Volume', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(age_data['State'], rotation=45, ha='right')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))

plt.tight_layout()
plt.savefig(output_dir / 'chart8_top_states_volume.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   Saved: chart8_top_states_volume.png")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("VISUALIZATION GENERATION COMPLETE")
print("="*70)
print(f"\n8 charts saved to: {output_dir}")

for f in sorted(output_dir.glob('chart*.png')):
    print(f"   {f.name}")

print("\nReady for submission!")
