
import nbformat
import nbformat.v4 as nbf

nb_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'
out_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Re-define COLORS locally for string interpolation if needed, though mostly using variable references
COLORS = {
    'critical': '#d32f2f',
    'at_risk': '#fbc02d', 
    'healthy': '#388e3c',
    'optimal': '#1976d2',
    'primary': '#1565c0'
}

# ============================================
# CELL 18: Enrolment vs Updates Scatter (Update Efficiency)
# ============================================
cell_18_content = """# Insight 4: UPDATE EFFICIENCY MATRIX
# ============================================
# Insight: Are high-enrolment states keeping their data fresh?

fig, ax = plt.subplots(figsize=(14, 10))

# Color by IFI (Risk Level)
scatter = ax.scatter(state_df['total_enrolments'], state_df['total_updates'],
                     c=state_df['ifi'], cmap='RdYlGn', s=150, alpha=0.8, edgecolors='#424242', linewidth=0.5)

# Add Trend/Expectation Line (Simple linear fit for visual guide)
z = np.polyfit(state_df['total_enrolments'], state_df['total_updates'], 1)
p = np.poly1d(z)
ax.plot(state_df['total_enrolments'], p(state_df['total_enrolments']), "r--", alpha=0.4, label='Expected Update Volume')

# Annotate Notable States (Outliers)
# Top 5 most populous + outliers
notable_states = state_df.nlargest(5, 'total_enrolments')
for _, row in notable_states.iterrows():
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
plt.show()"""

if len(nb.cells) > 18:
    nb.cells[18].source = cell_18_content

# ============================================
# CELL 20: TAES (Weekend Access Equity)
# ============================================
cell_20_content = """# Insight 5: WEEKEND ACCESS EQUITY (TAES)
# ============================================
# Insight: Identifying states that limit access for working citizens.

fig, ax = plt.subplots(figsize=(16, 12))

# Filter: Focus on Bottom 20 States (The Problem Areas)
plot_data = taes_df.head(20).sort_values('taes', ascending=True)

# Color Logic
colors = [COLORS['critical'] if t < 0.7 else COLORS['at_risk'] for t in plot_data['taes']]

bars = ax.barh(plot_data['state'], plot_data['taes'], color=colors, edgecolor='white', height=0.6)

# Threshold Lines
ax.axvline(x=0.70, color=COLORS['at_risk'], linestyle='--', linewidth=2, label='Minimum Standard (0.70)')
ax.axvline(x=1.0, color=COLORS['healthy'], linestyle='-', linewidth=2, alpha=0.5, label='Ideal Parity (1.0)')

# Labels on bars
for bar, val in zip(bars, plot_data['taes']):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.2f}', 
            va='center', fontsize=10, fontweight='bold', color=COLORS['text_main'])

ax.set_title('Weekend Access Equity: Bottom 20 States', pad=20)
ax.set_xlabel('Temporal Access Equity Score (TAES)', fontweight='bold')
ax.set_ylabel('')
ax.set_xlim(0, 1.2)
ax.legend(loc='lower right')

# Add context box
ax.text(0.02, 0.95, "CRITICAL ZONE (< 0.70)\nCitizens struggle to find\nopen centers on weekends.", 
        transform=ax.transAxes, fontsize=12, fontweight='bold', color=COLORS['critical'],
        bbox=dict(facecolor='white', edgecolor=COLORS['critical'], boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.show()"""

if len(nb.cells) > 20:
    nb.cells[20].source = cell_20_content

# ============================================
# CELL 22: Lifecycle Gap
# ============================================
cell_22_content = """# Insight 6: CHILD BIOMETRIC GAP
# ============================================
# Insight: Are we enrolling children but failing to update their biometrics later?

fig, ax = plt.subplots(figsize=(14, 10))

# Size bubbles by total volume
sizes = lifecycle['total_enrolments'] / lifecycle['total_enrolments'].max() * 800 + 50

scatter = ax.scatter(lifecycle['child_enrol_share'], lifecycle['child_bio_share'],
                     s=sizes, c=lifecycle['lifecycle_gap'], cmap='RdYlGn_r',
                     alpha=0.7, edgecolors='#424242', linewidth=1)

# Parity Line (Ideal State)
ax.plot([0, 0.6], [0, 0.6], color=COLORS['text_main'], linestyle='--', alpha=0.5, label='Ideal Ratio (1:1)')

# Annotate High Gap States
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
plt.show()"""

if len(nb.cells) > 22:
    nb.cells[22].source = cell_22_content

# ============================================
# CELL 24: IFI Ranking (The "Lollipop" Chart)
# ============================================
cell_24_content = """# Insight 7: STATE HEALTH RANKINGS (IFI)
# ============================================
# Insight: The definitive leaderboard for Aadhaar ecosystem health.

fig, ax = plt.subplots(figsize=(16, 12))

# Data: Top 25 worst performing (lowest IFI)
plot_data = state_df.nsmallest(25, 'ifi').sort_values('ifi', ascending=True)

# Color Logic
colors = []
for ifi in plot_data['ifi']:
    if ifi < 0.20: colors.append(COLORS['critical'])     # Critical
    elif ifi < 0.40: colors.append(COLORS['at_risk'])    # At Risk
    else: colors.append(COLORS['healthy'])               # Healthy

# Lollipop Chart
ax.hlines(y=plot_data['state'], xmin=0, xmax=plot_data['ifi'], color=colors, alpha=0.6, linewidth=3)
ax.scatter(plot_data['ifi'], plot_data['state'], color=colors, s=120, zorder=5, edgecolors='white', linewidth=1)

# Labels
for i, (ifi, state) in enumerate(zip(plot_data['ifi'], plot_data['state'])):
    ax.text(ifi + 0.02, i, f'{ifi:.2f}', va='center', fontsize=10, fontweight='bold', color='#424242')

# National Average
national_avg = state_df['total_updates'].sum() / state_df['total_enrolments'].sum()
ax.axvline(x=national_avg, color=COLORS['primary'], linestyle='--', linewidth=2, label=f'National Avg: {national_avg:.2f}')

ax.set_title('Identity Freshness Index (IFI): Priority States for Intervention', pad=20)
ax.set_xlabel('IFI Score (Updates per Enrolment)', fontweight='bold')
ax.set_ylabel('')
ax.set_xlim(0, max(plot_data['ifi']) + 0.2)
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()"""

if len(nb.cells) > 24:
    nb.cells[24].source = cell_24_content

print("Script 2/3 applied.")

with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
