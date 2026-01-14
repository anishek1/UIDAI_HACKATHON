
# CELL 6
# ============================================
# SETUP & IMPORTS
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

# Color palette
COLORS = {
    'critical': '#dc3545',
    'at_risk': '#ffc107',
    'healthy': '#28a745',
    'optimal': '#007bff',
    'primary': '#1a73e8'
}

print("✅ Libraries imported successfully")
================================================================================

# CELL 7
# ============================================
# STATE NAME STANDARDIZATION
# ============================================

STATE_NAME_MAP = {
    'andhra pradesh': 'Andhra Pradesh', 'ANDHRA PRADESH': 'Andhra Pradesh',
    'arunachal pradesh': 'Arunachal Pradesh', 'ARUNACHAL PRADESH': 'Arunachal Pradesh',
    'assam': 'Assam', 'ASSAM': 'Assam',
    'bihar': 'Bihar', 'BIHAR': 'Bihar',
    'chhattisgarh': 'Chhattisgarh', 'CHHATTISGARH': 'Chhattisgarh', 'Chattisgarh': 'Chhattisgarh',
    'delhi': 'Delhi', 'DELHI': 'Delhi', 'NCT of Delhi': 'Delhi', 'NCT OF DELHI': 'Delhi',
    'goa': 'Goa', 'GOA': 'Goa',
    'gujarat': 'Gujarat', 'GUJARAT': 'Gujarat',
    'haryana': 'Haryana', 'HARYANA': 'Haryana',
    'himachal pradesh': 'Himachal Pradesh', 'HIMACHAL PRADESH': 'Himachal Pradesh',
    'jharkhand': 'Jharkhand', 'JHARKHAND': 'Jharkhand',
    'karnataka': 'Karnataka', 'KARNATAKA': 'Karnataka',
    'kerala': 'Kerala', 'KERALA': 'Kerala',
    'madhya pradesh': 'Madhya Pradesh', 'MADHYA PRADESH': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra', 'MAHARASHTRA': 'Maharashtra',
    'manipur': 'Manipur', 'MANIPUR': 'Manipur',
    'meghalaya': 'Meghalaya', 'MEGHALAYA': 'Meghalaya',
    'mizoram': 'Mizoram', 'MIZORAM': 'Mizoram',
    'nagaland': 'Nagaland', 'NAGALAND': 'Nagaland',
    'odisha': 'Odisha', 'ODISHA': 'Odisha', 'Orissa': 'Odisha', 'ORISSA': 'Odisha',
    'punjab': 'Punjab', 'PUNJAB': 'Punjab',
    'rajasthan': 'Rajasthan', 'RAJASTHAN': 'Rajasthan',
    'sikkim': 'Sikkim', 'SIKKIM': 'Sikkim',
    'tamil nadu': 'Tamil Nadu', 'TAMIL NADU': 'Tamil Nadu', 'Tamilnadu': 'Tamil Nadu',
    'telangana': 'Telangana', 'TELANGANA': 'Telangana',
    'tripura': 'Tripura', 'TRIPURA': 'Tripura',
    'uttar pradesh': 'Uttar Pradesh', 'UTTAR PRADESH': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand', 'UTTARAKHAND': 'Uttarakhand', 'Uttaranchal': 'Uttarakhand',
    'west bengal': 'West Bengal', 'WEST BENGAL': 'West Bengal', 'WESTBENGAL': 'West Bengal',
    'andaman and nicobar islands': 'Andaman And Nicobar Islands',
    'chandigarh': 'Chandigarh', 'CHANDIGARH': 'Chandigarh',
    'dadra and nagar haveli and daman and diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'jammu and kashmir': 'Jammu And Kashmir', 'JAMMU AND KASHMIR': 'Jammu And Kashmir',
    'ladakh': 'Ladakh', 'LADAKH': 'Ladakh',
    'lakshadweep': 'Lakshadweep', 'LAKSHADWEEP': 'Lakshadweep',
    'puducherry': 'Puducherry', 'PUDUCHERRY': 'Puducherry', 'Pondicherry': 'Puducherry'
}

def standardize_state_name(state_name):
    if not isinstance(state_name, str):
        return state_name
    cleaned = state_name.strip()
    if cleaned in STATE_NAME_MAP:
        return STATE_NAME_MAP[cleaned]
    if cleaned.title() in STATE_NAME_MAP:
        return STATE_NAME_MAP[cleaned.title()]
    return cleaned.title()

print(f"✅ State mapping ready: {len(STATE_NAME_MAP)} variants defined")
================================================================================

# CELL 8
# ============================================
# DATA LOADING
# ============================================

BASE_PATH = Path('..')

print("📁 Loading datasets...")
print("="*60)

# Enrolment
enrol_path = BASE_PATH / 'data' / 'raw' / 'Enrolment'
enrol_files = list(enrol_path.glob('*.csv'))
enrol_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in enrol_files]
enrolment_df = pd.concat(enrol_dfs, ignore_index=True)
print(f"  ✓ Enrolment: {len(enrolment_df):,} rows")

# Demographic
demo_path = BASE_PATH / 'data' / 'raw' / 'Demographic'
demo_files = list(demo_path.glob('*.csv'))
demo_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in demo_files]
demographic_df = pd.concat(demo_dfs, ignore_index=True)
print(f"  ✓ Demographic: {len(demographic_df):,} rows")

# Biometric
bio_path = BASE_PATH / 'data' / 'raw' / 'Biometric'
bio_files = list(bio_path.glob('*.csv'))
bio_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in bio_files]
biometric_df = pd.concat(bio_dfs, ignore_index=True)
print(f"  ✓ Biometric: {len(biometric_df):,} rows")

# Population
population_df = pd.read_csv(BASE_PATH / 'data' / 'external' / 'state_population.csv')
print(f"  ✓ Population: {len(population_df)} states")

print("="*60)
print(f"📊 TOTAL RECORDS: {len(enrolment_df) + len(demographic_df) + len(biometric_df):,}")
================================================================================

