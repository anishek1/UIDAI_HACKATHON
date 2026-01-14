"""
Update choropleth code with kaleido image export
"""
import json
from pathlib import Path

notebook_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb')

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and update the choropleth cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'INDIA CHOROPLETH MAP - IFI BY STATE' in source:
            # Replace with version that includes image export
            cell['source'] = [
                "# ============================================\n",
                "# INDIA CHOROPLETH MAP - IFI BY STATE\n",
                "# ============================================\n",
                "\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "import json\n",
                "import urllib.request\n",
                "\n",
                "print(\"=\"*70)\n",
                "print(\"🗺️ GENERATING INDIA CHOROPLETH MAP\")\n",
                "print(\"=\"*70)\n",
                "\n",
                "# Load India GeoJSON from public source\n",
                "india_geojson_url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'\n",
                "\n",
                "try:\n",
                "    with urllib.request.urlopen(india_geojson_url, timeout=15) as url:\n",
                "        india_geojson = json.loads(url.read().decode())\n",
                "    print(\"✓ India GeoJSON loaded successfully\")\n",
                "except Exception as e:\n",
                "    print(f\"⚠️ Could not load GeoJSON: {e}\")\n",
                "    india_geojson = None\n",
                "\n",
                "if india_geojson:\n",
                "    # Prepare data for choropleth\n",
                "    choropleth_data = state_df[['state', 'ifi', 'total_enrolments']].copy()\n",
                "    \n",
                "    # State name mapping for GeoJSON compatibility\n",
                "    geojson_name_map = {\n",
                "        'Andaman And Nicobar Islands': 'Andaman & Nicobar Island',\n",
                "        'Dadra And Nagar Haveli And Daman And Diu': 'Dadara & Nagar Havelli',\n",
                "        'Jammu And Kashmir': 'Jammu & Kashmir',\n",
                "        'Delhi': 'NCT of Delhi'\n",
                "    }\n",
                "    \n",
                "    choropleth_data['state_geojson'] = choropleth_data['state'].replace(geojson_name_map)\n",
                "    \n",
                "    # Create choropleth\n",
                "    fig = px.choropleth(\n",
                "        choropleth_data,\n",
                "        geojson=india_geojson,\n",
                "        locations='state_geojson',\n",
                "        featureidkey='properties.ST_NM',\n",
                "        color='ifi',\n",
                "        color_continuous_scale='RdYlGn',\n",
                "        range_color=[0, choropleth_data['ifi'].quantile(0.9)],\n",
                "        hover_name='state',\n",
                "        hover_data={'ifi': ':.1f', 'total_enrolments': ':,.0f', 'state_geojson': False},\n",
                "        labels={'ifi': 'IFI Score'},\n",
                "        title='<b>India Identity Freshness Index (IFI) Map</b><br><sup>Green = Healthy Data | Red = Staleness Risk</sup>'\n",
                "    )\n",
                "    \n",
                "    fig.update_geos(\n",
                "        visible=False,\n",
                "        fitbounds='locations',\n",
                "        bgcolor='white'\n",
                "    )\n",
                "    \n",
                "    fig.update_layout(\n",
                "        margin={'r': 0, 't': 60, 'l': 0, 'b': 0},\n",
                "        paper_bgcolor='white',\n",
                "        font=dict(family='Arial', size=12),\n",
                "        coloraxis_colorbar=dict(\n",
                "            title='IFI Score',\n",
                "            tickvals=[0, 10, 20, 30, 40],\n",
                "            ticktext=['Critical', '10', '20', '30', 'Healthy']\n",
                "        )\n",
                "    )\n",
                "    \n",
                "    # Save as static image using kaleido\n",
                "    try:\n",
                "        fig.write_image('../visualizations/india_choropleth_ifi.png', width=1200, height=800, scale=2)\n",
                "        print(\"✓ Choropleth saved to: visualizations/india_choropleth_ifi.png\")\n",
                "    except Exception as e:\n",
                "        print(f\"⚠️ Could not save image: {e}\")\n",
                "    \n",
                "    # Display interactive version\n",
                "    fig.show()\n",
                "else:\n",
                "    print(\"Creating alternative geographic visualization in next cell...\")\n"
            ]
            print("Updated choropleth cell with kaleido export")
            break

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("✅ Notebook updated!")
