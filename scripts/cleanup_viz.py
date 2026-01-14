"""
Audit and clean up visualizations based on project problem statement

Key deliverables from problem statement:
1. IFI - State and district rankings
2. CLCR - Child lifecycle coverage
3. TAES - Weekend vs weekday equity
4. District Priority Matrix
5. ₹ Impact Quantification

Visualizations to KEEP:
- IFI related charts
- CLCR/child biometric charts
- TAES/weekend charts
- District priority charts
- Summary dashboards
- Choropleth maps
- Heatmaps showing state metrics

Visualizations to DELETE:
- Generic/redundant charts
- Charts not directly tied to metrics
"""
import os
from pathlib import Path

viz_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\visualizations')

# Current visualizations
all_viz = list(viz_path.glob('*.png'))
print(f"Total visualizations: {len(all_viz)}")
print("=" * 60)

# Categorize each visualization
KEEP = []
DELETE = []

for viz in sorted(all_viz):
    name = viz.name
    
    # KEEP: Core metric visualizations
    if any(keyword in name.lower() for keyword in [
        'ifi', 'clcr', 'taes', 'composite', 'priority', 'district',
        'choropleth', 'regional', 'dashboard', 'heatmap', 'weekend',
        'child', 'biometric', 'confidence', 'state_map', 'ranking'
    ]):
        KEEP.append(name)
    
    # KEEP: Key numbered charts that are decision-relevant
    elif name in [
        '03_top_states_enrolment.png',  # Shows state volume
        '04_bottom_states.png',         # Shows problem areas
        '06_daily_trend.png',           # Shows temporal patterns
        '07_weekday_comparison.png',    # TAES related
        '09_state_comparison.png',      # State metrics
        '10_child_biometric.png',       # CLCR related
        '11_top_districts.png',         # District priority
        '12_state_month_heatmap.png',   # Temporal patterns
        '14_anomaly_detection.png',     # Outlier states
        '15_summary_dashboard.png',     # Summary
        '16_regional_disparity.png',    # Regional gaps
        '19_trend_analysis.png',        # Trends
    ]:
        KEEP.append(name)
    
    # DELETE: Generic/redundant
    elif name in [
        '01_dataset_comparison.png',    # Not decision-relevant
        '02_age_distribution.png',      # Basic demographic, redundant
        '05_state_age_stacked.png',     # Redundant with other charts
        '08_monthly_trend.png',         # Redundant with daily trend
        '13_correlation_matrix.png',    # Too technical for jury
        '17_accessibility_gap.png',     # Possibly redundant
        '18_child_transition.png',      # May be redundant
    ]:
        DELETE.append(name)
    
    else:
        # Default: Keep if not explicitly deleted
        KEEP.append(name)

print("\n🟢 KEEP (Decision-Relevant):")
for k in sorted(KEEP):
    size = (viz_path / k).stat().st_size / 1024
    print(f"   ✓ {k} ({size:.0f} KB)")

print(f"\n🔴 DELETE (Redundant/Generic):")
for d in sorted(DELETE):
    size = (viz_path / d).stat().st_size / 1024
    print(f"   ✗ {d} ({size:.0f} KB)")

# Calculate space savings
delete_size = sum((viz_path / d).stat().st_size for d in DELETE) / 1024
print(f"\n📊 Summary:")
print(f"   Keep: {len(KEEP)} files")
print(f"   Delete: {len(DELETE)} files")
print(f"   Space savings: {delete_size:.0f} KB")

# Actually delete files
print("\n🗑️ Deleting redundant files...")
for d in DELETE:
    file_path = viz_path / d
    if file_path.exists():
        os.remove(file_path)
        print(f"   Deleted: {d}")

print("\n✅ Cleanup complete!")
print(f"   Remaining visualizations: {len(list(viz_path.glob('*.png')))}")
