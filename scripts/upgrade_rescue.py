
import nbformat
import numpy as np

# Source is the SAFE backup
nb_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb'
# Target is the one we want to create/fix
out_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'

print(f"Reading backup from {nb_path}...")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

print(f"Loaded {len(nb.cells)} cells. Applying visual upgrades...")

# ============================================
# NEW STYLE SETUP (Cell 6) - VERIFY INDEX
# ============================================
# In MASTER_file.ipynb, Cell 6 (0-indexed) is the imports. 
# Cell 0: Style CSS
# Cell 1: Title
# Cell 2: TOC
# Cell 3: Markdown intro
# Cell 4: Evidence Base
# Cell 5: Approach
# Cell 6: IMPORTS (Starts with # ====================)
# Let's verify content starts with SETUP & IMPORTS or replace it if it looks like code.
if nb.cells[6].cell_type == 'code':
    print("Updating Cell 6 (Imports/Style)...")
    nb.cells[6].source = """# ============================================
# SETUP & IMPORTS
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# VISUALIZATION STYLING
# ---------------------------------------------------------
# Set professional style for government/consulting reports
plt.style.use('seaborn-v0_8-whitegrid')

# Global Figure Settings
plt.rcParams['figure.figsize'] = (16, 10)  # Larger, presentation-ready
plt.rcParams['figure.dpi'] = 150           # High resolution
plt.rcParams['figure.titlesize'] = 20      # Main title size
plt.rcParams['figure.titleweight'] = 'bold'

# Axes Settings
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Tick Settings
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Legend Settings
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.framealpha'] = 0.95
plt.rcParams['legend.facecolor'] = 'white'
plt.rcParams['legend.edgecolor'] = '#dbdbdb'

# Font Family (clean, sans-serif)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']

# ---------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------
# Consistent, high-contrast palette
COLORS = {
    'critical': '#d32f2f',   # Strong Red
    'at_risk': '#fbc02d',    # Warning Yellow/Amber
    'healthy': '#388e3c',    # Strong Green
    'optimal': '#1976d2',    # Primary Blue
    'primary': '#1565c0',    # Deep Blue
    'secondary': '#546e7a',  # Blue Grey
    'neutral': '#9e9e9e',    # Grey
    'text_main': '#212121',  # Almost Black
    'background': '#ffffff'  # White
}

# Custom Color Maps
cmap_risk = mcolors.LinearSegmentedColormap.from_list("risk", [COLORS['healthy'], COLORS['at_risk'], COLORS['critical']])
cmap_performance = mcolors.LinearSegmentedColormap.from_list("perf", [COLORS['critical'], COLORS['at_risk'], COLORS['healthy'], COLORS['optimal']])

print("✅ Visualization standards applied successfully")
"""

# ============================================
# IDENTIFY AND REPLACE PLOTTING CELLS
# ============================================
# We will search for key phrases to identify the correct cells since indices might slightly vary if backup differs.
# But inspect output showed generic structure. We'll target by string presence.

def update_cell_if_contains(search_str, new_content):
    count = 0
    for cell in nb.cells:
        if cell.cell_type == 'code' and search_str in cell.source:
            cell.source = new_content
            count += 1
            # Break after first match to avoid duplicates if any? 
            # In this notebook, plots are distinct.
    if count == 0:
        print(f"⚠️ Warning: Could not find cell containing '{search_str}'")
    else:
        print(f"Updated {count} cell(s) for '{search_str}'")

