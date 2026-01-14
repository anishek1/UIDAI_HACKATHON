"""
Execute Analysis Script
=======================
Runs the complete analysis with state name cleaning.
"""

import sys
sys.path.insert(0, r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import state mapping
from src.state_mapping import standardize_dataframe_states

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100

# Load config
with open(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("="*70)
print("UIDAI IDENTITY LIFECYCLE HEALTH ANALYSIS")
print("="*70)

# ============================================
# 1. LOAD DATA
# ============================================
print("\n[1/6] Loading datasets...")

enrol_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Enrolment')
enrol_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in enrol_path.glob('*.csv')]
enrolment_df = pd.concat(enrol_dfs, ignore_index=True)

demo_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Demographic')
demo_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in demo_path.glob('*.csv')]
demographic_df = pd.concat(demo_dfs, ignore_index=True)

bio_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\raw\Biometric')
bio_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in bio_path.glob('*.csv')]
biometric_df = pd.concat(bio_dfs, ignore_index=True)

population_df = pd.read_csv(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\external\state_population.csv')

print(f"   Enrolment: {len(enrolment_df):,} rows")
print(f"   Demographic: {len(demographic_df):,} rows")
print(f"   Biometric: {len(biometric_df):,} rows")
print(f"   Total: {len(enrolment_df) + len(demographic_df) + len(biometric_df):,} rows")

# ============================================
# 2. CLEAN STATE NAMES
# ============================================
print("\n[2/6] Standardizing state names...")

enrolment_df = standardize_dataframe_states(enrolment_df, 'state')
demographic_df = standardize_dataframe_states(demographic_df, 'state')
biometric_df = standardize_dataframe_states(biometric_df, 'state')

print(f"   Unique states after cleaning: {enrolment_df['state'].nunique()}")

# ============================================
# 3. PREPROCESS
# ============================================
print("\n[3/6] Preprocessing...")

enrolment_df['date'] = pd.to_datetime(enrolment_df['date'], format='%d-%m-%Y', errors='coerce')
demographic_df['date'] = pd.to_datetime(demographic_df['date'], format='%d-%m-%Y', errors='coerce')
biometric_df['date'] = pd.to_datetime(biometric_df['date'], format='%d-%m-%Y', errors='coerce')

enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

enrolment_df['is_weekend'] = enrolment_df['date'].dt.dayofweek >= 5

print(f"   Date range: {enrolment_df['date'].min().date()} to {enrolment_df['date'].max().date()}")

# ============================================
# 4. CALCULATE METRICS
# ============================================
print("\n[4/6] Calculating metrics...")

# IFI
enrol_state = enrolment_df.groupby('state')['total_enrolments'].sum().reset_index()
demo_state = demographic_df.groupby('state')['total_demo_updates'].sum().reset_index()
bio_state = biometric_df.groupby('state')['total_bio_updates'].sum().reset_index()

ifi_df = enrol_state.merge(demo_state, on='state', how='left')
ifi_df = ifi_df.merge(bio_state, on='state', how='left').fillna(0)
ifi_df['total_updates'] = ifi_df['total_demo_updates'] + ifi_df['total_bio_updates']
ifi_df['ifi'] = ifi_df['total_updates'] / ifi_df['total_enrolments'].replace(0, np.nan)
ifi_df['ifi'] = ifi_df['ifi'].fillna(0)

# CLCR
enrol_child = enrolment_df.groupby('state')['age_5_17'].sum().reset_index()
bio_child = biometric_df.groupby('state')['bio_age_5_17'].sum().reset_index()
clcr_df = enrol_child.merge(bio_child, on='state', how='left').fillna(0)
clcr_df['clcr'] = clcr_df['bio_age_5_17'] / (clcr_df['age_5_17'] * 0.20).replace(0, np.nan)
clcr_df['clcr'] = clcr_df['clcr'].fillna(0)

# TAES
daily_enrol = enrolment_df.groupby(['state', 'date', 'is_weekend'])['total_enrolments'].sum().reset_index()
weekend_avg = daily_enrol[daily_enrol['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekend_avg.columns = ['state', 'weekend_avg']
weekday_avg = daily_enrol[~daily_enrol['is_weekend']].groupby('state')['total_enrolments'].mean().reset_index()
weekday_avg.columns = ['state', 'weekday_avg']
taes_df = weekend_avg.merge(weekday_avg, on='state', how='outer').fillna(0)
taes_df['taes'] = taes_df['weekend_avg'] / taes_df['weekday_avg'].replace(0, np.nan)
taes_df['taes'] = taes_df['taes'].fillna(0).clip(upper=1.5)

# National averages
national_ifi = ifi_df['total_updates'].sum() / ifi_df['total_enrolments'].sum()
national_taes = taes_df['weekend_avg'].sum() / taes_df['weekday_avg'].sum()

print(f"   National IFI: {national_ifi:.2f}")
print(f"   National TAES: {national_taes:.2f} ({(1-national_taes)*100:.0f}% weekend drop)")

# ============================================
# 5. COMPOSITE RANKINGS
# ============================================
print("\n[5/6] Computing composite rankings...")

composite = ifi_df[['state', 'ifi', 'total_enrolments']].copy()
composite = composite.merge(clcr_df[['state', 'clcr']], on='state', how='left')
composite = composite.merge(taes_df[['state', 'taes']], on='state', how='left').fillna(0)

composite['composite'] = (
    composite['ifi'].clip(upper=1) * 0.40 +
    composite['clcr'].clip(upper=1) * 0.30 +
    composite['taes'].clip(upper=1) * 0.30
)

composite = composite.sort_values('composite', ascending=True)

# Merge population
composite = composite.merge(population_df[['state', 'population_2024_est']], on='state', how='left')

# ============================================
# 6. OUTPUT RESULTS
# ============================================
print("\n[6/6] Saving results...")

composite.to_csv(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\data\processed\state_metrics_clean.csv', index=False)

print("\n" + "="*70)
print("RESULTS: PRIORITY INTERVENTION STATES")
print("="*70)
print(f"\n{'Rank':<5} {'State':<30} {'Score':<8} {'IFI':<8} {'CLCR':<8} {'TAES':<8}")
print("-"*70)

for i, (_, row) in enumerate(composite.head(20).iterrows(), 1):
    print(f"{i:<5} {row['state']:<30} {row['composite']:.3f}    {row['ifi']:.2f}    {row['clcr']:.2f}    {row['taes']:.2f}")

print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(f"\nTotal Records Analyzed: {len(enrolment_df) + len(demographic_df) + len(biometric_df):,}")
print(f"Total Enrolments: {enrolment_df['total_enrolments'].sum():,.0f}")
print(f"Total Demographic Updates: {demographic_df['total_demo_updates'].sum():,.0f}")
print(f"Total Biometric Updates: {biometric_df['total_bio_updates'].sum():,.0f}")
print(f"\nStates/UTs Analyzed: {len(composite)}")
print(f"States with IFI < 0.20: {len(ifi_df[ifi_df['ifi'] < 0.20])}")
print(f"States with TAES < 0.70: {len(taes_df[taes_df['taes'] < 0.70])}")

print("\n" + "="*70)
print("TOP PERFORMING STATES")
print("="*70)
top_states = composite.tail(10).iloc[::-1]
for i, (_, row) in enumerate(top_states.iterrows(), 1):
    print(f"{i}. {row['state']}: Composite = {row['composite']:.3f}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nResults saved to: data/processed/state_metrics_clean.csv")
