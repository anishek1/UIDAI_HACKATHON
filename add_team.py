"""
Add team details to notebook
"""
import json
from pathlib import Path

notebook_path = Path("notebooks/uidai_analysis.ipynb")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and update the header cell
for cell in nb['cells']:
    source = ''.join(cell.get('source', []))
    
    if 'UIDAI Hackathon 2025' in source and 'Analysis by' in source:
        # Replace old author line with team info
        new_source = source.replace(
            '**UIDAI Hackathon 2025** | Analysis by Anish | January 2026',
            '''**UIDAI Hackathon 2025** | Team ID: UIDAI_1545

<div class="box">

### 👥 Team Details

| Role | Name |
|------|------|
| **Team Lead** | Anishekh Prasad |
| Member | Gaurav Pandey |
| Member | Rohan Agrawal |
| Member | Viraj Agrawal |

**Institution:** Institute of Engineering and Technology, Lucknow

</div>'''
        )
        
        cell['source'] = new_source.split('\n')
        cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                         for i, line in enumerate(cell['source'])]
        print("✅ Updated header with team details")
        break

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("✅ Team details added to notebook")