# CELL 12: Daily Enrolment
update_cell_if_contains("Daily Enrolment Trend", """# Insight 1: DAILY ENROLMENT TREND
# ============================================
# Insight: Visualizing the 'Weekend Gap' in enrolment efficiency.

fig, ax = plt.subplots(figsize=(16, 8))

daily_enrol = enrolment_df.groupby('date')['total_enrolments'].sum()
rolling_avg = daily_enrol.rolling(7).mean()

# 1. Plot Data
ax.plot(daily_enrol.index, daily_enrol.values, alpha=0.4, color=COLORS['secondary'], label='Daily Volume', linewidth=1)
ax.plot(daily_enrol.index, rolling_avg, linewidth=3, color=COLORS['primary'], label='7-Day Rolling Average')

# 2. Statistical Annotations
mean_val = daily_enrol.mean()
ax.axhline(y=mean_val, color=COLORS['healthy'], linestyle='--', linewidth=2, label=f'Period Mean: {mean_val:,.0f}')

# Highlight Weekends
ax.annotate('Regular Weekend Dips', xy=(mdates.date2num(daily_enrol.index[13]), daily_enrol.values[13]), 
            xytext=(mdates.date2num(daily_enrol.index[25]), daily_enrol.values[13] + 5000),
            arrowprops=dict(facecolor=COLORS['text_main'], shrink=0.05), fontsize=12, fontweight='bold')

# 3. Formatting
ax.set_title('Daily Enrolment Consistency: The "Weekend Gap" Phenomenon', pad=20)
ax.set_xlabel('Timeline (2025)', labelpad=10)
ax.set_ylabel('Total Daily Enrolments', labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True, shadow=True)

# 4. Insight Text
plt.figtext(0.5, -0.05, "Insight: Consistent dips every 7 days indicate significant drop in service availability on weekends, potentially excluding working-class citizens.", 
            ha='center', fontsize=12, style='italic', bbox={'facecolor': '#f5f5f5', 'alpha': 0.5, 'pad': 10})

plt.tight_layout()
plt.show()

# Anomaly stats
z_scores = (daily_enrol - mean_val) / daily_enrol.std()
print(f"Stats: Mean={mean_val:,.0f}, Anomalies={len(daily_enrol[abs(z_scores)>2])}")""")

# CELL 14: Age Distribution
update_cell_if_contains("Age Distribution", """# Insight 2: DEMOGRAPHIC COMPOSITION
# ============================================
# Insight: Who are we enrolling?

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Data Prep
age_totals = [
    enrolment_df['age_0_5'].sum(),
    enrolment_df['age_5_17'].sum(),
    enrolment_df['age_18_greater'].sum()
]
labels = ['0-5 Years (Child)', '5-17 Years (Student)', '18+ Years (Adult)']
colors = [COLORS['at_risk'], COLORS['optimal'], COLORS['primary']]

# 1. Pie Chart (Donut)
wedges, texts, autotexts = axes[0].pie(age_totals, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90, pctdistance=0.85, 
                                        wedgeprops=dict(width=0.5, edgecolor='white'))
for t in texts: t.set_fontsize(11)
for t in autotexts: t.set_fontsize(11); t.set_fontweight('bold'); t.set_color('white')

axes[0].set_title('Share of Total Enrolments', pad=15)
axes[0].text(0, 0, f"Total\\n{sum(age_totals)/1e6:.1f}M", ha='center', va='center', fontsize=14, fontweight='bold')

# 2. Bar Chart
bar_x = np.arange(len(labels))
bars = axes[1].bar(bar_x, age_totals, color=colors, edgecolor='white', width=0.6)

for bar in bars:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.01*max(age_totals),
            f'{height/1e6:.1f} M', ha='center', va='bottom', fontweight='bold', fontsize=11)

axes[1].set_title('Absolute Volume by Age Segment', pad=15)
axes[1].set_xticks(bar_x)
axes[1].set_xticklabels(labels)
axes[1].set_ylabel('Enrolments (Millions)')
axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
axes[1].grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('Enrolment Demographics: Focus on Youth', fontsize=22, y=1.05)
plt.tight_layout()
plt.show()""")

# CELL 16: Weekend vs Weekday
update_cell_if_contains("Weekend vs Weekday", """# Insight 3: WEEKEND ACCESSIBILITY GAP
# ============================================
# Insight: Quantifying the service drop-off on weekends.

fig, ax = plt.subplots(figsize=(14, 7))

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_data = enrolment_df.groupby('weekday')['total_enrolments'].sum().reindex(weekday_order)

# Conditional Coloring
colors_week = [COLORS['healthy'] if day in ['Saturday', 'Sunday'] else COLORS['primary'] for day in weekday_order]

bars = ax.bar(weekday_data.index, weekday_data.values, color=colors_week, edgecolor='white', width=0.7)

# Annotation of the Gap
avg_weekday = weekday_data[:5].mean()
avg_weekend = weekday_data[5:].mean()
gap_pct = (avg_weekend - avg_weekday) / avg_weekday * 100

ax.axhline(y=avg_weekday, color=COLORS['primary'], linestyle='--', alpha=0.5, label='Avg Weekday Volume')
ax.axhline(y=avg_weekend, color=COLORS['healthy'], linestyle='--', alpha=0.5, label='Avg Weekend Volume')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02*max(weekday_data.values),
            f'{height/1000:.0f}K', ha='center', va='bottom', fontsize=10)

arrow_x = 5.5 # Between Sat/Sun
ax.annotate(f'{gap_pct:.1f}% Drop', 
            xy=(arrow_x, avg_weekend), xytext=(arrow_x, avg_weekday),
            arrowprops=dict(arrowstyle='<->', color=COLORS['critical'], lw=2),
            ha='center', va='center', fontweight='bold', color=COLORS['critical'], backgroundcolor='white')

ax.set_title('Service Accessibility: Significant Drop-off on Weekends', pad=20)
ax.set_ylabel('Total Enrolments')
ax.set_xlabel('')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax.legend(loc='upper left')

plt.tight_layout()
plt.show()""")

