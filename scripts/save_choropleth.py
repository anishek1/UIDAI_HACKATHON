"""
Standalone script to generate and save India Choropleth Map as PNG
"""
import pandas as pd
import numpy as np
import plotly.express as px
import json
import urllib.request
from pathlib import Path

print("=" * 70)
print("🗺️ GENERATING INDIA CHOROPLETH MAP")
print("=" * 70)

# Load data
BASE_PATH = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON')

# Load state metrics
enrol_path = BASE_PATH / 'data' / 'raw' / 'Enrolment'
enrol_files = list(enrol_path.glob('*.csv'))
enrol_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in enrol_files]
enrolment_df = pd.concat(enrol_dfs, ignore_index=True)
enrolment_df['total_enrolments'] = enrolment_df['age_0_5'] + enrolment_df['age_5_17'] + enrolment_df['age_18_greater']

demo_path = BASE_PATH / 'data' / 'raw' / 'Demographic'
demo_files = list(demo_path.glob('*.csv'))
demo_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in demo_files]
demographic_df = pd.concat(demo_dfs, ignore_index=True)
demographic_df['total_demo_updates'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']

bio_path = BASE_PATH / 'data' / 'raw' / 'Biometric'
bio_files = list(bio_path.glob('*.csv'))
bio_dfs = [pd.read_csv(f, on_bad_lines='skip') for f in bio_files]
biometric_df = pd.concat(bio_dfs, ignore_index=True)
biometric_df['total_bio_updates'] = biometric_df['bio_age_5_17'] + biometric_df['bio_age_17_']

# Aggregate by state
enrol_state = enrolment_df.groupby('state')['total_enrolments'].sum().reset_index()
demo_state = demographic_df.groupby('state')['total_demo_updates'].sum().reset_index()
bio_state = biometric_df.groupby('state')['total_bio_updates'].sum().reset_index()

state_df = enrol_state.merge(demo_state, on='state', how='left')
state_df = state_df.merge(bio_state, on='state', how='left').fillna(0)
state_df['total_updates'] = state_df['total_demo_updates'] + state_df['total_bio_updates']
state_df['ifi'] = state_df['total_updates'] / state_df['total_enrolments'].replace(0, np.nan)
state_df = state_df.fillna(0)

print(f"✓ Loaded data for {len(state_df)} states")

# Load India GeoJSON
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
    output_path = BASE_PATH / 'visualizations' / 'india_choropleth_ifi.png'
    fig.write_image(str(output_path), width=1200, height=800, scale=2)
    print(f"✓ Choropleth saved to: {output_path}")
    print(f"✓ File size: {output_path.stat().st_size / 1024:.1f} KB")
else:
    print("❌ Could not generate choropleth - GeoJSON not available")

print("\n" + "=" * 70)
print("✅ DONE!")
