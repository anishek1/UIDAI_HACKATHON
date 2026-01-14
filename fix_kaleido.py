"""Fix kaleido message in notebook"""
import json
from pathlib import Path

notebook_path = Path("notebooks/uidai_analysis.ipynb")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'kaleido not installed' in source:
            # Replace the try/except block with just the save command
            new_source = source.replace(
                """    # Also save as static image
    try:
        fig.write_image('../visualizations/20_india_choropleth.png', scale=2)
        print('✓ Saved: 20_india_choropleth.png')
    except:
        print('Note: Could not save static image (kaleido not installed)')""",
                """    # Save as static image
    fig.write_image('../visualizations/20_india_choropleth.png', scale=2)
    print('✓ Saved: 20_india_choropleth.png')"""
            )
            cell['source'] = new_source.split('\n')
            cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                             for i, line in enumerate(cell['source'])]
            print("✅ Fixed kaleido message")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("✅ Notebook updated")
