
import nbformat

nb_path = r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file_FINAL.ipynb'

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    print(f"Total cells: {len(nb.cells)}")
    
    plotting_keywords = ['plt.', 'sns.', '.plot(', 'matplotlib', 'seaborn', 'Figure', 'Axes']
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = cell.source
            if any(kw in source for kw in plotting_keywords):
                print(f"--- Cell {i} ---")
                print(source[:500]) # Print first 500 chars
                print("...\n")

except Exception as e:
    print(f"Error reading notebook: {e}")
