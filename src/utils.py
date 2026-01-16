"""
Utility Functions for UIDAI Hackathon
=====================================
Common utilities for formatting, validation, and logging.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Optional
import logging
from functools import wraps
import time

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

def setup_logger(name: str = 'uidai', level: int = logging.INFO) -> logging.Logger:
    """
    Create a configured logger instance.
    
    Parameters:
    -----------
    name : str
        Logger name
    level : int
        Logging level (e.g., logging.INFO, logging.DEBUG)
    
    Returns:
    --------
    logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


# =============================================================================
# NUMBER FORMATTING
# =============================================================================

def format_indian_number(num: Union[int, float], precision: int = 2) -> str:
    """
    Format number in Indian numbering system (Lakhs, Crores).
    
    Parameters:
    -----------
    num : int or float
        Number to format
    precision : int
        Decimal places
    
    Returns:
    --------
    str : Formatted string (e.g., "₹6,000 Cr", "45.2 Lakh")
    
    Examples:
    ---------
    >>> format_indian_number(60000000000)
    '₹6,000 Cr'
    >>> format_indian_number(4523456)
    '45.23 Lakh'
    """
    if num >= 1e7:  # Crores (10 million+)
        return f"₹{num/1e7:,.{precision}f} Cr"
    elif num >= 1e5:  # Lakhs (100k+)
        return f"{num/1e5:,.{precision}f} Lakh"
    elif num >= 1e3:  # Thousands
        return f"{num:,.0f}"
    else:
        return f"{num:,.{precision}f}"


def format_number_short(num: Union[int, float], precision: int = 1) -> str:
    """
    Format number with K, M, B suffixes.
    
    Parameters:
    -----------
    num : int or float
        Number to format
    precision : int
        Decimal places
    
    Returns:
    --------
    str : Formatted string (e.g., "4.8M", "35.2K")
    """
    if abs(num) >= 1e9:
        return f"{num/1e9:.{precision}f}B"
    elif abs(num) >= 1e6:
        return f"{num/1e6:.{precision}f}M"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"


def format_percentage(value: float, precision: int = 1) -> str:
    """Format value as percentage string."""
    return f"{value * 100:.{precision}f}%"


def format_score(score: float, precision: int = 2) -> str:
    """Format metric score with consistent precision."""
    return f"{score:.{precision}f}"


# =============================================================================
# DATA VALIDATION
# =============================================================================

def validate_dataframe(df: pd.DataFrame, 
                       required_columns: List[str],
                       name: str = 'DataFrame') -> bool:
    """
    Validate that a DataFrame has required columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to validate
    required_columns : list
        List of required column names
    name : str
        Name for error messages
    
    Returns:
    --------
    bool : True if valid
    
    Raises:
    -------
    ValueError : If validation fails
    """
    if df is None:
        raise ValueError(f"{name} is None")
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"{name} must be a pandas DataFrame")
    
    if df.empty:
        logger.warning(f"{name} is empty")
        return True
    
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")
    
    return True


def validate_numeric_column(df: pd.DataFrame, column: str) -> bool:
    """Validate that a column contains numeric data."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric")
    
    return True


def validate_date_column(df: pd.DataFrame, column: str) -> bool:
    """Validate and convert column to datetime."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        try:
            df[column] = pd.to_datetime(df[column])
        except Exception as e:
            raise ValueError(f"Cannot convert '{column}' to datetime: {e}")
    
    return True


# =============================================================================
# METRIC HELPERS
# =============================================================================

def normalize_scores(series: pd.Series, method: str = 'minmax') -> pd.Series:
    """
    Normalize a series of scores.
    
    Parameters:
    -----------
    series : pd.Series
        Series to normalize
    method : str
        'minmax' or 'zscore'
    
    Returns:
    --------
    pd.Series : Normalized series
    """
    if method == 'minmax':
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([0.5] * len(series), index=series.index)
        return (series - min_val) / (max_val - min_val)
    
    elif method == 'zscore':
        mean_val = series.mean()
        std_val = series.std()
        if std_val == 0:
            return pd.Series([0] * len(series), index=series.index)
        return (series - mean_val) / std_val
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def calculate_percentile_rank(series: pd.Series) -> pd.Series:
    """Calculate percentile rank for each value."""
    return series.rank(pct=True) * 100


def categorize_risk(score: float, 
                    critical_threshold: float = 0.20,
                    at_risk_threshold: float = 0.40,
                    healthy_threshold: float = 0.60) -> str:
    """
    Categorize a metric score into risk level.
    
    Parameters:
    -----------
    score : float
        Metric score (0-1 scale)
    
    Returns:
    --------
    str : 'Critical', 'At Risk', 'Healthy', or 'Optimal'
    """
    if score < critical_threshold:
        return 'Critical'
    elif score < at_risk_threshold:
        return 'At Risk'
    elif score < healthy_threshold:
        return 'Healthy'
    else:
        return 'Optimal'


# =============================================================================
# DECORATORS
# =============================================================================

def timer(func):
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"⏱️ {func.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper


def log_call(func):
    """Decorator to log function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"📊 Running: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"✅ {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"❌ {func.__name__} failed: {e}")
            raise
    return wrapper


# =============================================================================
# STATE/REGION MAPPING
# =============================================================================

REGION_MAPPING = {
    'North': ['Jammu And Kashmir', 'Himachal Pradesh', 'Punjab', 'Chandigarh', 
              'Uttarakhand', 'Haryana', 'Delhi', 'Rajasthan', 'Ladakh'],
    'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana',
              'Puducherry', 'Lakshadweep', 'Andaman And Nicobar Islands'],
    'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
    'West': ['Goa', 'Gujarat', 'Maharashtra', 'Dadra And Nagar Haveli And Daman And Diu'],
    'Northeast': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 
                  'Mizoram', 'Nagaland', 'Sikkim', 'Tripura'],
    'Central': ['Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh'],
}


def get_region(state: str) -> str:
    """Get region for a state."""
    state_normalized = state.strip().title()
    
    for region, states in REGION_MAPPING.items():
        if state_normalized in states:
            return region
    
    return 'Other'


def add_region_column(df: pd.DataFrame, state_col: str = 'state') -> pd.DataFrame:
    """Add region column to DataFrame based on state."""
    df = df.copy()
    df['region'] = df[state_col].apply(get_region)
    return df


# =============================================================================
# EXPORT HELPERS
# =============================================================================

def save_dataframe(df: pd.DataFrame, 
                   path: str, 
                   index: bool = False,
                   format: str = 'csv') -> str:
    """
    Save DataFrame to file with logging.
    
    Parameters:
    -----------
    df : pd.DataFrame
    path : str
    index : bool
    format : str ('csv' or 'excel')
    
    Returns:
    --------
    str : Path to saved file
    """
    if format == 'csv':
        df.to_csv(path, index=index)
    elif format == 'excel':
        df.to_excel(path, index=index)
    else:
        raise ValueError(f"Unknown format: {format}")
    
    logger.info(f"💾 Saved: {path} ({len(df)} rows)")
    return path


# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

def generate_summary_stats(df: pd.DataFrame, 
                           numeric_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Generate summary statistics for numeric columns.
    
    Returns DataFrame with count, mean, std, min, max, median for each column.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    stats = []
    for col in numeric_cols:
        stats.append({
            'column': col,
            'count': df[col].count(),
            'mean': df[col].mean(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'median': df[col].median(),
            'missing': df[col].isna().sum()
        })
    
    return pd.DataFrame(stats)
