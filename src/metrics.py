"""
Engineered Metrics for UIDAI Hackathon
=======================================
5 core metrics for Identity Lifecycle Health Analysis.

Metrics:
1. IFI  - Identity Freshness Index
2. CLCR - Child Lifecycle Capture Rate
3. TAES - Temporal Access Equity Score
4. UCR  - Update Completeness Ratio
5. AAUP - Age-Adjusted Update Propensity
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# METRIC 1: Identity Freshness Index (IFI)
# =============================================================================

def calculate_ifi(
    enrolment_df: pd.DataFrame,
    demographic_df: pd.DataFrame,
    biometric_df: pd.DataFrame,
    group_by: str = 'state'
) -> pd.DataFrame:
    """
    Calculate Identity Freshness Index at specified granularity.
    
    IFI = (Demographic Updates + Biometric Updates) / Total Enrolments
    
    Parameters
    ----------
    enrolment_df : DataFrame with enrolment data
    demographic_df : DataFrame with demographic update data
    biometric_df : DataFrame with biometric update data
    group_by : 'state' or 'district' level aggregation
    
    Returns
    -------
    DataFrame with IFI scores and risk categories
    """
    # Aggregate enrolments
    if 'total_enrolments' not in enrolment_df.columns:
        enrolment_df = enrolment_df.copy()
        enrolment_df['total_enrolments'] = (
            enrolment_df['age_0_5'] + 
            enrolment_df['age_5_17'] + 
            enrolment_df['age_18_greater']
        )
    
    enrol_agg = enrolment_df.groupby(group_by)['total_enrolments'].sum().reset_index()
    
    # Aggregate demographic updates
    if 'total_demo_updates' not in demographic_df.columns:
        demographic_df = demographic_df.copy()
        demographic_df['total_demo_updates'] = (
            demographic_df['demo_age_5_17'] + 
            demographic_df['demo_age_17_']
        )
    
    demo_agg = demographic_df.groupby(group_by)['total_demo_updates'].sum().reset_index()
    
    # Aggregate biometric updates
    if 'total_bio_updates' not in biometric_df.columns:
        biometric_df = biometric_df.copy()
        biometric_df['total_bio_updates'] = (
            biometric_df['bio_age_5_17'] + 
            biometric_df['bio_age_17_']
        )
    
    bio_agg = biometric_df.groupby(group_by)['total_bio_updates'].sum().reset_index()
    
    # Merge all
    result = enrol_agg.merge(demo_agg, on=group_by, how='left')
    result = result.merge(bio_agg, on=group_by, how='left')
    result = result.fillna(0)
    
    # Calculate IFI
    result['total_updates'] = result['total_demo_updates'] + result['total_bio_updates']
    result['ifi'] = result['total_updates'] / result['total_enrolments'].replace(0, np.nan)
    result['ifi'] = result['ifi'].fillna(0)
    
    # Categorize risk
    result['ifi_risk'] = pd.cut(
        result['ifi'],
        bins=[-np.inf, 0.20, 0.40, 0.60, np.inf],
        labels=['Critical', 'At Risk', 'Healthy', 'Optimal']
    )
    
    return result.sort_values('ifi', ascending=True)


# =============================================================================
# METRIC 2: Child Lifecycle Capture Rate (CLCR)
# =============================================================================

def calculate_clcr(
    enrolment_df: pd.DataFrame,
    biometric_df: pd.DataFrame,
    group_by: str = 'state',
    expected_annual_update_rate: float = 0.20
) -> pd.DataFrame:
    """
    Calculate Child Lifecycle Capture Rate.
    
    CLCR = bio_age_5_17 / (enrol_age_5_17 × expected_rate)
    
    Measures whether children are receiving mandatory biometric updates.
    
    Parameters
    ----------
    enrolment_df : DataFrame with enrolment data
    biometric_df : DataFrame with biometric update data
    group_by : 'state' or 'district' level aggregation
    expected_annual_update_rate : Expected % of children updating per year (default 20%)
    
    Returns
    -------
    DataFrame with CLCR scores
    """
    # Aggregate child enrolments
    enrol_child = enrolment_df.groupby(group_by)['age_5_17'].sum().reset_index()
    enrol_child.columns = [group_by, 'child_enrolments']
    
    # Aggregate child biometric updates
    bio_child = biometric_df.groupby(group_by)['bio_age_5_17'].sum().reset_index()
    bio_child.columns = [group_by, 'child_bio_updates']
    
    # Merge
    result = enrol_child.merge(bio_child, on=group_by, how='left')
    result = result.fillna(0)
    
    # Calculate CLCR
    expected_updates = result['child_enrolments'] * expected_annual_update_rate
    result['clcr'] = result['child_bio_updates'] / expected_updates.replace(0, np.nan)
    result['clcr'] = result['clcr'].fillna(0)
    
    # Categorize
    result['clcr_status'] = pd.cut(
        result['clcr'],
        bins=[-np.inf, 0.50, 0.80, 1.00, np.inf],
        labels=['Critical Gap', 'Below Target', 'On Track', 'Exceeding']
    )
    
    return result.sort_values('clcr', ascending=True)


# =============================================================================
# METRIC 3: Temporal Access Equity Score (TAES)
# =============================================================================

def calculate_taes(
    df: pd.DataFrame,
    value_col: str = 'total_enrolments',
    group_by: str = 'state'
) -> pd.DataFrame:
    """
    Calculate Temporal Access Equity Score.
    
    TAES = Avg(weekend_daily) / Avg(weekday_daily)
    
    Measures whether weekend service is equitable.
    
    Parameters
    ----------
    df : DataFrame with date column and value column
    value_col : Column to aggregate (enrolments or updates)
    group_by : 'state' or 'district' level aggregation
    
    Returns
    -------
    DataFrame with TAES scores
    """
    df = df.copy()
    
    # Ensure date parsing
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    df['is_weekend'] = df['date'].dt.dayofweek >= 5
    
    # Calculate daily totals by group
    daily = df.groupby([group_by, 'date', 'is_weekend'])[value_col].sum().reset_index()
    
    # Separate weekend and weekday averages
    weekend_avg = daily[daily['is_weekend']].groupby(group_by)[value_col].mean().reset_index()
    weekend_avg.columns = [group_by, 'weekend_avg']
    
    weekday_avg = daily[~daily['is_weekend']].groupby(group_by)[value_col].mean().reset_index()
    weekday_avg.columns = [group_by, 'weekday_avg']
    
    # Merge and calculate TAES
    result = weekend_avg.merge(weekday_avg, on=group_by, how='outer')
    result = result.fillna(0)
    
    result['taes'] = result['weekend_avg'] / result['weekday_avg'].replace(0, np.nan)
    result['taes'] = result['taes'].fillna(0).clip(upper=1.5)  # Cap at 1.5
    
    # Categorize
    result['taes_status'] = pd.cut(
        result['taes'],
        bins=[-np.inf, 0.50, 0.70, 0.90, np.inf],
        labels=['Severe Inequity', 'Moderate Inequity', 'Acceptable', 'Equitable']
    )
    
    return result.sort_values('taes', ascending=True)


# =============================================================================
# METRIC 4: Update Completeness Ratio (UCR)
# =============================================================================

def calculate_ucr(
    demographic_df: pd.DataFrame,
    biometric_df: pd.DataFrame,
    group_by: str = 'state',
    min_activity_threshold: int = 100
) -> pd.DataFrame:
    """
    Calculate Update Completeness Ratio.
    
    UCR = (Districts with > threshold updates) / Total Districts
    
    Measures geographic coverage of update services.
    
    Parameters
    ----------
    demographic_df : DataFrame with demographic updates
    biometric_df : DataFrame with biometric updates
    group_by : 'state' level (counts districts within state)
    min_activity_threshold : Minimum updates to count as "active"
    
    Returns
    -------
    DataFrame with UCR scores
    """
    # Combine updates at district level
    demo_dist = demographic_df.groupby(['state', 'district']).agg({
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum'
    }).reset_index()
    demo_dist['total_demo'] = demo_dist['demo_age_5_17'] + demo_dist['demo_age_17_']
    
    bio_dist = biometric_df.groupby(['state', 'district']).agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum'
    }).reset_index()
    bio_dist['total_bio'] = bio_dist['bio_age_5_17'] + bio_dist['bio_age_17_']
    
    # Merge
    dist_data = demo_dist.merge(bio_dist, on=['state', 'district'], how='outer')
    dist_data = dist_data.fillna(0)
    dist_data['total_updates'] = dist_data['total_demo'] + dist_data['total_bio']
    
    # Flag active districts
    dist_data['is_active'] = dist_data['total_updates'] >= min_activity_threshold
    
    # Aggregate to state level
    result = dist_data.groupby('state').agg({
        'district': 'count',
        'is_active': 'sum'
    }).reset_index()
    result.columns = ['state', 'total_districts', 'active_districts']
    
    # Calculate UCR
    result['ucr'] = result['active_districts'] / result['total_districts']
    
    # Categorize
    result['ucr_status'] = pd.cut(
        result['ucr'],
        bins=[-np.inf, 0.50, 0.75, 0.90, np.inf],
        labels=['Poor Coverage', 'Partial', 'Good', 'Excellent']
    )
    
    return result.sort_values('ucr', ascending=True)


# =============================================================================
# METRIC 5: Age-Adjusted Update Propensity (AAUP)
# =============================================================================

def calculate_aaup(
    demographic_df: pd.DataFrame,
    biometric_df: pd.DataFrame,
    population_df: pd.DataFrame,
    group_by: str = 'state'
) -> pd.DataFrame:
    """
    Calculate Age-Adjusted Update Propensity.
    
    AAUP = (updates per capita) / (national average per capita)
    
    Population-normalized update rate comparison.
    
    Parameters
    ----------
    demographic_df : DataFrame with demographic updates
    biometric_df : DataFrame with biometric updates  
    population_df : DataFrame with state population data
    group_by : 'state' level aggregation
    
    Returns
    -------
    DataFrame with AAUP scores
    """
    # Aggregate updates by state
    demo_agg = demographic_df.groupby('state').agg({
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum'
    }).reset_index()
    demo_agg['demo_total'] = demo_agg['demo_age_5_17'] + demo_agg['demo_age_17_']
    
    bio_agg = biometric_df.groupby('state').agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum'
    }).reset_index()
    bio_agg['bio_total'] = bio_agg['bio_age_5_17'] + bio_agg['bio_age_17_']
    
    # Merge updates
    updates = demo_agg.merge(bio_agg, on='state', how='outer')
    updates = updates.fillna(0)
    updates['total_updates'] = updates['demo_total'] + updates['bio_total']
    
    # Merge with population
    result = updates.merge(
        population_df[['state', 'population_2024_est']], 
        on='state', 
        how='left'
    )
    
    # Calculate per-capita rate
    result['updates_per_10k'] = (
        result['total_updates'] / result['population_2024_est'] * 10000
    )
    
    # Calculate national average
    national_avg = result['updates_per_10k'].mean()
    
    # Calculate AAUP
    result['aaup'] = result['updates_per_10k'] / national_avg
    
    # Categorize
    result['aaup_status'] = pd.cut(
        result['aaup'],
        bins=[-np.inf, 0.50, 0.80, 1.20, np.inf],
        labels=['Severely Under', 'Under', 'Normal', 'Over']
    )
    
    return result.sort_values('aaup', ascending=True)


# =============================================================================
# COMBINED METRICS DASHBOARD
# =============================================================================

def calculate_all_metrics(
    enrolment_df: pd.DataFrame,
    demographic_df: pd.DataFrame,
    biometric_df: pd.DataFrame,
    population_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Calculate all 5 metrics and return unified state-level dashboard.
    
    Returns
    -------
    DataFrame with all metric scores per state
    """
    # Calculate each metric
    ifi = calculate_ifi(enrolment_df, demographic_df, biometric_df, 'state')
    clcr = calculate_clcr(enrolment_df, biometric_df, 'state')
    taes = calculate_taes(enrolment_df, 'total_enrolments', 'state')
    ucr = calculate_ucr(demographic_df, biometric_df, 'state')
    
    # Merge all
    result = ifi[['state', 'ifi', 'ifi_risk', 'total_enrolments', 'total_updates']]
    result = result.merge(clcr[['state', 'clcr', 'clcr_status']], on='state', how='left')
    result = result.merge(taes[['state', 'taes', 'taes_status']], on='state', how='left')
    result = result.merge(ucr[['state', 'ucr', 'ucr_status']], on='state', how='left')
    
    # Add AAUP if population data available
    if population_df is not None:
        aaup = calculate_aaup(demographic_df, biometric_df, population_df, 'state')
        result = result.merge(aaup[['state', 'aaup', 'aaup_status']], on='state', how='left')
    
    # Calculate composite score (simple average of normalized metrics)
    result['composite_score'] = (
        result['ifi'].clip(upper=1) * 0.30 +
        result['clcr'].clip(upper=1) * 0.25 +
        result['taes'].clip(upper=1) * 0.20 +
        result['ucr'] * 0.25
    )
    
    return result.sort_values('composite_score', ascending=True)


