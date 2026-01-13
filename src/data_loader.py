"""
Data Loading Utilities for UIDAI Hackathon
==========================================
Functions to load, merge, and preprocess Aadhaar datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional
import warnings
warnings.filterwarnings('ignore')


def load_dataset_chunks(folder_path: str, dataset_type: str) -> pd.DataFrame:
    """
    Load and merge all CSV chunks for a given dataset type.
    
    Parameters:
    -----------
    folder_path : str
        Path to the main data directory
    dataset_type : str
        One of 'Enrolment', 'Demographic', 'Biometric'
    
    Returns:
    --------
    pd.DataFrame
        Merged dataframe with all chunks
    """
    data_path = Path(folder_path) / dataset_type
    
    if not data_path.exists():
        raise FileNotFoundError(f"Directory not found: {data_path}")
    
    csv_files = list(data_path.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    
    print(f"📂 Loading {dataset_type} dataset...")
    print(f"   Found {len(csv_files)} files")
    
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)
        print(f"   ✓ Loaded {file.name}: {len(df):,} rows")
    
    merged_df = pd.concat(dfs, ignore_index=True)
    print(f"   📊 Total rows: {len(merged_df):,}\n")
    
    return merged_df


def load_all_datasets(base_path: str) -> dict:
    """
    Load all three datasets (Enrolment, Demographic, Biometric).
    
    Parameters:
    -----------
    base_path : str
        Path to the main project directory containing data folders
    
    Returns:
    --------
    dict
        Dictionary with keys 'enrolment', 'demographic', 'biometric'
    """
    datasets = {}
    
    for dtype in ['Enrolment', 'Demographic', 'Biometric']:
        try:
            datasets[dtype.lower()] = load_dataset_chunks(base_path, dtype)
        except FileNotFoundError as e:
            print(f"⚠️ Warning: {e}")
            datasets[dtype.lower()] = None
    
    return datasets


def preprocess_dataframe(df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
    """
    Clean and preprocess a dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataframe
    dataset_type : str
        One of 'enrolment', 'demographic', 'biometric'
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe with additional features
    """
    df = df.copy()
    
    # Parse date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        
        # Extract temporal features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.day_name()
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['is_weekend'] = df['date'].dt.dayofweek >= 5
    
    # Standardize state names
    if 'state' in df.columns:
        df['state'] = df['state'].str.strip().str.title()
    
    # Standardize district names
    if 'district' in df.columns:
        df['district'] = df['district'].str.strip().str.title()
    
    # Ensure pincode is string
    if 'pincode' in df.columns:
        df['pincode'] = df['pincode'].astype(str).str.zfill(6)
    
    # Add total column based on dataset type
    if dataset_type == 'enrolment':
        if all(col in df.columns for col in ['age_0_5', 'age_5_17', 'age_18_greater']):
            df['total_enrolments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    
    elif dataset_type == 'demographic':
        if all(col in df.columns for col in ['demo_age_5_17', 'demo_age_17_']):
            df['total_demo_updates'] = df['demo_age_5_17'] + df['demo_age_17_']
    
    elif dataset_type == 'biometric':
        if all(col in df.columns for col in ['bio_age_5_17', 'bio_age_17_']):
            df['total_bio_updates'] = df['bio_age_5_17'] + df['bio_age_17_']
    
    return df


def get_data_summary(df: pd.DataFrame, name: str) -> dict:
    """
    Generate a summary of the dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to summarize
    name : str
        Name of the dataset
    
    Returns:
    --------
    dict
        Summary statistics
    """
    summary = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
    }
    
    if 'date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['date']):
        summary['date_range'] = f"{df['date'].min()} to {df['date'].max()}"
    
    if 'state' in df.columns:
        summary['unique_states'] = df['state'].nunique()
    
    if 'district' in df.columns:
        summary['unique_districts'] = df['district'].nunique()
    
    return summary


def print_data_summary(summary: dict):
    """Print formatted data summary."""
    print(f"\n{'='*50}")
    print(f"📊 {summary['name'].upper()} DATASET SUMMARY")
    print(f"{'='*50}")
    print(f"  Rows:           {summary['rows']:,}")
    print(f"  Columns:        {summary['columns']}")
    print(f"  Missing Values: {summary['missing_values']:,}")
    print(f"  Duplicates:     {summary['duplicates']:,}")
    print(f"  Memory:         {summary['memory_mb']:.2f} MB")
    
    if 'date_range' in summary:
        print(f"  Date Range:     {summary['date_range']}")
    if 'unique_states' in summary:
        print(f"  Unique States:  {summary['unique_states']}")
    if 'unique_districts' in summary:
        print(f"  Unique Districts: {summary['unique_districts']}")
    print(f"{'='*50}\n")
