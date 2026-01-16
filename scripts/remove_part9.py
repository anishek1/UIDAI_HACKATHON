"""
Remove the Part 9 Enhanced Features section from the notebook.
This removes the cells that say "PART 9: Enhanced Features (v3.0)" 
and the bullet list that follows it.
"""

import json

NOTEBOOK_PATH = "notebooks/MASTER_file_FINAL.ipynb"

def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(notebook, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

def find_and_remove_part9_cells(notebook):
    """Find and remove the Part 9 Enhanced Features header and its content."""
    cells_to_remove = []
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell.get('source', []))
            
            # Find the Part 9 header cell
            if 'PART 9: Enhanced Features' in source:
                cells_to_remove.append(i)
                print(f"  Found Part 9 header at cell {i}")
    
    # Remove cells in reverse order to maintain indices
    for idx in sorted(cells_to_remove, reverse=True):
        del notebook['cells'][idx]
        print(f"  ✓ Removed cell {idx}")
    
    return notebook, len(cells_to_remove)

def main():
    print("=" * 50)
    print("Removing Part 9 Enhanced Features Section")
    print("=" * 50)
    
    notebook = load_notebook(NOTEBOOK_PATH)
    original_count = len(notebook['cells'])
    print(f"\n📂 Original cells: {original_count}")
    
    notebook, removed = find_and_remove_part9_cells(notebook)
    
    new_count = len(notebook['cells'])
    print(f"\n📊 Cells removed: {removed}")
    print(f"📊 New total: {new_count}")
    
    save_notebook(notebook, NOTEBOOK_PATH)
    print(f"\n✅ Notebook saved: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    main()
