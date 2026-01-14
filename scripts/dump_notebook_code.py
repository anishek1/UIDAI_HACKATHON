
import nbformat

nb_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'
out_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\scripts\notebook_code_dump.py'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

with open(out_path, 'w', encoding='utf-8') as f:
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            f.write(f"\n# CELL {i}\n")
            f.write(cell.source)
            f.write("\n" + "="*80 + "\n")