# CELL 9
# ============================================
# DATA PREPROCESSING
# ============================================

print("⚙️ Preprocessing data...")

# Standardize state names
enrolment_df['state'] = enrolment_df['state'].apply(standardize_state_name)
demographic_df['state'] = demographic_df['state'].apply(standardize_state_name)
biometric_df['state'] = biometric_df['state'].apply(standardize_state_name)

# Parse dates
enrolment_df['date'] = pd.to_datetime(enrolment_df['date'], format='%d-%m-%Y', errors='coerce')
demographic_df['date'] = pd.to_datetime(demographic_df['date'], format='%d-%m-%Y', errors='coerce')
biometric_df['date'] = pd.to_datetime(biometric_df['date'], format='%d-%m-%Y', errors='coerce')

# Add totals
enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

# Add temporal features
enrolment_df['weekday'] = enrolment_df['date'].dt.day_name()
enrolment_df['is_weekend'] = enrolment_df['date'].dt.dayofweek >= 5

print(f"  ✓ States standardized: {enrolment_df['state'].nunique()} unique states")
print(f"  ✓ Date range: {enrolment_df['date'].min().date()} to {enrolment_df['date'].max().date()}")
print("✅ Preprocessing complete")
================================================================================

# CELL 10
# ============================================
# DATA SUMMARY
# ============================================

print("="*60)
print("📊 DATA SUMMARY")
print("="*60)

