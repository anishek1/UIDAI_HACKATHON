"""
Script to add "Premium" features to MASTER_file.ipynb:
1. Table of Contents (ToC)
2. Methodology Architecture Diagram (Mermaid)
3. CSS Styling for better PDF look
"""
import json
from pathlib import Path

notebook_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb')

# Load existing notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Custom CSS for PDF-like feel (Bigger headers, better spacing)
css_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "<style>\n",
        "    h1 { font-size: 2.5em !important; color: #2c3e50 !important; border-bottom: 2px solid #e74c3c !important; padding-bottom: 10px; }\n",
        "    h2 { font-size: 2.0em !important; color: #34495e !important; margin-top: 40px !important; }\n",
        "    h3 { font-size: 1.5em !important; color: #7f8c8d !important; }\n",
        "    .alert-box { background-color: #f1f8ff; border-left: 5px solid #0366d6; padding: 15px; margin: 20px 0; }\n",
        "    .metric-box { background-color: #fcf8e3; border: 1px solid #faebcc; padding: 15px; border-radius: 5px; text-align: center; }\n",
        "</style>"
    ]
}

# 2. Table of Contents
toc_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 📑 Table of Contents\n",
        "\n",
        "| Section | Page Content |\n",
        "|:---|:---|\n",
        "| **1. Executive Brief** | Project Drishti, Hero Metrics, & The Verdict |\n",
        "| **2. Problem Statement** | The 'Identity Staleness' Crisis |\n",
        "| **3. Datasets Used** | Enrolment, Demographic, & Biometric Data Sources |\n",
        "| **4. Methodology** | Pipeline Architecture & The IFI Formula |\n",
        "| **5. Analysis & Findings** | Regional, Lifecycle, & Temporal Insights |\n",
        "| **6. Visual Evidence** | Maps, Priority Matrices, & Trends |\n",
        "| **7. Recommendations** | 3-Tiered Strategy & Financial Impact |\n",
        "| **Appendix** | Code & Technical Implementation |"
    ]
}

# 3. Methodology Diagram (Image/Markdown representation since Mermaid support in basic nbconvert can be tricky without extensions, 
# but we can use a text-based ASCII or block architecture which translates perfectly to PDF)
method_diagram_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🏗️ Solution Architecture\n",
        "\n",
        "```mermaid\n",
        "graph TD\n",
        "    A[Raw UIDAI Data] -->|Enrolment + Updates| B(Data Cleaning);\n",
        "    B -->|State Standardization| C{Feature Engineering};\n",
        "    C -->|Calculate| D[Identity Freshness Index];\n",
        "    C -->|Calculate| E[Child Lifecycle Rate];\n",
        "    D --> F[Risk Scoring Model];\n",
        "    E --> F;\n",
        "    F -->|Output| G[District Priority Matrix];\n",
        "    F -->|Output| H[₹ Financial Risk Est.];\n",
        "```\n",
        "*(Data Pipeline Flow: From Raw Logs to Strategic Insights)*"
    ]
}

# Insert CSS at top
nb['cells'].insert(0, css_cell)

# Insert ToC after the Executive Brief (which is usually the first real content cell)
nb['cells'].insert(2, toc_cell)

# Find Methodology section and insert diagram
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and "## 3. Methodology" in "".join(cell['source']):
        nb['cells'].insert(i + 1, method_diagram_cell)
        break

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("✅ Added Premium Features: CSS Styling, ToC, and Architecture Diagram")
