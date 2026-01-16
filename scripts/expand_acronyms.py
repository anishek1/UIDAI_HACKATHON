"""
Replace metric acronyms with full forms (acronym) in the notebook.
Example: IFI → Identity Freshness Index (IFI)
"""

import json
import re

NOTEBOOK_PATH = "notebooks/MASTER_file_FINAL.ipynb"

# Mapping of acronyms to full forms
REPLACEMENTS = {
    # Primary metrics - be careful with word boundaries
    r'\bIFI\b': 'Identity Freshness Index (IFI)',
    r'\bCLCR\b': 'Child Lifecycle Capture Rate (CLCR)',
    r'\bTAES\b': 'Temporal Access Equity Score (TAES)',
    r'\bUCR\b': 'Update Completeness Ratio (UCR)',
    r'\bAAUP\b': 'Age-Adjusted Update Propensity (AAUP)',
    r'\bRPS\b': 'Risk Prediction Score (RPS)',
    r'\bEGS\b': 'Equity Gap Score (EGS)',
}

# Patterns to skip (already in full form or in code)
SKIP_PATTERNS = [
    r'Identity Freshness Index \(IFI\)',
    r'Child Lifecycle Capture Rate \(CLCR\)',
    r'Temporal Access Equity Score \(TAES\)',
    r'Update Completeness Ratio \(UCR\)',
    r'Age-Adjusted Update Propensity \(AAUP\)',
    r'Risk Prediction Score \(RPS\)',
    r'Equity Gap Score \(EGS\)',
]

def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(notebook, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

def replace_in_text(text):
    """Replace acronyms with full forms, but skip if already expanded."""
    # Check if already has full form
    for skip in SKIP_PATTERNS:
        if re.search(skip, text):
            # This text already has full form, be more careful
            pass
    
    result = text
    for pattern, replacement in REPLACEMENTS.items():
        # Don't replace if already in full form nearby
        # Simple approach: replace first occurrence only if not already expanded
        result = re.sub(pattern, replacement, result, count=1)
    
    return result

def smart_replace(text):
    """
    Smarter replacement that avoids double-expanding.
    Only replace if the acronym isn't already followed by its expansion.
    """
    result = text
    
    for acronym, full_form in REPLACEMENTS.items():
        # Extract just the acronym letters
        acr = acronym.replace(r'\b', '')
        
        # Skip if full form already present
        if full_form in result:
            continue
        
        # Replace standalone acronyms
        result = re.sub(acronym, full_form, result)
    
    return result

def process_notebook(notebook):
    """Process all markdown cells in the notebook."""
    changes = 0
    
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown':
            # Process source
            if isinstance(cell['source'], list):
                new_source = []
                for line in cell['source']:
                    new_line = smart_replace(line)
                    if new_line != line:
                        changes += 1
                    new_source.append(new_line)
                cell['source'] = new_source
            else:
                new_source = smart_replace(cell['source'])
                if new_source != cell['source']:
                    changes += 1
                cell['source'] = new_source
    
    return notebook, changes

def main():
    print("=" * 60)
    print("Replacing Acronyms with Full Forms")
    print("=" * 60)
    
    print("\nReplacements to make:")
    for acr, full in REPLACEMENTS.items():
        acr_clean = acr.replace(r'\b', '')
        print(f"  {acr_clean} → {full}")
    
    notebook = load_notebook(NOTEBOOK_PATH)
    print(f"\n📂 Loaded: {NOTEBOOK_PATH}")
    print(f"📊 Total cells: {len(notebook['cells'])}")
    
    notebook, changes = process_notebook(notebook)
    
    print(f"\n✏️ Changes made: {changes}")
    
    save_notebook(notebook, NOTEBOOK_PATH)
    print(f"✅ Notebook saved: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    main()
