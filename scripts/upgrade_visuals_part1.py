
import nbformat
import nbformat.v4 as nbf

nb_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'
out_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb' # Overwrite

print("Loading notebook...")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# ============================================
# NEW STYLE SETUP (Cell 6)
# ============================================
# We define a robust style setup that will apply globally.
cell_6_content = """# ============================================
# SETUP & IMPORTS
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
plt.rcParams['legend.framealpha'] = 0.9
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
import matplotlib.colors as mcolors
cmap_risk = mcolors.LinearSegmentedColormap.from_list("risk", [COLORS['healthy'], COLORS['at_risk'], COLORS['critical']])
cmap_performance = mcolors.LinearSegmentedColormap.from_list("perf", [COLORS['critical'], COLORS['at_risk'], COLORS['healthy'], COLORS['optimal']])

print("✅ Visualization standards applied successfully")
"""

nb.cells[6].source = cell_6_content

# ============================================
# CELL 12: Daily Enrolment Trend
# ============================================
cell_12_content = """# Insight 1: DAILY ENROLMENT TREND
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

# Highlight Weekends (Visualizing the Gap)
import matplotlib.dates as mdates
# Find a few weekend spans to highlight (not all to avoid clutter, or maybe subtle background)
# Creating a weekend mask for background
# For clarity, we'll just annotate the pattern
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
plt.show()"""

if len(nb.cells) > 12:
    nb.cells[12].source = cell_12_content

# ============================================
# CELL 14: Age Distribution (Improve Colors & Labels)
# ============================================
cell_14_content = """# Insight 2: DEMOGRAPHIC COMPOSITION
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
# Use our consistent palette
colors = [COLORS['at_risk'], COLORS['optimal'], COLORS['primary']]

# 1. Pie Chart (Donut Style for Modern Look)
wedges, texts, autotexts = axes[0].pie(age_totals, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90, pctdistance=0.85, 
                                        wedgeprops=dict(width=0.5, edgecolor='white'))
# Style pie text
for t in texts: t.set_fontsize(11)
for t in autotexts: t.set_fontsize(11); t.set_fontweight('bold'); t.set_color('white')

axes[0].set_title('Share of Total Enrolments', pad=15)

# Add center text
axes[0].text(0, 0, f"Total\n{sum(age_totals)/1e6:.1f}M", ha='center', va='center', fontsize=14, fontweight='bold')

# 2. Bar Chart
bar_x = np.arange(len(labels))
bars = axes[1].bar(bar_x, age_totals, color=colors, edgecolor='white', width=0.6)

# Labels on bars
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
plt.show()"""

if len(nb.cells) > 14:
    nb.cells[14].source = cell_14_content

# ============================================
# CELL 16: Weekend vs Weekday
# ============================================
cell_16_content = """# Insight 3: WEEKEND ACCESSIBILITY GAP
# ============================================
# Insight: Quantifying the service drop-off on weekends.

fig, ax = plt.subplots(figsize=(14, 7))

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_data = enrolment_df.groupby('weekday')['total_enrolments'].sum().reindex(weekday_order)

# Conditional Coloring
colors = [COLORS['healthy'] if day in ['Saturday', 'Sunday'] else COLORS['primary'] for day in weekday_order]

bars = ax.bar(weekday_data.index, weekday_data.values, color=colors, edgecolor='white', width=0.7)

# Annotation of the Gap
avg_weekday = weekday_data[:5].mean()
avg_weekend = weekday_data[5:].mean()
gap_pct = (avg_weekend - avg_weekday) / avg_weekday * 100

ax.axhline(y=avg_weekday, color=COLORS['primary'], linestyle='--', alpha=0.5, label='Avg Weekday Volume')
ax.axhline(y=avg_weekend, color=COLORS['healthy'], linestyle='--', alpha=0.5, label='Avg Weekend Volume')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02*max(weekday_data.values),
            f'{height/1000:.0f}K', ha='center', va='bottom', fontsize=10)

# Gap Arrow
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
plt.show()"""

if len(nb.cells) > 16:
    nb.cells[16].source = cell_16_content

print("Script 1/3 applied.")

with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