# CELL 18: Scatter
update_cell_if_contains("Color by IFI", """# Insight 4: UPDATE EFFICIENCY MATRIX
# ============================================
# Insight: Are high-enrolment states keeping their data fresh?

# Pre-calc metrics
enrol_state = enrolment_df.groupby('state')['total_enrolments'].sum().reset_index()
demo_state = demographic_df.groupby('state')['total_demo_updates'].sum().reset_index()
bio_state = biometric_df.groupby('state')['total_bio_updates'].sum().reset_index()
state_df = enrol_state.merge(demo_state, on='state', how='left').merge(bio_state, on='state', how='left').fillna(0)
state_df['total_updates'] = state_df['total_demo_updates'] + state_df['total_bio_updates']
state_df['ifi'] = state_df['total_updates'] / state_df['total_enrolments'].replace(0, np.nan)
state_df = state_df.fillna(0)

fig, ax = plt.subplots(figsize=(14, 10))

# Color by IFI (Risk Level)
scatter = ax.scatter(state_df['total_enrolments'], state_df['total_updates'],
                     c=state_df['ifi'], cmap='RdYlGn', s=150, alpha=0.8, edgecolors='#424242', linewidth=0.5)

# Add Trend Line
z = np.polyfit(state_df['total_enrolments'], state_df['total_updates'], 1)
p = np.poly1d(z)
ax.plot(state_df['total_enrolments'], p(state_df['total_enrolments']), "r--", alpha=0.4, label='Expected Update Volume')

# Annotate Notable States
for _, row in state_df.nlargest(5, 'total_enrolments').iterrows():
    ax.annotate(row['state'], (row['total_enrolments'], row['total_updates']),
                xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')

cbar = plt.colorbar(scatter)
cbar.set_label('Identity Freshness Index (IFI)', fontweight='bold')

ax.set_title('Update Conversion Efficiency: Volume vs. Freshness', pad=20)
ax.set_xlabel('Total Enrolment Base (Log Scale)', fontweight='bold')
ax.set_ylabel('Total Updates Processed (Log Scale)', fontweight='bold')
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True, which="both", ls="-", alpha=0.2)
ax.legend()

plt.figtext(0.5, -0.05, "Insight: States below the red line are under-performing on updates relative to their population size.", 
            ha='center', fontsize=12, style='italic', bbox={'facecolor': '#f5f5f5', 'alpha': 0.5, 'pad': 10})

plt.tight_layout()
plt.show()""")

# CELL 20: TAES
update_cell_if_contains("TAES by state", """# Insight 5: WEEKEND ACCESS EQUITY (TAES)
# ============================================
# Insight: Identifying states that limit access for working citizens.

# Calc TAES
daily_state = enrolment_df.groupby(['state', 'date', 'is_weekend'])['total_enrolments'].sum().reset_index()
weekend_avg = daily_state[daily_state['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekday_avg = daily_state[~daily_state['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekend_avg.columns = ['state', 'weekend_avg']
weekday_avg.columns = ['state', 'weekday_avg']
taes_df = weekend_avg.merge(weekday_avg, on='state', how='outer').fillna(0)
taes_df['taes'] = taes_df['weekend_avg'] / taes_df['weekday_avg'].replace(0, np.nan)
taes_df['taes'] = taes_df['taes'].fillna(0).clip(upper=1.5)

fig, ax = plt.subplots(figsize=(16, 12))

# Filter: Focus on Bottom 20 States
plot_data = taes_df.sort_values('taes', ascending=True).head(20)
colors_taes = [COLORS['critical'] if t < 0.7 else COLORS['at_risk'] for t in plot_data['taes']]

bars = ax.barh(plot_data['state'], plot_data['taes'], color=colors_taes, edgecolor='white', height=0.6)

ax.axvline(x=0.70, color=COLORS['at_risk'], linestyle='--', linewidth=2, label='Minimum Standard (0.70)')
ax.axvline(x=1.0, color=COLORS['healthy'], linestyle='-', linewidth=2, alpha=0.5, label='Ideal Parity (1.0)')

for bar, val in zip(bars, plot_data['taes']):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.2f}', 
            va='center', fontsize=10, fontweight='bold', color=COLORS['text_main'])

ax.set_title('Weekend Access Equity: Bottom 20 States', pad=20)
ax.set_xlabel('Temporal Access Equity Score (TAES)', fontweight='bold')
ax.set_ylabel('')
ax.set_xlim(0, 1.2)
ax.legend(loc='lower right')

ax.text(0.02, 0.95, "CRITICAL ZONE (< 0.70)\\nCitizens struggle to find\\nopen centers on weekends.", 
        transform=ax.transAxes, fontsize=12, fontweight='bold', color=COLORS['critical'],
        bbox=dict(facecolor='white', edgecolor=COLORS['critical'], boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.show()""")