# =============================================================================
# LIFECYCLE GAP ANALYSIS (Trivariate)
# =============================================================================

def calculate_lifecycle_gap(
    enrolment_df: pd.DataFrame,
    biometric_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Trivariate analysis: State × Age × Update
    
    Identifies states with high child enrolment but low biometric updates.
    
    Returns
    -------
    DataFrame with lifecycle gap scores
    """
    # Child share of enrolments
    enrol_agg = enrolment_df.groupby('state').agg({
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    enrol_agg['child_share'] = (
        enrol_agg['age_5_17'] / 
        (enrol_agg['age_5_17'] + enrol_agg['age_18_greater'])
    )
    
    # Child bio update rate
    bio_agg = biometric_df.groupby('state').agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum'
    }).reset_index()
    bio_agg['child_bio_share'] = (
        bio_agg['bio_age_5_17'] / 
        (bio_agg['bio_age_5_17'] + bio_agg['bio_age_17_'])
    )
    
    # Merge
    result = enrol_agg.merge(bio_agg, on='state')
    
    # Calculate lifecycle gap
    # Positive = high enrolment but low update (gap exists)
    result['lifecycle_gap'] = result['child_share'] - result['child_bio_share']
    
    # Identify quadrant
    result['quadrant'] = 'Normal'
    result.loc[
        (result['child_share'] > 0.35) & (result['lifecycle_gap'] > 0.05), 
        'quadrant'
    ] = 'LIFECYCLE GAP'
    result.loc[
        (result['child_share'] > 0.35) & (result['lifecycle_gap'] <= 0.05), 
        'quadrant'
    ] = 'Working System'
    result.loc[
        (result['child_share'] <= 0.35) & (result['lifecycle_gap'] > 0.05), 
        'quadrant'
    ] = 'Monitoring Needed'
    
    return result.sort_values('lifecycle_gap', ascending=False)


# =============================================================================
# METRIC 6: Risk Prediction Score (RPS) - NEW
# =============================================================================

def calculate_risk_prediction_score(
    ifi: float,
    clcr: float,
    taes: float,
    weights: dict = None
) -> float:
    """
    Calculate composite Risk Prediction Score predicting DBT failure probability.
    
    RPS = w1*(1-IFI) + w2*(1-CLCR) + w3*(1-TAES)
    
    Higher RPS = Higher risk of authentication failures and DBT disruption.
    
    Parameters
    ----------
    ifi : float
        Identity Freshness Index (0-1 scale)
    clcr : float
        Child Lifecycle Capture Rate (0-1 scale)
    taes : float
        Temporal Access Equity Score (0-1 scale)
    weights : dict, optional
        Custom weights for each metric. Default: {'ifi': 0.5, 'clcr': 0.3, 'taes': 0.2}
    
    Returns
    -------
    float : Risk Prediction Score (0-1, higher = more risk)
    """
    if weights is None:
        weights = {'ifi': 0.5, 'clcr': 0.3, 'taes': 0.2}
    
    # Normalize inputs to 0-1 range
    ifi_norm = min(max(ifi, 0), 1)
    clcr_norm = min(max(clcr, 0), 1)
    taes_norm = min(max(taes, 0), 1)
    
    # Calculate risk (inverse of health)
    rps = (
        weights['ifi'] * (1 - ifi_norm) +
        weights['clcr'] * (1 - clcr_norm) +
        weights['taes'] * (1 - taes_norm)
    )
    
    return round(rps, 4)


def calculate_rps_dataframe(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Risk Prediction Score for all states in metrics DataFrame.
    
    Parameters
    ----------
    metrics_df : DataFrame with 'ifi', 'clcr', 'taes' columns
    
    Returns
    -------
    DataFrame with 'rps' column added
    """
    result = metrics_df.copy()
    
    result['rps'] = result.apply(
        lambda row: calculate_risk_prediction_score(
            row['ifi'] if row['ifi'] <= 1 else row['ifi'] / 100,  # Handle percentage format
            row['clcr'],
            row['taes']
        ),
        axis=1
    )
    
    # Categorize risk levels
    result['rps_level'] = pd.cut(
        result['rps'],
        bins=[-np.inf, 0.30, 0.50, 0.70, np.inf],
        labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
    )
    
    # Estimate DBT impact (₹ Crores at risk)
    # Assumption: Total DBT = ₹10 lakh Cr, distributed by population
    total_dbt = 1000000  # ₹ Crores
    result['dbt_at_risk_cr'] = (result['rps'] * total_dbt * 0.06).round(0)  # 6% allocation
    
    return result.sort_values('rps', ascending=False)


# =============================================================================
# METRIC 7: Equity Gap Score (EGS) - NEW
# =============================================================================

def calculate_equity_gap(
    metrics_df: pd.DataFrame,
    group_col: str = 'region',
    metric_col: str = 'ifi'
) -> pd.DataFrame:
    """
    Calculate equity gap - disparity between best and worst performers within groups.
    
    Measures how unequal service delivery is within regions/states.
    
    Parameters
    ----------
    metrics_df : DataFrame with metrics and grouping column
    group_col : Column to group by (e.g., 'region', 'state')
    metric_col : Metric to analyze (e.g., 'ifi', 'clcr')
    
    Returns
    -------
    DataFrame with equity gap scores per group
    """
    result = metrics_df.groupby(group_col).agg({
        metric_col: ['min', 'max', 'mean', 'std', 'count']
    }).reset_index()
    
    result.columns = [group_col, 'min_score', 'max_score', 'mean_score', 'std_score', 'count']
    
    # Calculate equity gap (range / mean, normalized)
    result['range'] = result['max_score'] - result['min_score']
    result['equity_gap'] = result['range'] / result['mean_score'].replace(0, np.nan)
    result['equity_gap'] = result['equity_gap'].fillna(0)
    
    # Calculate coefficient of variation
    result['cv'] = result['std_score'] / result['mean_score'].replace(0, np.nan)
    result['cv'] = result['cv'].fillna(0)
    
    # Equity status
    result['equity_status'] = pd.cut(
        result['equity_gap'],
        bins=[-np.inf, 0.30, 0.60, 1.00, np.inf],
        labels=['Equitable', 'Moderate Gap', 'Significant Gap', 'Severe Disparity']
    )
    
    return result.sort_values('equity_gap', ascending=False)


def calculate_district_equity_within_state(
    district_df: pd.DataFrame,
    metric_col: str = 'ifi'
) -> pd.DataFrame:
    """
    Calculate equity gap at district level within each state.
    
    Identifies states with large internal disparities.
    """
    return calculate_equity_gap(district_df, 'state', metric_col)


# =============================================================================
# STATISTICAL CONFIDENCE UTILITIES - NEW
# =============================================================================

def calculate_confidence_interval(
    data: pd.Series,
    confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for a metric.
    
    Parameters
    ----------
    data : pd.Series of values
    confidence : Confidence level (default 0.95 for 95% CI)
    
    Returns
    -------
    Tuple of (mean, lower_bound, upper_bound)
    """
    from scipy import stats
    
    n = len(data)
    mean = data.mean()
    
    if n < 2:
        return (mean, mean, mean)
    
    std_err = data.std() / np.sqrt(n)
    
    # t-distribution for small samples
    if n < 30:
        t_val = stats.t.ppf((1 + confidence) / 2, n - 1)
    else:
        t_val = stats.norm.ppf((1 + confidence) / 2)
    
    margin = t_val * std_err
    
    return (mean, mean - margin, mean + margin)


def add_confidence_to_metrics(
    df: pd.DataFrame,
    metric_cols: list,
    group_by: str = 'state'
) -> pd.DataFrame:
    """
    Add confidence intervals to aggregated metrics.
    
    Parameters
    ----------
    df : Raw data DataFrame
    metric_cols : List of metric columns to calculate CI for
    group_by : Grouping column
    
    Returns
    -------
    DataFrame with _ci_lower and _ci_upper columns for each metric
    """
    try:
        from scipy import stats
        
        result_data = []
        
        for group_name, group_df in df.groupby(group_by):
            row = {group_by: group_name}
            
            for col in metric_cols:
                if col in group_df.columns:
                    mean, lower, upper = calculate_confidence_interval(group_df[col])
                    row[col] = mean
                    row[f'{col}_ci_lower'] = lower
                    row[f'{col}_ci_upper'] = upper
                    row[f'{col}_sample_size'] = len(group_df)
            
            result_data.append(row)
        
        return pd.DataFrame(result_data)
    
    except ImportError:
        # Fallback without scipy
        return df.groupby(group_by)[metric_cols].agg(['mean', 'std', 'count']).reset_index()


def flag_low_confidence_estimates(
    df: pd.DataFrame,
    sample_col: str,
    min_sample: int = 30
) -> pd.DataFrame:
    """
    Flag estimates with low sample sizes that may be unreliable.
    
    Parameters
    ----------
    df : DataFrame with sample size column
    sample_col : Name of sample size column
    min_sample : Minimum sample size for reliable estimate
    
    Returns
    -------
    DataFrame with 'low_confidence' flag column
    """
    result = df.copy()
    result['low_confidence'] = result[sample_col] < min_sample
    result['confidence_note'] = result['low_confidence'].apply(
        lambda x: '⚠️ Low sample size' if x else '✓ Reliable'
    )
    return result


# =============================================================================
# PRIORITY RANKING - NEW
# =============================================================================

def calculate_intervention_priority(
    metrics_df: pd.DataFrame,
    population_col: str = None
) -> pd.DataFrame:
    """
    Calculate intervention priority score combining risk and impact.
    
    Priority = RPS × Log(Population affected)
    
    Parameters
    ----------
    metrics_df : DataFrame with metrics
    population_col : Column with population data (optional)
    
    Returns
    -------
    DataFrame with priority rankings
    """
    result = metrics_df.copy()
    
    # Calculate RPS if not present
    if 'rps' not in result.columns:
        result = calculate_rps_dataframe(result)
    
    # Calculate priority
    if population_col and population_col in result.columns:
        result['log_population'] = np.log10(result[population_col].replace(0, 1))
        result['priority_score'] = result['rps'] * result['log_population']
    else:
        result['priority_score'] = result['rps']
    
    # Normalize to 0-100
    max_priority = result['priority_score'].max()
    if max_priority > 0:
        result['priority_score_normalized'] = (result['priority_score'] / max_priority * 100).round(1)
    else:
        result['priority_score_normalized'] = 0
    
    # Rank
    result['priority_rank'] = result['priority_score_normalized'].rank(ascending=False).astype(int)
    
    # Intervention tier
    result['intervention_tier'] = pd.cut(
        result['priority_rank'],
        bins=[0, 5, 15, 30, np.inf],
        labels=['Tier 1: Immediate', 'Tier 2: Short-term', 'Tier 3: Medium-term', 'Tier 4: Monitoring']
    )
    
    return result.sort_values('priority_rank')
