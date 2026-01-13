"""
Visualization Utilities for UIDAI Hackathon
============================================
Custom visualization functions for Aadhaar data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set default style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Custom color palettes
COLORS = {
    'primary': '#1a73e8',
    'secondary': '#ea4335',
    'success': '#34a853',
    'warning': '#fbbc04',
    'info': '#4285f4',
    'dark': '#202124',
    'light': '#f8f9fa'
}

AGE_COLORS = {
    '0-5': '#ff6b6b',
    '5-17': '#4ecdc4',
    '18+': '#45b7d1'
}

STATE_COLORS = sns.color_palette("viridis", 36)


def set_plot_style():
    """Set consistent plot styling."""
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.dpi'] = 100


def plot_state_distribution(df: pd.DataFrame, 
                            value_col: str, 
                            title: str,
                            top_n: int = 15,
                            figsize: Tuple = (14, 8),
                            save_path: Optional[str] = None):
    """
    Plot state-wise distribution as horizontal bar chart.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with 'state' column
    value_col : str
        Column to aggregate
    title : str
        Plot title
    top_n : int
        Number of top states to show
    figsize : Tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    """
    set_plot_style()
    
    state_data = df.groupby('state')[value_col].sum().sort_values(ascending=True).tail(top_n)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(state_data)))
    bars = ax.barh(state_data.index, state_data.values, color=colors)
    
    # Add value labels
    for bar, val in zip(bars, state_data.values):
        ax.text(val + state_data.max() * 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:,.0f}', va='center', fontsize=9)
    
    ax.set_xlabel('Count', fontweight='bold')
    ax.set_ylabel('State', fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Format x-axis with commas
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_age_distribution(df: pd.DataFrame,
                         age_columns: List[str],
                         labels: List[str],
                         title: str,
                         figsize: Tuple = (10, 8),
                         save_path: Optional[str] = None):
    """
    Plot age group distribution as pie/donut chart.
    """
    set_plot_style()
    
    totals = [df[col].sum() for col in age_columns]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = [AGE_COLORS.get(label, '#888888') for label in labels]
    
    wedges, texts, autotexts = ax.pie(
        totals, 
        labels=labels, 
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        explode=[0.02] * len(totals),
        shadow=True,
        textprops={'fontsize': 12}
    )
    
    # Make it a donut
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    ax.add_patch(centre_circle)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Add legend with counts
    legend_labels = [f'{label}: {total:,.0f}' for label, total in zip(labels, totals)]
    ax.legend(wedges, legend_labels, loc='lower center', ncol=len(labels),
              bbox_to_anchor=(0.5, -0.1), fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_time_series(df: pd.DataFrame,
                     value_col: str,
                     title: str,
                     freq: str = 'D',
                     figsize: Tuple = (14, 6),
                     save_path: Optional[str] = None):
    """
    Plot time series trend.
    """
    set_plot_style()
    
    time_data = df.groupby(pd.Grouper(key='date', freq=freq))[value_col].sum()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(time_data.index, time_data.values, 
            color=COLORS['primary'], linewidth=2, marker='o', markersize=4)
    ax.fill_between(time_data.index, time_data.values, alpha=0.3, color=COLORS['primary'])
    
    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_heatmap(df: pd.DataFrame,
                 row_col: str,
                 col_col: str,
                 value_col: str,
                 title: str,
                 figsize: Tuple = (14, 10),
                 save_path: Optional[str] = None):
    """
    Plot heatmap for cross-tabulation analysis.
    """
    set_plot_style()
    
    pivot_data = df.pivot_table(
        values=value_col, 
        index=row_col, 
        columns=col_col, 
        aggfunc='sum'
    ).fillna(0)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    sns.heatmap(pivot_data, cmap='YlOrRd', annot=False, 
                fmt='.0f', linewidths=0.5, ax=ax,
                cbar_kws={'label': 'Count'})
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(col_col.title(), fontweight='bold')
    ax.set_ylabel(row_col.title(), fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_weekday_comparison(df: pd.DataFrame,
                            value_col: str,
                            title: str,
                            figsize: Tuple = (12, 6),
                            save_path: Optional[str] = None):
    """
    Plot weekday comparison bar chart.
    """
    set_plot_style()
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_data = df.groupby('weekday')[value_col].sum().reindex(weekday_order)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['#4ecdc4' if day in ['Saturday', 'Sunday'] else '#45b7d1' 
              for day in weekday_order]
    
    bars = ax.bar(weekday_data.index, weekday_data.values, color=colors, edgecolor='white')
    
    # Add value labels
    for bar, val in zip(bars, weekday_data.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + weekday_data.max() * 0.01,
                f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Day of Week', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_comparison_bars(data_dict: dict,
                         title: str,
                         xlabel: str = 'Category',
                         ylabel: str = 'Count',
                         figsize: Tuple = (12, 6),
                         save_path: Optional[str] = None):
    """
    Plot grouped bar chart for comparison.
    """
    set_plot_style()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    x = np.arange(len(data_dict))
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    
    bars = ax.bar(x, list(data_dict.values()), color=colors[:len(data_dict)], 
                  edgecolor='white', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, data_dict.values()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data_dict.values()) * 0.01,
                f'{val:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(list(data_dict.keys()))
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_summary_dashboard(enrolment_df: pd.DataFrame,
                             demographic_df: pd.DataFrame,
                             biometric_df: pd.DataFrame,
                             save_path: Optional[str] = None):
    """
    Create a summary dashboard with key metrics.
    """
    set_plot_style()
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('UIDAI Aadhaar Data Analysis Dashboard', fontsize=20, fontweight='bold', y=1.02)
    
    # 1. Total counts comparison
    ax1 = axes[0, 0]
    totals = {
        'Enrolments': enrolment_df['total_enrolments'].sum() if 'total_enrolments' in enrolment_df.columns else 0,
        'Demo Updates': demographic_df['total_demo_updates'].sum() if 'total_demo_updates' in demographic_df.columns else 0,
        'Bio Updates': biometric_df['total_bio_updates'].sum() if 'total_bio_updates' in biometric_df.columns else 0
    }
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    bars = ax1.bar(totals.keys(), totals.values(), color=colors)
    ax1.set_title('Total Records by Category', fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Add value labels
    for bar, val in zip(bars, totals.values()):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
    
    # 2. Enrolment age distribution
    ax2 = axes[0, 1]
    if all(col in enrolment_df.columns for col in ['age_0_5', 'age_5_17', 'age_18_greater']):
        age_totals = [
            enrolment_df['age_0_5'].sum(),
            enrolment_df['age_5_17'].sum(),
            enrolment_df['age_18_greater'].sum()
        ]
        ax2.pie(age_totals, labels=['0-5 Years', '5-17 Years', '18+ Years'],
                colors=['#ff6b6b', '#4ecdc4', '#45b7d1'], autopct='%1.1f%%', startangle=90)
    ax2.set_title('Enrolment Age Distribution', fontweight='bold')
    
    # 3. Top 10 states (Enrolment)
    ax3 = axes[0, 2]
    if 'total_enrolments' in enrolment_df.columns:
        top_states = enrolment_df.groupby('state')['total_enrolments'].sum().nlargest(10)
        ax3.barh(top_states.index, top_states.values, color=plt.cm.viridis(np.linspace(0.2, 0.8, 10)))
    ax3.set_title('Top 10 States by Enrolment', fontweight='bold')
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # 4. Time series (Enrolment)
    ax4 = axes[1, 0]
    if 'date' in enrolment_df.columns and 'total_enrolments' in enrolment_df.columns:
        daily_enrol = enrolment_df.groupby('date')['total_enrolments'].sum()
        ax4.plot(daily_enrol.index, daily_enrol.values, color=COLORS['primary'], linewidth=1)
        ax4.fill_between(daily_enrol.index, daily_enrol.values, alpha=0.3, color=COLORS['primary'])
    ax4.set_title('Daily Enrolment Trend', fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Weekday comparison
    ax5 = axes[1, 1]
    if 'weekday' in enrolment_df.columns and 'total_enrolments' in enrolment_df.columns:
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_data = enrolment_df.groupby('weekday')['total_enrolments'].sum()
        weekday_data = weekday_data.reindex(weekday_order)
        colors = ['#4ecdc4' if day in ['Saturday', 'Sunday'] else '#45b7d1' for day in weekday_order]
        ax5.bar(range(7), weekday_data.values, color=colors)
        ax5.set_xticks(range(7))
        ax5.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax5.set_title('Enrolment by Day of Week', fontweight='bold')
    
    # 6. Update comparison (Demo vs Bio)
    ax6 = axes[1, 2]
    if 'total_demo_updates' in demographic_df.columns and 'total_bio_updates' in biometric_df.columns:
        update_comparison = {
            'Demographic': demographic_df['total_demo_updates'].sum(),
            'Biometric': biometric_df['total_bio_updates'].sum()
        }
        ax6.bar(update_comparison.keys(), update_comparison.values(), 
                color=[COLORS['secondary'], COLORS['success']])
    ax6.set_title('Demographic vs Biometric Updates', fontweight='bold')
    ax6.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()