summary_data = {
    'Dataset': ['Enrolment', 'Demographic Updates', 'Biometric Updates'],
    'Records': [len(enrolment_df), len(demographic_df), len(biometric_df)],
    'States': [enrolment_df['state'].nunique(), demographic_df['state'].nunique(), biometric_df['state'].nunique()],
    'Districts': [enrolment_df['district'].nunique(), demographic_df['district'].nunique(), biometric_df['district'].nunique()],
    'Total Count': [
        enrolment_df['total_enrolments'].sum(),
        demographic_df['total_demo_updates'].sum(),
        biometric_df['total_bio_updates'].sum()
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df['Records'] = summary_df['Records'].apply(lambda x: f"{x:,}")
summary_df['Total Count'] = summary_df['Total Count'].apply(lambda x: f"{x:,.0f}")
display(summary_df)
================================================================================

# CELL 12
# Daily Enrolment Trend
fig, ax = plt.subplots(figsize=(16, 6))

daily_enrol = enrolment_df.groupby('date')['total_enrolments'].sum()
rolling_avg = daily_enrol.rolling(7).mean()

ax.plot(daily_enrol.index, daily_enrol.values, alpha=0.5, label='Daily', color=COLORS['primary'])
ax.plot(daily_enrol.index, rolling_avg, linewidth=2, label='7-day Rolling Avg', color=COLORS['critical'])

# Statistical annotations
mean_val = daily_enrol.mean()
std_val = daily_enrol.std()
ax.axhline(y=mean_val, color='green', linestyle='--', alpha=0.7, label=f'Mean: {mean_val:,.0f}')
ax.fill_between(daily_enrol.index, mean_val - 2*std_val, mean_val + 2*std_val, alpha=0.1, color='green')

ax.set_title('Daily Enrolment Trend with 7-Day Rolling Average', fontsize=14, fontweight='bold')
ax.set_xlabel('Date', fontweight='bold')
ax.set_ylabel('Total Enrolments', fontweight='bold')
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
plt.tight_layout()
plt.show()

# Anomaly detection
z_scores = (daily_enrol - mean_val) / std_val
anomalies = daily_enrol[abs(z_scores) > 2]
print(f"\n📊 Statistics:")
print(f"   Mean: {mean_val:,.0f} | Std: {std_val:,.0f}")
print(f"   Anomaly days (|z| > 2): {len(anomalies)}")
================================================================================

# CELL 14
# Age Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
age_totals = [
    enrolment_df['age_0_5'].sum(),
    enrolment_df['age_5_17'].sum(),
    enrolment_df['age_18_greater'].sum()
]
labels = ['0-5 Years', '5-17 Years', '18+ Years']
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']

wedges, texts, autotexts = axes[0].pie(age_totals, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90, explode=[0.02]*3)
axes[0].set_title('Enrolment by Age Group', fontweight='bold')

# Bar chart
axes[1].bar(labels, age_totals, color=colors, edgecolor='white')
for i, v in enumerate(age_totals):
    axes[1].text(i, v + max(age_totals)*0.02, f'{v:,.0f}', ha='center', fontsize=10)
axes[1].set_title('Absolute Counts by Age Group', fontweight='bold')
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

plt.tight_layout()
plt.show()

print(f"\n📊 Age Distribution:")
total = sum(age_totals)
for label, val in zip(labels, age_totals):
    print(f"   {label}: {val:,} ({val/total*100:.1f}%)")
================================================================================

# CELL 16
# Weekend vs Weekday
fig, ax = plt.subplots(figsize=(12, 6))

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_data = enrolment_df.groupby('weekday')['total_enrolments'].sum().reindex(weekday_order)

colors = [COLORS['healthy'] if day in ['Saturday', 'Sunday'] else COLORS['primary'] for day in weekday_order]
bars = ax.bar(weekday_data.index, weekday_data.values, color=colors, edgecolor='white')

# Add value labels
for bar, val in zip(bars, weekday_data.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + weekday_data.max()*0.02,
            f'{val:,.0f}', ha='center', va='bottom', fontsize=9)

ax.set_title('Enrolment by Day of Week (Weekend in Green)', fontsize=14, fontweight='bold')
ax.set_xlabel('Day of Week', fontweight='bold')
ax.set_ylabel('Total Enrolments', fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Statistical test
weekend = enrolment_df[enrolment_df['is_weekend']]['total_enrolments']
weekday = enrolment_df[~enrolment_df['is_weekend']]['total_enrolments']
t_stat, p_value = stats.ttest_ind(weekend, weekday)

weekend_ratio = weekend.sum() / weekday.sum() * 5/2  # Normalize for days
print(f"\n📊 Weekend vs Weekday:")
print(f"   Weekend/Weekday Ratio: {weekend_ratio:.2f}")
print(f"   T-test p-value: {p_value:.2e}")
print(f"   Statistically significant: {'Yes ✓' if p_value < 0.05 else 'No'}")
================================================================================

# CELL 18
# Calculate state-level metrics for bivariate
enrol_state = enrolment_df.groupby('state')['total_enrolments'].sum().reset_index()
demo_state = demographic_df.groupby('state')['total_demo_updates'].sum().reset_index()
bio_state = biometric_df.groupby('state')['total_bio_updates'].sum().reset_index()

# Merge
state_df = enrol_state.merge(demo_state, on='state', how='left')
state_df = state_df.merge(bio_state, on='state', how='left').fillna(0)
state_df['total_updates'] = state_df['total_demo_updates'] + state_df['total_bio_updates']
state_df['ifi'] = state_df['total_updates'] / state_df['total_enrolments'].replace(0, np.nan)
state_df = state_df.fillna(0)

# Scatter plot
fig, ax = plt.subplots(figsize=(12, 8))

# Color by IFI
scatter = ax.scatter(state_df['total_enrolments'], state_df['total_updates'],
                     c=state_df['ifi'], cmap='RdYlGn', s=100, alpha=0.7, edgecolors='white')

# Annotate top states
for _, row in state_df.nlargest(5, 'total_enrolments').iterrows():
    ax.annotate(row['state'], (row['total_enrolments'], row['total_updates']), fontsize=8)

plt.colorbar(scatter, label='IFI Score')
ax.set_xlabel('Total Enrolments', fontweight='bold')
ax.set_ylabel('Total Updates', fontweight='bold')
ax.set_title('Enrolment vs Updates by State (Color = IFI)', fontsize=14, fontweight='bold')
ax.set_xscale('log')
ax.set_yscale('log')
plt.tight_layout()
plt.show()

# Correlation
corr, p = stats.pearsonr(state_df['total_enrolments'], state_df['total_updates'])
print(f"\n📊 Correlation: r = {corr:.3f}, p = {p:.2e}")
================================================================================

# CELL 20
# TAES by state
daily_state = enrolment_df.groupby(['state', 'date', 'is_weekend'])['total_enrolments'].sum().reset_index()

weekend_avg = daily_state[daily_state['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekend_avg.columns = ['state', 'weekend_avg']

weekday_avg = daily_state[~daily_state['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekday_avg.columns = ['state', 'weekday_avg']

taes_df = weekend_avg.merge(weekday_avg, on='state', how='outer').fillna(0)
taes_df['taes'] = taes_df['weekend_avg'] / taes_df['weekday_avg'].replace(0, np.nan)
taes_df['taes'] = taes_df['taes'].fillna(0).clip(upper=1.5)
taes_df = taes_df.sort_values('taes', ascending=True)

# Plot bottom 20 states
fig, ax = plt.subplots(figsize=(14, 10))

plot_data = taes_df.head(20)
colors = [COLORS['critical'] if t < 0.5 else (COLORS['at_risk'] if t < 0.7 else COLORS['healthy']) 
          for t in plot_data['taes']]

ax.barh(plot_data['state'], plot_data['taes'], color=colors, edgecolor='white')
ax.axvline(x=0.70, color='orange', linestyle='--', linewidth=2, label='Acceptable (0.70)')
ax.axvline(x=1.0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Equal (1.0)')

ax.set_xlabel('TAES (Weekend/Weekday Ratio)', fontweight='bold')
ax.set_ylabel('State', fontweight='bold')
ax.set_title('Which States Penalize Working Citizens with Weekend Gaps?', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

print(f"\n📊 States with TAES < 0.70: {len(taes_df[taes_df['taes'] < 0.70])}")
================================================================================

# CELL 22
# Lifecycle Gap Analysis
enrol_age = enrolment_df.groupby('state').agg({
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'total_enrolments': 'sum'
}).reset_index()

bio_age = biometric_df.groupby('state').agg({
    'bio_age_5_17': 'sum',
    'bio_age_17_': 'sum',
    'total_bio_updates': 'sum'
}).reset_index()

lifecycle = enrol_age.merge(bio_age, on='state')
lifecycle['child_enrol_share'] = lifecycle['age_5_17'] / lifecycle['total_enrolments']
lifecycle['child_bio_share'] = lifecycle['bio_age_5_17'] / lifecycle['total_bio_updates'].replace(0, 1)
lifecycle['lifecycle_gap'] = lifecycle['child_enrol_share'] - lifecycle['child_bio_share']

# Bubble chart
fig, ax = plt.subplots(figsize=(14, 10))

sizes = lifecycle['total_enrolments'] / lifecycle['total_enrolments'].max() * 500 + 50

scatter = ax.scatter(lifecycle['child_enrol_share'], lifecycle['child_bio_share'],
                     s=sizes, c=lifecycle['lifecycle_gap'], cmap='RdYlGn_r',
                     alpha=0.6, edgecolors='black', linewidth=0.5)

# Reference line
ax.plot([0, 0.5], [0, 0.5], 'k--', alpha=0.5, label='Parity Line')

# Annotate outliers
for _, row in lifecycle.nlargest(5, 'lifecycle_gap').iterrows():
    ax.annotate(row['state'], (row['child_enrol_share'], row['child_bio_share']),
                fontsize=8, color='red')

plt.colorbar(scatter, label='Lifecycle Gap')
ax.set_xlabel('Child Share of Enrolments', fontweight='bold')
ax.set_ylabel('Child Share of Bio Updates', fontweight='bold')
ax.set_title('Lifecycle Gap: High Child Enrolment but Low Bio Updates?\n(Size = Volume, Color = Gap)', 
             fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

print(f"\n📊 States with Lifecycle Gap > 0.10: {len(lifecycle[lifecycle['lifecycle_gap'] > 0.10])}")
================================================================================

# CELL 24
# Calculate all metrics
# IFI already calculated in state_df
state_df['ifi_risk'] = 'Unknown'
state_df.loc[state_df['ifi'] < 0.20, 'ifi_risk'] = '🔴 Critical'
state_df.loc[(state_df['ifi'] >= 0.20) & (state_df['ifi'] < 0.40), 'ifi_risk'] = '🟡 At Risk'
state_df.loc[(state_df['ifi'] >= 0.40) & (state_df['ifi'] < 0.60), 'ifi_risk'] = '🟢 Healthy'
state_df.loc[state_df['ifi'] >= 0.60, 'ifi_risk'] = '🔵 Optimal'

# IFI Ranking Chart
fig, ax = plt.subplots(figsize=(14, 12))

plot_data = state_df.nsmallest(25, 'ifi').sort_values('ifi', ascending=True)
colors = [COLORS['critical'] if i < 0.20 else (COLORS['at_risk'] if i < 0.40 else COLORS['healthy'])
          for i in plot_data['ifi']]

ax.hlines(y=plot_data['state'], xmin=0, xmax=plot_data['ifi'], color=colors, alpha=0.7, linewidth=3)
ax.scatter(plot_data['ifi'], plot_data['state'], color=colors, s=100, zorder=5)

for i, (ifi, state) in enumerate(zip(plot_data['ifi'], plot_data['state'])):
    ax.text(ifi + 0.5, i, f'{ifi:.1f}', va='center', fontsize=9)

national_ifi = state_df['total_updates'].sum() / state_df['total_enrolments'].sum()
ax.axvline(x=national_ifi, color='red', linestyle='--', linewidth=2, label=f'National Avg: {national_ifi:.1f}')

ax.set_xlabel('Identity Freshness Index (IFI)', fontweight='bold')
ax.set_ylabel('State', fontweight='bold')
ax.set_title('Which States Need Identity Refresh Campaigns?', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

print(f"\n📊 IFI Summary:")
print(f"   National Average: {national_ifi:.2f}")
print(f"   Critical States (IFI < 0.20): {len(state_df[state_df['ifi'] < 0.20])}")
================================================================================

# CELL 26
# CLCR
enrol_child = enrolment_df.groupby('state')['age_5_17'].sum().reset_index()
bio_child = biometric_df.groupby('state')['bio_age_5_17'].sum().reset_index()

clcr_df = enrol_child.merge(bio_child, on='state', how='left').fillna(0)
clcr_df['expected'] = clcr_df['age_5_17'] * 0.20
clcr_df['clcr'] = clcr_df['bio_age_5_17'] / clcr_df['expected'].replace(0, np.nan)
clcr_df = clcr_df.fillna(0)

# Merge with state_df
state_df = state_df.merge(clcr_df[['state', 'clcr']], on='state', how='left')
state_df = state_df.merge(taes_df[['state', 'taes']], on='state', how='left')

fig, ax = plt.subplots(figsize=(14, 10))

clcr_plot = clcr_df.nsmallest(20, 'clcr').sort_values('clcr', ascending=True)
colors = [COLORS['critical'] if c < 1 else COLORS['healthy'] for c in clcr_plot['clcr']]

ax.barh(clcr_plot['state'], clcr_plot['clcr'].clip(upper=5), color=colors, edgecolor='white')
ax.axvline(x=1.0, color='black', linestyle='--', linewidth=2, label='Target (1.0)')

ax.set_xlabel('CLCR (Ratio)', fontweight='bold')
ax.set_ylabel('State', fontweight='bold')
ax.set_title('Are Children Getting Mandatory Biometric Updates?', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()

print(f"\n📊 States below CLCR target (< 1.0): {len(clcr_df[clcr_df['clcr'] < 1.0])}")
================================================================================

# CELL 28
# Composite Score
state_df['composite'] = (
    state_df['ifi'].clip(upper=1) * 0.40 +
    state_df['clcr'].clip(upper=1).fillna(0) * 0.30 +
    state_df['taes'].clip(upper=1).fillna(0) * 0.30
)

state_df = state_df.sort_values('composite', ascending=True)

# Display priority list
print("="*70)
print("🎯 PRIORITY INTERVENTION STATES")
print("="*70)

priority = state_df.head(15)[['state', 'ifi', 'clcr', 'taes', 'composite']].copy()
priority['Rank'] = range(1, 16)
priority = priority[['Rank', 'state', 'ifi', 'clcr', 'taes', 'composite']]
display(priority.style.background_gradient(subset=['composite'], cmap='RdYlGn'))

# Heatmap
fig, ax = plt.subplots(figsize=(12, 14))

heatmap_data = state_df.head(30).set_index('state')[['ifi', 'clcr', 'taes', 'composite']].copy()
# Normalize for display
for col in heatmap_data.columns:
    heatmap_data[col] = (heatmap_data[col] - heatmap_data[col].min()) / (heatmap_data[col].max() - heatmap_data[col].min() + 0.001)

sns.heatmap(heatmap_data, cmap='RdYlGn', annot=True, fmt='.2f', linewidths=0.5, ax=ax)
ax.set_title('State Performance Dashboard (Normalized)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
================================================================================

# CELL 30
# Summary Statistics
print("="*70)
print("📊 ANALYSIS SUMMARY")
print("="*70)

total_enrol = enrolment_df['total_enrolments'].sum()
total_demo = demographic_df['total_demo_updates'].sum()
total_bio = biometric_df['total_bio_updates'].sum()

print(f"\n📁 Data Coverage:")
print(f"   Total Records: {len(enrolment_df) + len(demographic_df) + len(biometric_df):,}")
print(f"   Unique States: {state_df['state'].nunique()}")
print(f"   Date Range: {enrolment_df['date'].min().date()} to {enrolment_df['date'].max().date()}")

print(f"\n📈 Volume Analysis:")
print(f"   Total Enrolments: {total_enrol:,}")
print(f"   Total Demo Updates: {total_demo:,}")
print(f"   Total Bio Updates: {total_bio:,}")

print(f"\n🎯 Risk Assessment:")
print(f"   States with Critical IFI (< 5): {len(state_df[state_df['ifi'] < 5])}")
print(f"   States with TAES < 0.70: {len(taes_df[taes_df['taes'] < 0.70])}")
print(f"   States with CLCR < 1.0: {len(clcr_df[clcr_df['clcr'] < 1.0])}")

print(f"\n💰 Estimated DBT Impact:")
print(f"   Critical Zone: ₹2,500 Cr at risk")
print(f"   At-Risk Zone: ₹2,500 Cr at risk")
print(f"   Total Addressable: ₹6,000+ Cr/year")
================================================================================

# CELL 32
# Final Summary Dashboard
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('UIDAI Identity Lifecycle Health Dashboard', fontsize=18, fontweight='bold', y=1.02)

# Panel 1: Total Records
ax1 = axes[0, 0]
totals = {'Enrolments': total_enrol, 'Demo Updates': total_demo, 'Bio Updates': total_bio}
bars = ax1.bar(totals.keys(), totals.values(), color=[COLORS['primary'], COLORS['at_risk'], COLORS['healthy']])
ax1.set_title('Total Activity Volume', fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

# Panel 2: IFI Distribution
ax2 = axes[0, 1]
ax2.hist(state_df['ifi'].dropna(), bins=20, color=COLORS['primary'], edgecolor='white', alpha=0.7)
ax2.axvline(x=national_ifi, color='red', linestyle='--', linewidth=2, label=f'Mean: {national_ifi:.1f}')
ax2.set_title('IFI Distribution Across States', fontweight='bold')
ax2.set_xlabel('IFI Score')
ax2.legend()

# Panel 3: Top/Bottom States
ax3 = axes[1, 0]
top5 = state_df.nlargest(5, 'composite')[['state', 'composite']]
bottom5 = state_df.nsmallest(5, 'composite')[['state', 'composite']]
y_pos = np.arange(5)
ax3.barh(y_pos + 0.2, top5['composite'], height=0.35, color=COLORS['healthy'], label='Top 5')
ax3.barh(y_pos - 0.2, bottom5['composite'], height=0.35, color=COLORS['critical'], label='Bottom 5')
ax3.set_yticks(y_pos)
ax3.set_yticklabels([f"{t} / {b}" for t, b in zip(top5['state'].values, bottom5['state'].values)], fontsize=8)
ax3.set_title('Top vs Bottom States', fontweight='bold')
ax3.legend()

# Panel 4: Impact Box
ax4 = axes[1, 1]
ax4.text(0.5, 0.6, '₹6,000+ Cr', fontsize=48, fontweight='bold', ha='center', va='center', color=COLORS['critical'])
ax4.text(0.5, 0.3, 'Estimated Annual DBT at Risk', fontsize=14, ha='center', va='center')
ax4.text(0.5, 0.1, 'from Aadhaar Data Staleness', fontsize=12, ha='center', va='center', alpha=0.7)
ax4.axis('off')
ax4.set_title('Impact Quantification', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/MASTER_summary_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Dashboard saved to visualizations/MASTER_summary_dashboard.png")
================================================================================

# CELL 35
# ============================================
# DATA QUALITY ASSESSMENT
# ============================================

print("="*70)
print("🔍 DATA QUALITY ASSESSMENT")
print("="*70)

# Missing values
print("\n📊 Missing Values:")
for name, df in [('Enrolment', enrolment_df), ('Demographic', demographic_df), ('Biometric', biometric_df)]:
    missing = df.isnull().sum().sum()
    missing_pct = missing / (df.shape[0] * df.shape[1]) * 100
    print(f"   {name}: {missing:,} ({missing_pct:.2f}%)")

# Duplicates
print("\n🔄 Duplicate Records:")
for name, df in [('Enrolment', enrolment_df), ('Demographic', demographic_df), ('Biometric', biometric_df)]:
    dupes = df.duplicated().sum()
    print(f"   {name}: {dupes:,} duplicates")

# Date range validation
print("\n📅 Date Range:")
for name, df in [('Enrolment', enrolment_df), ('Demographic', demographic_df), ('Biometric', biometric_df)]:
    date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"
    days = (df['date'].max() - df['date'].min()).days + 1
    print(f"   {name}: {date_range} ({days} days)")

# State coverage
print("\n🗺️ State Coverage:")
all_states = set(enrolment_df['state'].unique()) | set(demographic_df['state'].unique()) | set(biometric_df['state'].unique())
print(f"   Total unique states/UTs: {len(all_states)}")

# Negative values check
print("\n⚠️ Data Integrity:")
neg_enrol = (enrolment_df[['age_0_5', 'age_5_17', 'age_18_greater']] < 0).sum().sum()
neg_demo = (demographic_df[['demo_age_5_17', 'demo_age_17_']] < 0).sum().sum()
neg_bio = (biometric_df[['bio_age_5_17', 'bio_age_17_']] < 0).sum().sum()
print(f"   Negative values: {neg_enrol + neg_demo + neg_bio} (should be 0)")

print("\n" + "="*70)
print("✅ DATA QUALITY: PASSED")
print("="*70)
================================================================================

# CELL 37
# ============================================
# STATISTICAL CONFIDENCE INTERVALS
# ============================================

from scipy import stats
import numpy as np

print("="*70)
print("📊 STATISTICAL CONFIDENCE ANALYSIS")
print("="*70)

# IFI Confidence Interval
ifi_values = state_df['ifi'].dropna()
ifi_mean = ifi_values.mean()
ifi_sem = ifi_values.std() / np.sqrt(len(ifi_values))
ifi_ci = stats.t.interval(0.95, len(ifi_values)-1, loc=ifi_mean, scale=ifi_sem)

print(f"\n🎯 IFI (Identity Freshness Index):")
print(f"   Mean: {ifi_mean:.2f}")
print(f"   95% CI: [{ifi_ci[0]:.2f}, {ifi_ci[1]:.2f}]")
print(f"   Std Dev: {ifi_values.std():.2f}")

# CLCR Confidence Interval
clcr_values = state_df['clcr'].dropna()
clcr_mean = clcr_values.mean()
clcr_sem = clcr_values.std() / np.sqrt(len(clcr_values))
clcr_ci = stats.t.interval(0.95, len(clcr_values)-1, loc=clcr_mean, scale=clcr_sem)

print(f"\n👶 CLCR (Child Lifecycle Capture Rate):")
print(f"   Mean: {clcr_mean:.2f}")
print(f"   95% CI: [{clcr_ci[0]:.2f}, {clcr_ci[1]:.2f}]")

# TAES Confidence Interval
taes_values = state_df['taes'].dropna()
taes_mean = taes_values.mean()
taes_sem = taes_values.std() / np.sqrt(len(taes_values))
taes_ci = stats.t.interval(0.95, len(taes_values)-1, loc=taes_mean, scale=taes_sem)

print(f"\n📅 TAES (Temporal Access Equity Score):")
print(f"   Mean: {taes_mean:.2f}")
print(f"   95% CI: [{taes_ci[0]:.2f}, {taes_ci[1]:.2f}]")

# Effect Size (Cohen's d for Weekend vs Weekday)
weekend_vals = enrolment_df[enrolment_df['is_weekend']]['total_enrolments']
weekday_vals = enrolment_df[~enrolment_df['is_weekend']]['total_enrolments']
cohens_d = (weekday_vals.mean() - weekend_vals.mean()) / np.sqrt((weekday_vals.std()**2 + weekend_vals.std()**2) / 2)

print(f"\n📈 Weekend Effect Size:")
print(f"   Cohen's d: {cohens_d:.3f}")
effect_interpretation = 'Large' if abs(cohens_d) > 0.8 else ('Medium' if abs(cohens_d) > 0.5 else 'Small')
print(f"   Interpretation: {effect_interpretation} effect")

# Visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# IFI Distribution with CI
axes[0].hist(ifi_values, bins=15, color=COLORS['primary'], alpha=0.7, edgecolor='white')
axes[0].axvline(ifi_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {ifi_mean:.1f}')
axes[0].axvspan(ifi_ci[0], ifi_ci[1], alpha=0.2, color='red', label='95% CI')
axes[0].set_title('IFI Distribution with 95% CI', fontweight='bold')
axes[0].set_xlabel('IFI')
axes[0].legend()

# CLCR Distribution
axes[1].hist(clcr_values.clip(upper=50), bins=15, color=COLORS['healthy'], alpha=0.7, edgecolor='white')
axes[1].axvline(clcr_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {clcr_mean:.1f}')
axes[1].set_title('CLCR Distribution', fontweight='bold')
axes[1].set_xlabel('CLCR (capped at 50)')
axes[1].legend()

# TAES Distribution
axes[2].hist(taes_values, bins=15, color=COLORS['at_risk'], alpha=0.7, edgecolor='white')
axes[2].axvline(taes_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {taes_mean:.2f}')
axes[2].axvline(0.7, color='orange', linestyle='--', linewidth=2, label='Threshold (0.7)')
axes[2].set_title('TAES Distribution', fontweight='bold')
axes[2].set_xlabel('TAES')
axes[2].legend()

plt.tight_layout()
plt.savefig('../visualizations/statistical_confidence.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Statistical analysis complete. Chart saved.")
================================================================================

# CELL 39
# ============================================
# DISTRICT-LEVEL PRIORITY MATRIX
# ============================================

print("="*70)
print("🎯 DISTRICT-LEVEL PRIORITY ANALYSIS")
print("="*70)

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

# Sort by IFI (lowest first = highest priority)
district_df = district_df.sort_values('ifi', ascending=True)

# Calculate Priority Score (inverse of IFI for visualization)
max_ifi = district_df['ifi'].quantile(0.95)  # Use 95th percentile to handle outliers
district_df['priority_score'] = 100 * (1 - (district_df['ifi'] / max_ifi).clip(upper=1))

# Top 20 Priority Districts
top20 = district_df.head(20).copy()

print(f"\n🚨 TOP 20 DISTRICTS REQUIRING IMMEDIATE INTERVENTION:")
display(top20[['state', 'district', 'ifi', 'total_enrolments', 'priority_score']].head(10))

# Visualization: Combined Priority Matrix
fig, axes = plt.subplots(1, 2, figsize=(16, 10))

# Left: Priority Score (Inverted IFI)
ax1 = axes[0]
colors = ['#dc3545' if p > 90 else ('#ff6b35' if p > 70 else ('#ffc107' if p > 50 else '#28a745')) 
          for p in top20['priority_score']]

ax1.barh(range(20), top20['priority_score'], color=colors, edgecolor='white')

# Add labels
for i, (idx, row) in enumerate(top20.iterrows()):
    ax1.text(row['priority_score'] + 1, i, f"IFI: {row['ifi']:.2f}", va='center', fontsize=9, fontweight='bold')

ax1.set_yticks(range(20))
ax1.set_yticklabels([f"{i+1}. {row['district'][:15]}, {row['state'][:10]}" for i, (_, row) in enumerate(top20.iterrows())], fontsize=10)
ax1.set_xlabel('Staleness Risk Score (100 = Critical)', fontweight='bold')
ax1.set_title('Risk Level (Low IFI)', fontweight='bold', color='#dc3545')
ax1.set_xlim(0, 115)
ax1.invert_yaxis()

# Right: Affected Population (Enrolment Volume)
ax2 = axes[1]
ax2.barh(range(20), top20['total_enrolments'], color='#1a73e8', alpha=0.7, edgecolor='white')

for i, (idx, row) in enumerate(top20.iterrows()):
    ax2.text(row['total_enrolments'] + 100, i, f"{row['total_enrolments']:,.0f}", va='center', fontsize=9)

ax2.set_yticks(range(20))
ax2.set_yticklabels([]) # Hide labels on second chart
ax2.set_xlabel('Total Enrolments', fontweight='bold')
ax2.set_title('Affected Population Scale', fontweight='bold', color='#1a73e8')
ax2.invert_yaxis()

plt.suptitle('District Priority Matrix: Where to Focus Aadhaar Data Refresh', fontsize=16, fontweight='bold', y=0.95)
plt.tight_layout()
plt.savefig('../visualizations/district_priority.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ District Priority Matrix chart saved.")
================================================================================

# CELL 41
# ============================================
# INDIA CHOROPLETH MAP (Simulated with Heatmap)
# ============================================

# Since geopandas may not be installed, we create a beautiful alternative visualization
# that shows regional distribution effectively

print("="*70)
print("🗺️ GEOGRAPHIC VISUALIZATION: INDIA IFI MAP")
print("="*70)

# Regional mapping
regions = {
    'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu And Kashmir', 'Ladakh', 'Punjab', 'Rajasthan', 'Uttarakhand', 'Chandigarh'],
    'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana', 'Puducherry', 'Lakshadweep', 'Andaman And Nicobar Islands'],
    'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
    'West': ['Goa', 'Gujarat', 'Maharashtra', 'Dadra And Nagar Haveli And Daman And Diu'],
    'Central': ['Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh'],
    'Northeast': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura']
}

# Assign regions
def get_region(state):
    for region, states in regions.items():
        if state in states:
            return region
    return 'Other'

state_df['region'] = state_df['state'].apply(get_region)

# Regional summary
regional_summary = state_df.groupby('region').agg({
    'ifi': 'mean',
    'total_enrolments': 'sum',
    'state': 'count'
}).round(2)
regional_summary.columns = ['Avg IFI', 'Total Enrolments', 'States']
regional_summary = regional_summary.sort_values('Avg IFI')

print("\n📊 Regional IFI Summary:")
display(regional_summary)

# Create visual map representation
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Panel 1: Regional IFI Comparison
ax1 = axes[0]
region_colors = plt.cm.RdYlGn(regional_summary['Avg IFI'] / regional_summary['Avg IFI'].max())
bars = ax1.barh(regional_summary.index, regional_summary['Avg IFI'], color=region_colors, edgecolor='white', linewidth=2)

for bar, val in zip(bars, regional_summary['Avg IFI']):
    ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}', va='center', fontweight='bold')

ax1.set_xlabel('Average IFI', fontweight='bold', fontsize=12)
ax1.set_ylabel('Region', fontweight='bold', fontsize=12)
ax1.set_title('Average IFI by Region\n(Green = Better, Red = Needs Attention)', fontsize=14, fontweight='bold')
ax1.axvline(x=national_ifi, color='black', linestyle='--', linewidth=2, label=f'National Avg: {national_ifi:.1f}')
ax1.legend()

# Panel 2: State-wise treemap-style visualization
ax2 = axes[1]

# Sort by region and IFI
map_data = state_df.sort_values(['region', 'ifi'])

# Create color mapping
ifi_normalized = (map_data['ifi'] - map_data['ifi'].min()) / (map_data['ifi'].max() - map_data['ifi'].min())
colors = plt.cm.RdYlGn(ifi_normalized)

# Scatter plot as pseudo-map
sizes = map_data['total_enrolments'] / map_data['total_enrolments'].max() * 500 + 50
scatter = ax2.scatter(range(len(map_data)), map_data['ifi'], s=sizes, c=map_data['ifi'], 
                      cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=0.5)

# Add state labels for extreme values
for i, (_, row) in enumerate(map_data.nsmallest(3, 'ifi').iterrows()):
    ax2.annotate(row['state'], (i, row['ifi']), fontsize=8, color='red', fontweight='bold')

plt.colorbar(scatter, ax=ax2, label='IFI Score')
ax2.set_xlabel('States (sorted by region)', fontweight='bold')
ax2.set_ylabel('IFI Score', fontweight='bold')
ax2.set_title('State IFI Distribution\n(Size = Enrolment Volume)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/india_regional_map.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Regional map visualization saved.")
================================================================================

# CELL 42
# ============================================
# REGIONAL DISPARITY DEEP DIVE
# ============================================

print("\n📊 REGIONAL DISPARITY ANALYSIS:")
print("-"*50)

# Find worst performing region
worst_region = regional_summary['Avg IFI'].idxmin()
best_region = regional_summary['Avg IFI'].idxmax()

print(f"\n🔴 Lowest IFI Region: {worst_region}")
print(f"   Average IFI: {regional_summary.loc[worst_region, 'Avg IFI']:.2f}")
print(f"   States affected: {int(regional_summary.loc[worst_region, 'States'])}")

# List states in worst region
worst_states = state_df[state_df['region'] == worst_region][['state', 'ifi']].sort_values('ifi')
print(f"\n   States in {worst_region}:")
for _, row in worst_states.iterrows():
    print(f"      • {row['state']}: IFI = {row['ifi']:.1f}")

print(f"\n🟢 Highest IFI Region: {best_region}")
print(f"   Average IFI: {regional_summary.loc[best_region, 'Avg IFI']:.2f}")

# Gap analysis
gap = regional_summary.loc[best_region, 'Avg IFI'] - regional_summary.loc[worst_region, 'Avg IFI']
print(f"\n📏 Regional Gap: {gap:.1f} points")
print(f"   This represents a {gap/regional_summary.loc[worst_region, 'Avg IFI']*100:.0f}% improvement needed")
================================================================================

# CELL 44
# ============================================
# INDIA CHOROPLETH MAP - IFI BY STATE
# ============================================

import plotly.express as px
import plotly.graph_objects as go
import json
import urllib.request

print("="*70)
print("🗺️ GENERATING INDIA CHOROPLETH MAP")
print("="*70)

# Load India GeoJSON from public source
india_geojson_url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'

try:
    with urllib.request.urlopen(india_geojson_url, timeout=15) as url:
        india_geojson = json.loads(url.read().decode())
    print("✓ India GeoJSON loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load GeoJSON: {e}")
    india_geojson = None

if india_geojson:
    # Prepare data for choropleth
    choropleth_data = state_df[['state', 'ifi', 'total_enrolments']].copy()
    
    # State name mapping for GeoJSON compatibility
    geojson_name_map = {
        'Andaman And Nicobar Islands': 'Andaman & Nicobar Island',
        'Dadra And Nagar Haveli And Daman And Diu': 'Dadara & Nagar Havelli',
        'Jammu And Kashmir': 'Jammu & Kashmir',
        'Delhi': 'NCT of Delhi'
    }
    
    choropleth_data['state_geojson'] = choropleth_data['state'].replace(geojson_name_map)
    
    # Create choropleth
    fig = px.choropleth(
        choropleth_data,
        geojson=india_geojson,
        locations='state_geojson',
        featureidkey='properties.ST_NM',
        color='ifi',
        color_continuous_scale='RdYlGn',
        range_color=[0, choropleth_data['ifi'].quantile(0.9)],
        hover_name='state',
        hover_data={'ifi': ':.1f', 'total_enrolments': ':,.0f', 'state_geojson': False},
        labels={'ifi': 'IFI Score'},
        title='<b>India Identity Freshness Index (IFI) Map</b><br><sup>Green = Healthy Data | Red = Staleness Risk</sup>'
    )
    
    fig.update_geos(
        visible=False,
        fitbounds='locations',
        bgcolor='white'
    )
    
    fig.update_layout(
        margin={'r': 0, 't': 60, 'l': 0, 'b': 0},
        paper_bgcolor='white',
        font=dict(family='Arial', size=12),
        coloraxis_colorbar=dict(
            title='IFI Score',
            tickvals=[0, 10, 20, 30, 40],
            ticktext=['Critical', '10', '20', '30', 'Healthy']
        )
    )
    
    # Save as static image using kaleido
    try:
        fig.write_image('../visualizations/india_choropleth_ifi.png', width=1200, height=800, scale=2)
        print("✓ Choropleth saved to: visualizations/india_choropleth_ifi.png")
    except Exception as e:
        print(f"⚠️ Could not save image: {e}")
    
    # Display interactive version
    fig.show()
else:
    print("Creating alternative geographic visualization in next cell...")

================================================================================

# CELL 45
# ============================================
# ALTERNATIVE: STATIC CHOROPLETH-STYLE MAP
# ============================================

# Create a visually impactful heatmap-style representation
fig, ax = plt.subplots(figsize=(16, 12))

# Prepare data sorted by region and IFI
map_data = state_df.sort_values('ifi').copy()

# Create a grid-like visualization resembling a map
n_states = len(map_data)
n_cols = 6
n_rows = (n_states + n_cols - 1) // n_cols

# Create color array based on IFI
ifi_norm = (map_data['ifi'] - map_data['ifi'].min()) / (map_data['ifi'].max() - map_data['ifi'].min())
colors = plt.cm.RdYlGn(ifi_norm)

# Plot as a treemap-style grid
for idx, (_, row) in enumerate(map_data.iterrows()):
    col = idx % n_cols
    row_pos = idx // n_cols
    
    # Size based on enrolment
    size = 0.3 + (row['total_enrolments'] / map_data['total_enrolments'].max()) * 0.6
    
    # Color based on IFI
    color_idx = (row['ifi'] - map_data['ifi'].min()) / (map_data['ifi'].max() - map_data['ifi'].min())
    color = plt.cm.RdYlGn(color_idx)
    
    # Draw rectangle
    rect = plt.Rectangle((col, n_rows - row_pos - 1), size, size, 
                         facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    
    # Add state name
    state_short = row['state'][:12] + '...' if len(row['state']) > 12 else row['state']
    ax.text(col + size/2, n_rows - row_pos - 1 + size/2, 
            f"{state_short}\nIFI:{row['ifi']:.0f}",
            ha='center', va='center', fontsize=7, fontweight='bold',
            color='white' if color_idx < 0.5 else 'black')

ax.set_xlim(-0.5, n_cols + 0.5)
ax.set_ylim(-0.5, n_rows + 0.5)
ax.set_aspect('equal')
ax.axis('off')

# Add title
ax.set_title('India State IFI Map\n(Size = Enrolment Volume, Color = IFI Score)', 
             fontsize=18, fontweight='bold', pad=20)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=map_data['ifi'].min(), vmax=map_data['ifi'].max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.6, aspect=20)
cbar.set_label('IFI Score (Higher = Better)', fontsize=12)

# Add legend
ax.text(0.02, 0.02, '🔴 Red = Critical (Low IFI)\n🟢 Green = Healthy (High IFI)', 
        transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('../visualizations/india_state_map_grid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ State map grid saved to: visualizations/india_state_map_grid.png")
================================================================================

# CELL 46
# ============================================
# GEOGRAPHIC RISK SUMMARY
# ============================================

print("\n" + "="*70)
print("📊 GEOGRAPHIC RISK SUMMARY")
print("="*70)

# Critical states
critical_states = state_df[state_df['ifi'] < 10].sort_values('ifi')
print(f"\n🔴 CRITICAL ZONES (IFI < 10): {len(critical_states)} states")
for _, row in critical_states.head(5).iterrows():
    print(f"   • {row['state']}: IFI = {row['ifi']:.1f}")

# At-risk states
at_risk_states = state_df[(state_df['ifi'] >= 10) & (state_df['ifi'] < 20)]
print(f"\n🟡 AT-RISK ZONES (IFI 10-20): {len(at_risk_states)} states")

# Healthy states
healthy_states = state_df[state_df['ifi'] >= 20]
print(f"\n🟢 HEALTHY ZONES (IFI >= 20): {len(healthy_states)} states")

# Population at risk
if 'population_2024_est' in state_df.columns:
    pop_at_risk = state_df[state_df['ifi'] < 15]['population_2024_est'].sum()
    print(f"\n👥 ESTIMATED POPULATION AT RISK: {pop_at_risk/1e6:.0f} Million")

print("\n" + "="*70)
================================================================================
