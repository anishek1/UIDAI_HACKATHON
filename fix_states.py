"""
Fix state name standardization in notebook
"""
import json
from pathlib import Path

notebook_path = Path("notebooks/uidai_analysis.ipynb")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# State name standardization code to add after data loading
STATE_STANDARDIZATION_CODE = '''
# ============================================
# STATE NAME STANDARDIZATION
# ============================================
# Fix inconsistent state name spellings

state_mapping = {
    # West Bengal variations
    'Westbengal': 'West Bengal',
    'West Bangal': 'West Bengal',
    'west bengal': 'West Bengal',
    
    # Daman & Diu variations
    'Daman And Diu': 'Daman & Diu',
    'daman and diu': 'Daman & Diu',
    'Daman and Diu': 'Daman & Diu',
    
    # Dadra & Nagar Haveli variations
    'Dadra And Nagar Haveli': 'Dadra & Nagar Haveli',
    'Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli',
    'dadra and nagar haveli': 'Dadra & Nagar Haveli',
    
    # Andaman variations
    'Andaman And Nicobar Islands': 'Andaman & Nicobar',
    'Andaman & Nicobar Islands': 'Andaman & Nicobar',
    
    # Jammu variations
    'Jammu And Kashmir': 'Jammu & Kashmir',
    'jammu and kashmir': 'Jammu & Kashmir',
    
    # Delhi variations
    'Nct Of Delhi': 'Delhi',
    'NCT of Delhi': 'Delhi',
    'NCT OF DELHI': 'Delhi',
    
    # Other common variations
    'Pondicherry': 'Puducherry',
    'Orissa': 'Odisha',
    'Uttaranchal': 'Uttarakhand',
}

# Apply standardization to all dataframes
for df in [df_enrolment, df_demographic, df_biometric]:
    if 'state' in df.columns:
        df['state'] = df['state'].str.strip().str.title()
        df['state'] = df['state'].replace(state_mapping)

print("✅ State names standardized")
print(f"   Unique states in enrolment: {df_enrolment['state'].nunique()}")
'''

# Find the cell after data loading and add standardization
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'print_data_summary' in source or 'Data loaded successfully' in source:
            # Insert new cell after this one
            new_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": STATE_STANDARDIZATION_CODE.split('\n')
            }
            new_cell['source'] = [line + '\n' if j < len(new_cell['source'])-1 else line 
                                  for j, line in enumerate(new_cell['source'])]
            nb['cells'].insert(i + 1, new_cell)
            print(f"✅ Added state standardization cell at position {i+1}")
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("✅ State name standardization added to notebook")