# CELL 22: Lifecycle Gap Analysis
update_cell_if_contains("Lifecycle Gap Analysis", """# Insight 6: CHILD BIOMETRIC GAP
# ============================================
# Insight: Are we enrolling children but failing to update their biometrics later?

# Calc Lifecycle
enrol_age = enrolment_df.groupby('state').agg({'age_5_17': 'sum', 'total_enrolments': 'sum'}).reset_index()
bio_age = biometric_df.groupby('state').agg({'bio_age_5_17': 'sum', 'total_bio_updates': 'sum'}).reset_index()
lifecycle = enrol_age.merge(bio_age, on='state')
lifecycle['child_enrol_share'] = lifecycle['age_5_17'] / lifecycle['total_enrolments']
lifecycle['child_bio_share'] = lifecycle['bio_age_5_17'] / lifecycle['total_bio_updates'].replace(0, 1)
lifecycle['lifecycle_gap'] = lifecycle['child_enrol_share'] - lifecycle['child_bio_share']

fig, ax = plt.subplots(figsize=(14, 10))

sizes = lifecycle['total_enrolments'] / lifecycle['total_enrolments'].max() * 800 + 50
scatter = ax.scatter(lifecycle['child_enrol_share'], lifecycle['child_bio_share'],
                     s=sizes, c=lifecycle['lifecycle_gap'], cmap='RdYlGn_r',
                     alpha=0.7, edgecolors='#424242', linewidth=1)

ax.plot([0, 0.6], [0, 0.6], color=COLORS['text_main'], linestyle='--', alpha=0.5, label='Ideal Ratio (1:1)')

high_gap = lifecycle.nlargest(5, 'lifecycle_gap')
for _, row in high_gap.iterrows():
    ax.annotate(row['state'], (row['child_enrol_share'], row['child_bio_share']),
                xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')

cbar = plt.colorbar(scatter)
cbar.set_label('Lifecycle Gap Magnitude', fontweight='bold')

ax.set_title('Lifecycle Disconnect: Child Enrolment vs. Biometric Updates', pad=20)
ax.set_xlabel('Child Share of New Enrolments', fontweight='bold')
ax.set_ylabel('Child Share of Biometric Updates', fontweight='bold')
ax.legend()

plt.figtext(0.5, -0.05, "Insight: Large bubbles in the lower-right quadrant indicate states acquiring many children but failing to capture their Mandatory Biometric Updates.", 
            ha='center', fontsize=12, style='italic', bbox={'facecolor': '#f5f5f5', 'alpha': 0.5, 'pad': 10})

plt.tight_layout()
plt.show()""")

