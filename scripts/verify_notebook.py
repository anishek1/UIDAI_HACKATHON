import json

with open(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
print("=" * 60)

for i, cell in enumerate(nb['cells']):
    cell_type = cell['cell_type'].upper()
    if cell['source']:
        first_line = cell['source'][0][:50].replace('\n', ' ')
    else:
        first_line = "(empty)"
    print(f"[{i+1:2}] {cell_type:8} | {first_line}...")
