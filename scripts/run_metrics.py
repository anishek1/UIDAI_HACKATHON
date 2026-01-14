"""
UIDAI Metrics Execution Script
==============================
Runs all 5 engineered metrics and generates state rankings.
Demonstrates how to use config.yaml for parameters.
"""

import sys
sys.path.insert(0, r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

import pandas as pd
import numpy as np
import yaml
from pathlib import Path

# Load configuration from config.yaml
# This is how you use config.yaml - load once, use everywhere
with open(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("=" * 60)
print("📊 UIDAI METRICS EXECUTION")
print("=" * 60)
print(f"\nUsing config.yaml for:")
print(f"  • IFI Critical Threshold: {config['analysis']['ifi_bands']['critical']}")
print(f"  • Expected Child Update Rate: {config['analysis']['expected_child_update_rate']}")
print(f"  • TAES Acceptable: {config['analysis']['taes_acceptable']}")
print()

# Load all datasets
print("📁 Loading datasets...")

# Enrolment
enrol_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Enrolment')
enrol_files = list(enrol_path.glob('*.csv'))
enrol_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in enrol_files]
enrolment_df = pd.concat(enrol_dfs, ignore_index=True)
print(f"  ✓ Enrolment: {len(enrolment_df):,} rows")

# Demographic
demo_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Demographic')
demo_files = list(demo_path.glob('*.csv'))
demo_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in demo_files]
demographic_df = pd.concat(demo_dfs, ignore_index=True)
print(f"  ✓ Demographic: {len(demographic_df):,} rows")

# Biometric
bio_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Biometric')
bio_files = list(bio_path.glob('*.csv'))
bio_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in bio_files]
biometric_df = pd.concat(bio_dfs, ignore_index=True)
print(f"  ✓ Biometric: {len(biometric_df):,} rows")

