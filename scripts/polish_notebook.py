"""
Script to polish MASTER_file.ipynb with "Human-Centric" Consulting Report phrasing.
"""
import json
from pathlib import Path

notebook_path = Path(r'c:\Users\anish\Desktop\UIDAI_HACKATHON\notebooks\MASTER_file.ipynb')

# Load existing notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Define the new markdown content map
# Keys are substrings to identify the cell, Values are the new content
updates = {
    "# 🎯 Problem Statement": [
        "# 🇮🇳 Project Drishti: The Identity Freshness Index (IFI)\n",
        "### *Unlocking Societal Trends in Aadhaar: Predicting Data Staleness to Prevent DBT Leakages*\n",
        "\n",
        "---\n",
        "\n",
        "> **Team ID:** UIDAI_1545\n",
        "> **Theme:** Access & Equity | **Focus:** Identity Lifecycle Health\n",
        "\n",
        "---\n",
        "\n",
        "## 🚀 Executive Brief\n",
        "\n",
        "**The Problem:** India's Direct Benefit Transfer (DBT) infrastructure relies entirely on accurate identity data. When citizens fail to update their biometrics (at age 5/15) or demographics (address/mobile), authentication fails, and welfare delivery breaks. We call this silent crisis **\"Identity Staleness.\"**\n",
        "\n",
        "**The Solution:** We built the **Identity Freshness Index (IFI)**—a predictive score that flags districts where data is \"stale\" and authentication failure is imminent.\n",
        "\n",
        "**⚡ Key Verdict:**\n",
        "*   **💸 Financial Risk:** An estimated **₹6,142 Crores** of DBT is at risk annually due to stale data.\n",
        "*   **🚨 Critical Zones:** We identified **20 Districts** (e.g., Medinipur West, SPSR Nellore) requiring immediate intervention.\n",
        "*   **📅 The Weekend Gap:** Service availability drops significantly on weekends, disproportionately affecting the working class."
    ],
    "## 1. Problem Statement & Approach": [
        "---\n",
        "\n",
        "## 1. The Challenge: Why \"Freshness\" Matters\n",
        "\n",
        "Most analysis focuses on *growth* (e.g., \"How many new enrolments?\"). We argue that since Aadhaar has >99% saturation, the real metric of success is now **Maintenance**.\n",
        "\n",
        "### 🔍 The Core Question\n",
        "If a citizen enrolled 10 years ago and hasn't updated their data since, can we rely on that identity today? \n",
        "\n",
        "> **Our Hypothesis:** Stale data leads to authentication failures. By identifying *where* data is stale, we can prevent those failures."
    ],
    "## 2. Datasets Used": [
        "---\n",
        "\n",
        "## 2. The Evidence Base\n",
        "\n",
        "We utilized three primary datasets provided by UIDAI. Instead of treating them in isolation, we linked them to build a comprehensive view of the lifecycle.\n",
        "\n",
        "| Dataset | What it Tells Us | Key Columns |\n",
        "|:---|:---|:---|\n",
        "| **Enrolment** | The Baseline Volume | `date`, `state`, `district`, `age_group` |\n",
        "| **Demographic** | The \"Soft\" Updates | `mobile_update`, `address_change` |\n",
        "| **Biometric** | The Critical Updates | `mandatory_biometric_update` |"
    ],
    "## 3. Methodology": [
        "---\n",
        "\n",
        "## 3. Our Approach: From Raw Logs to Risk Scores\n",
        "\n",
        "We didn't just count rows. We engineered a robust pipeline to measure health.\n",
        "\n",
        "### 🏗️ The 3-Step Pipeline\n",
        "1.  **Standardization:** Mapping 50+ state name variations (e.g., \"Telengana\" vs \"Telangana\") to a single canonical list.\n",
        "2.  **Transformation:** Aggregating daily logs into monthly/yearly trends and flagging weekends.\n",
        "3.  **Metric Engineering:** Creating the **IFI Score**.\n",
        "\n",
        "```python\n",
        "# The Project Drishti Formula\n",
        "IFI = (Demographic_Updates + Biometric_Updates) / Total_Enrolments\n",
        "```"
    ],
    "## 3.1 Data Quality Assessment": [
         "---\n",
         "\n",
         "## 3.1 Data Integrity Check\n",
         "\n",
         "Before analysis, we rigorously tested the data quality. Good insights require good data. We checked for missing values, duplicates, and illogical ranges (e.g., negative ages)."
    ],
    "## 4. Univariate Analysis": [
        "---\n",
        "\n",
        "## 4. 📉 Insight 1: The 'Weekend Gap' in Access\n",
        "\n",
        "When we analyze the daily heartbeat of enrolments, a clear pattern emerges. The dips aren't random errors—they are Sundays.\n",
        "\n",
        "> **💡 Why this matters:** Working-class citizens often cannot afford to take a day off work (Mon-Fri) to visit a Kendra. If services are offline on weekends, we are effectively excluding them."
    ],
    "## 5. Bivariate Analysis": [
        "---\n",
        "\n",
        "## 5. 🗺️ Insight 2: The Regional Divide\n",
        "\n",
        "India is not uniform. When we compare **Enrolment Volume** vs. **Update Rates**, distinct regional clusters emerge.\n",
        "\n",
        "*   **High Volume, Low Updates:** These contain our \"Critical Priority\" states.\n",
        "*   **Balanced:** States with healthy lifecycle management."
    ],
    "## 6. Trivariate Analysis": [
        "---\n",
        "\n",
        "## 6. 👶 Insight 3: The 'Lost Generation' of Biometrics\n",
        "\n",
        "This is our most critical finding regarding children. \n",
        "\n",
        "Children **must** update biometrics at age 5 and 15. By overlaying Age × Update Type, we can calculate the **Child Lifecycle Capture Rate (CLCR)**. Low CLCR means millions of children effectively have \"expired\" biometrics."
    ],
    "## 7. Engineered Metrics": [
        "---\n",
        "\n",
        "## 7. The Engine: Identity Freshness Index (IFI)\n",
        "\n",
        "We combined our insights into a single, trackable score for every state."
    ],
    "## 7.4 Statistical Confidence Analysis": [
        "---\n",
        "\n",
        "## 7.1 Statistical Rigor\n",
        "\n",
        "We computed 95% confidence intervals to ensure our rankings aren't just statistical noise. The results are significant."
    ],
    "## 8. Visualizations": [
        "---\n",
        "\n",
        "## 8. Visual Evidence: Mapping the Crisis\n",
        "\n",
        "We generated 30+ charts. Here are the most impactful ones driving our recommendations."
    ],
    "## 8.1 District-Level Priority Analysis": [
        "---\n",
        "\n",
        "## 8.1 🎯 The 'Red Zone': Top 20 Priority Districts\n",
        "\n",
        "State averages hide local problems. We drilled down to the district level. \n",
        "\n",
        "> **The Strategy:** If UIDAI focuses resources on just these 20 districts, we can achieve maximum impact on the national IFI score."
    ],
    "## 8.2 Geographic Visualization": [
        "---\n",
        "\n",
        "## 8.2 🗺️ The National Heatmap\n",
        "\n",
        "A geographic view of Identity Freshness. Red areas represent high staleness risk."
    ],
    "## 9. Key Findings & Insights": [
        "---\n",
        "\n",
        "## 9. Executive Verdict: Six Key Takeaways\n",
        "\n",
        "If you only read one section, read this. These are the fundamental truths revealed by the data."
    ],
    "## 10. Recommendations": [
        "---\n",
        "\n",
        "## 10. The Playbook: From Insight to Action\n",
        "\n",
        "Analysis is useless without action. We propose a 3-Tiered Strategy for UIDAI."
    ]
}

# Iterate and apply updates
count = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        content = "".join(cell['source'])
        
        # Check against our map
        for key, new_content in updates.items():
            if key in content:
                # Special handling for "Key Findings" to keeping the dynamic content if any
                # But here we are replacing the intro text primarily.
                # Let's replace the whole cell logic for the match
                cell['source'] = [line + "\n" for line in new_content] # Add newlines for safety
                count += 1
                print(f"✓ Updated section: {key.splitlines()[0]}...")
                break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("="*60)
print(f"✨ Makeover Complete! Updated {count} sections.")
print("The notebook now reads like a human-written consulting report.")