# CELL 24: IFI Ranking
update_cell_if_contains("IFI Ranking Chart", """# Insight 7: STATE HEALTH RANKINGS (IFI)
# ============================================
# Insight: The definitive leaderboard for Aadhaar ecosystem health.

fig, ax = plt.subplots(figsize=(16, 12))

# Calc Risk
state_df.loc[state_df['ifi'] < 0.20, 'ifi_risk'] = 'Critical'
state_df.loc[(state_df['ifi'] >= 0.20) & (state_df['ifi'] < 0.40), 'ifi_risk'] = 'At Risk'
state_df.loc[state_df['ifi'] >= 0.40, 'ifi_risk'] = 'Healthy'

plot_data = state_df.nsmallest(25, 'ifi').sort_values('ifi', ascending=True)
colors_ifi = []
for ifi in plot_data['ifi']:
    if ifi < 0.20: colors_ifi.append(COLORS['critical'])
    elif ifi < 0.40: colors_ifi.append(COLORS['at_risk'])
    else: colors_ifi.append(COLORS['healthy'])

ax.hlines(y=plot_data['state'], xmin=0, xmax=plot_data['ifi'], color=colors_ifi, alpha=0.6, linewidth=3)
ax.scatter(plot_data['ifi'], plot_data['state'], color=colors_ifi, s=120, zorder=5, edgecolors='white', linewidth=1)

for i, (ifi, state) in enumerate(zip(plot_data['ifi'], plot_data['state'])):
    ax.text(ifi + 0.02, i, f'{ifi:.2f}', va='center', fontsize=10, fontweight='bold', color='#424242')

national_avg = state_df['total_updates'].sum() / state_df['total_enrolments'].sum()
ax.axvline(x=national_avg, color=COLORS['primary'], linestyle='--', linewidth=2, label=f'National Avg: {national_avg:.2f}')

ax.set_title('Identity Freshness Index (IFI): Priority States for Intervention', pad=20)
ax.set_xlabel('IFI Score (Updates per Enrolment)', fontweight='bold')
ax.set_ylabel('')
ax.set_xlim(0, max(plot_data['ifi']) + 0.2)
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()""")

# CELL 26: CLCR
update_cell_if_contains("# CLCR", """# Insight 8: MANDATORY UPDATE COMPLIANCE (CLCR)
# ============================================
# Insight: Are we effectively capturing the 5/15 year mandatory updates?

# Calc CLCR
clcr_df = enrolment_df.groupby('state')['age_5_17'].sum().reset_index()
bio_clcr = biometric_df.groupby('state')['bio_age_5_17'].sum().reset_index()
clcr_df = clcr_df.merge(bio_clcr, on='state', how='left').fillna(0)
clcr_df['expected'] = clcr_df['age_5_17'] * 0.20 # Approx target
clcr_df['clcr'] = clcr_df['bio_age_5_17'] / clcr_df['expected'].replace(0, np.nan)
clcr_df = clcr_df.fillna(0)

# Merge back to state_df for composite
state_df = state_df.merge(clcr_df[['state', 'clcr']], on='state', how='left')
state_df = state_df.merge(taes_df[['state', 'taes']], on='state', how='left')

fig, ax = plt.subplots(figsize=(14, 10))

clcr_plot = clcr_df.nsmallest(20, 'clcr').sort_values('clcr', ascending=True)
colors_clcr = [COLORS['critical'] if c < 1 else COLORS['healthy'] for c in clcr_plot['clcr']]

ax.barh(clcr_plot['state'], clcr_plot['clcr'].clip(upper=5), color=colors_clcr, edgecolor='white')
ax.axvline(x=1.0, color='black', linestyle='--', linewidth=2, label='Target (1.0)')

ax.set_title('Mandatory Biometric Update Gap', pad=20)
ax.set_xlabel('Capture Rate (Actual / Expected)', fontweight='bold')
ax.set_ylabel('')
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()""")

# CELL 28: Heatmap
# Note: searching for "# Composite Score"
update_cell_if_contains("# Composite Score", """# Insight 9: 360-DEGREE STATE PERFORMANCE
# ============================================
# Insight: A holistic view of state health across all dimensions.

# Calc Composite
state_df['composite'] = (
    state_df['ifi'].clip(upper=1) * 0.40 +
    state_df['clcr'].clip(upper=1).fillna(0) * 0.30 +
    state_df['taes'].clip(upper=1).fillna(0) * 0.30
)
state_df = state_df.sort_values('composite', ascending=True)

fig, ax = plt.subplots(figsize=(12, 14))

heatmap_data = state_df.head(30).set_index('state')[['ifi', 'clcr', 'taes', 'composite']].copy()
# Normalize
for col in heatmap_data.columns:
    heatmap_data[col] = (heatmap_data[col] - heatmap_data[col].min()) / (heatmap_data[col].max() - heatmap_data[col].min() + 0.001)

sns.heatmap(heatmap_data, cmap='RdYlGn', annot=True, fmt='.2f', linewidths=0.5, ax=ax, cbar_kws={'label': 'Normalized Score (0-1)'})

ax.set_title('Holistic State Health Dashboard', pad=20)
ax.set_ylabel('')
ax.set_xlabel('Key Performance Indicators', fontweight='bold')

plt.tight_layout()
plt.show()

display(state_df.head(10)[['state', 'ifi', 'clcr', 'taes', 'composite']])""")

print("Updates complete. Saving file...")
with open(out_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"successfully restored and upgraded {out_path}")