# Population
population_df = pd.read_csv(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\external\state_population.csv')
print(f"  ✓ Population: {len(population_df)} states")

# Preprocess
enrolment_df['date'] = pd.to_datetime(enrolment_df['date'], format='%d-%m-%Y', errors='coerce')
demographic_df['date'] = pd.to_datetime(demographic_df['date'], format='%d-%m-%Y', errors='coerce')
biometric_df['date'] = pd.to_datetime(biometric_df['date'], format='%d-%m-%Y', errors='coerce')

# Add totals
enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

# Add weekend flag for TAES
enrolment_df['is_weekend'] = enrolment_df['date'].dt.dayofweek >= 5
enrolment_df['weekday'] = enrolment_df['date'].dt.day_name()

print("\n" + "=" * 60)
print("📈 METRIC 1: IDENTITY FRESHNESS INDEX (IFI)")
print("=" * 60)

# Calculate IFI by state
enrol_state = enrolment_df.groupby('state')['total_enrolments'].sum().reset_index()
demo_state = demographic_df.groupby('state')['total_demo_updates'].sum().reset_index()
bio_state = biometric_df.groupby('state')['total_bio_updates'].sum().reset_index()

ifi_df = enrol_state.merge(demo_state, on='state', how='left')
ifi_df = ifi_df.merge(bio_state, on='state', how='left')
ifi_df = ifi_df.fillna(0)

ifi_df['total_updates'] = ifi_df['total_demo_updates'] + ifi_df['total_bio_updates']
ifi_df['ifi'] = ifi_df['total_updates'] / ifi_df['total_enrolments']

# Categorize using config thresholds
ifi_df['ifi_risk'] = pd.cut(
    ifi_df['ifi'],
    bins=[-np.inf, config['analysis']['ifi_bands']['critical'], 
          config['analysis']['ifi_bands']['at_risk'], 
          config['analysis']['ifi_bands']['healthy'], np.inf],
    labels=['🔴 Critical', '🟡 At Risk', '🟢 Healthy', '🔵 Optimal']
)

ifi_df = ifi_df.sort_values('ifi', ascending=True)

print("\n🚨 BOTTOM 10 STATES (Highest Staleness Risk):")
print("-" * 50)
bottom_10 = ifi_df.head(10)[['state', 'ifi', 'ifi_risk', 'total_enrolments', 'total_updates']]
for _, row in bottom_10.iterrows():
    print(f"  {row['ifi_risk']} {row['state']}: IFI = {row['ifi']:.3f}")

print("\n✅ TOP 10 STATES (Freshest Data):")
print("-" * 50)
top_10 = ifi_df.tail(10)[['state', 'ifi', 'ifi_risk']].iloc[::-1]
for _, row in top_10.iterrows():
    print(f"  {row['ifi_risk']} {row['state']}: IFI = {row['ifi']:.3f}")

# National average
national_ifi = ifi_df['total_updates'].sum() / ifi_df['total_enrolments'].sum()
print(f"\n📊 National Average IFI: {national_ifi:.3f}")

print("\n" + "=" * 60)
print("👶 METRIC 2: CHILD LIFECYCLE CAPTURE RATE (CLCR)")
print("=" * 60)

enrol_child = enrolment_df.groupby('state')['age_5_17'].sum().reset_index()
bio_child = biometric_df.groupby('state')['bio_age_5_17'].sum().reset_index()

clcr_df = enrol_child.merge(bio_child, on='state', how='left')
clcr_df = clcr_df.fillna(0)

expected_rate = config['analysis']['expected_child_update_rate']
clcr_df['expected_updates'] = clcr_df['age_5_17'] * expected_rate
clcr_df['clcr'] = clcr_df['bio_age_5_17'] / clcr_df['expected_updates'].replace(0, np.nan)
clcr_df = clcr_df.fillna(0)

clcr_df['clcr_status'] = pd.cut(
    clcr_df['clcr'],
    bins=[-np.inf, 0.50, 0.80, 1.00, np.inf],
    labels=['🔴 Critical Gap', '🟡 Below Target', '🟢 On Track', '🔵 Exceeding']
)

clcr_df = clcr_df.sort_values('clcr', ascending=True)

print("\n🚨 STATES WITH CHILD LIFECYCLE GAPS:")
print("-" * 50)
child_gaps = clcr_df[clcr_df['clcr'] < 0.80].head(10)
for _, row in child_gaps.iterrows():
    print(f"  {row['clcr_status']} {row['state']}: CLCR = {row['clcr']:.2f}")

print("\n" + "=" * 60)
print("📅 METRIC 3: TEMPORAL ACCESS EQUITY SCORE (TAES)")
print("=" * 60)

daily_enrol = enrolment_df.groupby(['state', 'date', 'is_weekend'])['total_enrolments'].sum().reset_index()

weekend_avg = daily_enrol[daily_enrol['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekend_avg.columns = ['state', 'weekend_avg']

weekday_avg = daily_enrol[~daily_enrol['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekday_avg.columns = ['state', 'weekday_avg']

taes_df = weekend_avg.merge(weekday_avg, on='state', how='outer').fillna(0)
taes_df['taes'] = taes_df['weekend_avg'] / taes_df['weekday_avg'].replace(0, np.nan)
taes_df['taes'] = taes_df['taes'].fillna(0).clip(upper=1.5)

taes_df['taes_status'] = pd.cut(
    taes_df['taes'],
    bins=[-np.inf, 0.50, config['analysis']['taes_acceptable'], 0.90, np.inf],
    labels=['🔴 Severe', '🟡 Moderate', '🟢 Acceptable', '🔵 Equitable']
)

taes_df = taes_df.sort_values('taes', ascending=True)

print("\n🚨 STATES WITH WEEKEND ACCESS INEQUITY:")
print("-" * 50)
inequity = taes_df[taes_df['taes'] < config['analysis']['taes_acceptable']].head(10)
for _, row in inequity.iterrows():
    pct_drop = (1 - row['taes']) * 100
    print(f"  {row['taes_status']} {row['state']}: TAES = {row['taes']:.2f} ({pct_drop:.0f}% weekend drop)")

national_taes = taes_df['weekend_avg'].sum() / taes_df['weekday_avg'].sum()
print(f"\n📊 National TAES: {national_taes:.2f} ({(1-national_taes)*100:.0f}% weekend drop)")

print("\n" + "=" * 60)
print("🎯 COMPOSITE STATE RANKINGS")
print("=" * 60)

# Merge all metrics
composite = ifi_df[['state', 'ifi', 'ifi_risk', 'total_enrolments']].copy()
composite = composite.merge(clcr_df[['state', 'clcr', 'clcr_status']], on='state', how='left')
composite = composite.merge(taes_df[['state', 'taes', 'taes_status']], on='state', how='left')
composite = composite.fillna(0)

# Calculate composite score (higher = better)
composite['composite'] = (
    composite['ifi'].clip(upper=1) * 0.40 +
    composite['clcr'].clip(upper=1) * 0.30 +
    composite['taes'].clip(upper=1) * 0.30
)

composite = composite.sort_values('composite', ascending=True)

print("\n🚨 PRIORITY INTERVENTION STATES (Lowest Composite):")
print("-" * 60)
for i, (_, row) in enumerate(composite.head(15).iterrows(), 1):
    print(f"  {i:2}. {row['state']:<25} Score: {row['composite']:.3f}  |  IFI: {row['ifi']:.2f}  CLCR: {row['clcr']:.2f}  TAES: {row['taes']:.2f}")

print("\n" + "=" * 60)
print("📊 SUMMARY STATISTICS")
print("=" * 60)
print(f"\nTotal Records Analyzed: {len(enrolment_df) + len(demographic_df) + len(biometric_df):,}")
print(f"Total Enrolments: {enrolment_df['total_enrolments'].sum():,}")
print(f"Total Demo Updates: {demographic_df['total_demo_updates'].sum():,}")
print(f"Total Bio Updates: {biometric_df['total_bio_updates'].sum():,}")
print(f"\nStates in Critical IFI Zone: {len(ifi_df[ifi_df['ifi'] < config['analysis']['ifi_bands']['critical']])}")
print(f"States with CLCR Gap: {len(clcr_df[clcr_df['clcr'] < 0.80])}")
print(f"States with Weekend Inequity: {len(taes_df[taes_df['taes'] < config['analysis']['taes_acceptable']])}")

# Save results
composite.to_csv(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\processed\state_metrics.csv', index=False)
print(f"\n✅ Results saved to: data/processed/state_metrics.csv")

print("\n" + "=" * 60)
print("🏁 EXECUTION COMPLETE")
print("=" * 60)
