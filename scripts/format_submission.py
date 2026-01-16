"""
UIDAI Hackathon - Format Notebook for Submission Requirements
==============================================================

Hackathon requires these sections:
1. Problem Statement and Approach
2. Datasets Used
3. Methodology
4. Data Analysis and Visualisation (with code)

This script adds proper section headers to match requirements.
"""

import json

NOTEBOOK_PATH = "notebooks/UIDAI_1545.ipynb"

# Required sections per hackathon norms
SUBMISSION_SECTIONS = [
    # Section 1: Problem Statement and Approach
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 50px 40px; border-radius: 15px; text-align: center; margin-bottom: 30px;">\n',
            '\n',
            '<h1 style="font-size: 2.5em; margin-bottom: 10px; font-weight: 800;">🇮🇳 UIDAI HACKATHON 2025</h1>\n',
            '<h2 style="font-size: 1.6em; font-weight: 400; opacity: 0.95;">Identity Lifecycle Health Analysis</h2>\n',
            '<p style="font-size: 1.2em; color: #00ACC1; margin-top: 20px;">Predicting Aadhaar Data Staleness to Prevent DBT Failures</p>\n',
            '\n',
            '<hr style="border: 1px solid rgba(255,255,255,0.3); margin: 25px 80px;">\n',
            '\n',
            '<p><strong>Team ID:</strong> UIDAI_1545 | <strong>Institution:</strong> IET Lucknow</p>\n',
            '<p style="margin-top: 10px;">Anishekh Prasad (Lead) • Gaurav Pandey • Rohan Agrawal • Viraj Agrawal</p>\n',
            '</div>'
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '---\n',
            '\n',
            '# 1️⃣ PROBLEM STATEMENT AND APPROACH\n',
            '\n',
            '## 1.1 Problem Statement\n',
            '\n',
            "India's **₹10+ lakh crore Direct Benefit Transfer (DBT)** infrastructure relies on accurate Aadhaar data for authentication. When demographic or biometric information becomes **outdated (stale)**, the following cascade occurs:\n",
            '\n',
            '```\n',
            'Stale Aadhaar Data → Authentication Failure → DBT Rejection → Citizen Excluded from Welfare Benefits\n',
            '```\n',
            '\n',
            '**The Core Question:** *Which states and districts have the highest risk of stale Aadhaar data, and how can UIDAI proactively intervene before authentication failures occur?*\n',
            '\n',
            '## 1.2 Our Approach: Predictive Metrics\n',
            '\n',
            'Instead of just analyzing historical trends, we created **7 predictive metrics** that identify staleness risk **before failures happen**:\n',
            '\n',
            '| Metric | Full Name | Purpose |\n',
            '|--------|-----------|--------|\n',
            '| **IFI** | Identity Freshness Index | Overall data freshness score |\n',
            '| **CLCR** | Child Lifecycle Capture Rate | Are children getting mandatory updates? |\n',
            '| **TAES** | Temporal Access Equity Score | Weekend vs weekday service equity |\n',
            '| **UCR** | Update Completeness Ratio | Geographic coverage of services |\n',
            '| **AAUP** | Age-Adjusted Update Propensity | Population-normalized update rates |\n',
            '| **RPS** | Risk Prediction Score | Composite DBT failure probability |\n',
            '| **EGS** | Equity Gap Score | Regional disparity measure |\n',
            '\n',
            '### Key Innovation: Identity Freshness Index (IFI)\n',
            '\n',
            '```\n',
            'IFI = (Demographic Updates + Biometric Updates) / Total Enrolments\n',
            '```\n',
            '\n',
            'A single score predicting which regions have highest staleness risk.\n',
            '\n',
            '---'
        ]
    },
    
    # Section 2: Datasets Used
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '# 2️⃣ DATASETS USED\n',
            '\n',
            '## 2.1 Dataset Overview\n',
            '\n',
            'We used **all three datasets** provided by UIDAI, with a combined **4.8+ million records**:\n',
            '\n',
            '| Dataset | Records | Time Period | Source |\n',
            '|---------|---------|-------------|--------|\n',
            '| **Enrolment Data** | ~1.6M | 2024 | UIDAI Provided |\n',
            '| **Demographic Updates** | ~1.5M | 2024 | UIDAI Provided |\n',
            '| **Biometric Updates** | ~1.7M | 2024 | UIDAI Provided |\n',
            '\n',
            '## 2.2 Columns Used\n',
            '\n',
            '### Enrolment Dataset\n',
            '| Column | Description | Usage |\n',
            '|--------|-------------|-------|\n',
            '| `state` | State/UT name | Geographic aggregation |\n',
            '| `district` | District name | District-level analysis |\n',
            '| `date` | Enrolment date | Temporal patterns |\n',
            '| `age_0_5` | Enrolments age 0-5 | Age group analysis |\n',
            '| `age_5_17` | Enrolments age 5-17 | Child lifecycle capture |\n',
            '| `age_18_greater` | Enrolments 18+ | Adult population |\n',
            '\n',
            '### Demographic Update Dataset\n',
            '| Column | Description | Usage |\n',
            '|--------|-------------|-------|\n',
            '| `state`, `district` | Location | Geographic analysis |\n',
            '| `date` | Update date | Temporal patterns |\n',
            '| `demo_age_5_17` | Demo updates age 5-17 | CLCR calculation |\n',
            '| `demo_age_17_` | Demo updates 17+ | IFI calculation |\n',
            '\n',
            '### Biometric Update Dataset\n',
            '| Column | Description | Usage |\n',
            '|--------|-------------|-------|\n',
            '| `state`, `district` | Location | Geographic analysis |\n',
            '| `date` | Update date | Temporal patterns |\n',
            '| `bio_age_5_17` | Bio updates age 5-17 | Mandatory child updates |\n',
            '| `bio_age_17_` | Bio updates 17+ | IFI calculation |\n',
            '\n',
            '### External Data\n',
            '| Source | Usage |\n',
            '|--------|-------|\n',
            '| Census 2011 + Projections | Population normalization (AAUP) |\n',
            '| India GeoJSON | Choropleth mapping |\n',
            '\n',
            '---'
        ]
    },
    
    # Section 3: Methodology
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '# 3️⃣ METHODOLOGY\n',
            '\n',
            '## 3.1 Data Cleaning & Preprocessing\n',
            '\n',
            '### Step 1: Data Loading and Initial Inspection\n',
            '```python\n',
            '# Loaded all CSV files from each dataset folder\n',
            '# Combined into single DataFrames per category\n',
            'enrolment_df = pd.concat([pd.read_csv(f) for f in enrolment_files])\n',
            'demographic_df = pd.concat([pd.read_csv(f) for f in demographic_files])\n',
            'biometric_df = pd.concat([pd.read_csv(f) for f in biometric_files])\n',
            '```\n',
            '\n',
            '### Step 2: State Name Standardization\n',
            '- Mapped variant spellings to standard names\n',
            '- Example: "ANDAMAN & NICOBAR", "Andaman and Nicobar" → "Andaman And Nicobar Islands"\n',
            '\n',
            '### Step 3: Date Parsing and Feature Engineering\n',
            '```python\n',
            "# Parse dates in DD-MM-YYYY format\n",
            "df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')\n",
            "\n",
            "# Extract temporal features\n",
            "df['weekday'] = df['date'].dt.dayofweek\n",
            "df['is_weekend'] = df['weekday'] >= 5\n",
            "df['month'] = df['date'].dt.month\n",
            '```\n',
            '\n',
            '### Step 4: Missing Value Handling\n',
            '- Numeric columns: Filled with 0 (no activity)\n',
            '- Dropped records with missing state/district\n',
            '\n',
            '## 3.2 Metric Engineering\n',
            '\n',
            '### Identity Freshness Index (IFI)\n',
            '```python\n',
            'def calculate_ifi(enrolment_df, demographic_df, biometric_df, group_by="state"):\n',
            '    total_updates = demo_updates + bio_updates\n',
            '    ifi = total_updates / total_enrolments\n',
            '    return ifi\n',
            '```\n',
            '\n',
            '### Child Lifecycle Capture Rate (CLCR)\n',
            '```python\n',
            'def calculate_clcr(enrolment_df, biometric_df, expected_rate=0.20):\n',
            '    expected_updates = child_enrolments * expected_rate  # 20% annual\n',
            '    clcr = actual_child_bio_updates / expected_updates\n',
            '    return clcr\n',
            '```\n',
            '\n',
            '### Temporal Access Equity Score (TAES)\n',
            '```python\n',
            'def calculate_taes(df, value_col="enrolments"):\n',
            '    weekend_avg = df[df["is_weekend"]][value_col].mean()\n',
            '    weekday_avg = df[~df["is_weekend"]][value_col].mean()\n',
            '    taes = weekend_avg / weekday_avg\n',
            '    return taes  # 1.0 = equitable, <0.7 = inequitable\n',
            '```\n',
            '\n',
            '## 3.3 Analysis Flow\n',
            '\n',
            '```\n',
            '┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐\n',
            '│  Raw Data       │ →  │  Clean & Merge  │ →  │  Calculate      │\n',
            '│  (3 datasets)   │    │  (Standardize)  │    │  7 Metrics      │\n',
            '└─────────────────┘    └─────────────────┘    └─────────────────┘\n',
            '                                                      ↓\n',
            '┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐\n',
            '│  Recommendations│ ←  │  Risk Ranking   │ ←  │  Visualize &    │\n',
            '│  (3 Tiers)      │    │  (Priority)     │    │  Map Results    │\n',
            '└─────────────────┘    └─────────────────┘    └─────────────────┘\n',
            '```\n',
            '\n',
            '---'
        ]
    },
    
    # Section 4: Data Analysis Header
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '# 4️⃣ DATA ANALYSIS AND VISUALISATION\n',
            '\n',
            '*The following sections contain our complete analysis code, visualizations, and key findings.*\n',
            '\n',
            '---'
        ]
    }
]

# Conclusion section to add at the end
CONCLUSION_SECTION = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '---\n',
            '\n',
            '# 5️⃣ KEY FINDINGS AND RECOMMENDATIONS\n',
            '\n',
            '## 5.1 Summary of Findings\n',
            '\n',
            '| Finding | Metric Value | Impact |\n',
            '|---------|--------------|--------|\n',
            '| 🔴 Northeast has 4× lower IFI | IFI = 0.12 vs 0.47 national | 50M+ at authentication risk |\n',
            '| 🟡 8 states failing child updates | CLCR < 0.50 | Mandatory updates missed |\n',
            '| 🔵 30% weekend service reduction | TAES = 0.70 | Working citizens excluded |\n',
            '| 💰 **Total DBT at Risk** | **₹6,000+ Cr/year** | Addressable impact |\n',
            '\n',
            '## 5.2 Tiered Recommendations\n',
            '\n',
            '### Tier 1: Immediate (0-3 months)\n',
            '| Action | Owner | Target |\n',
            '|--------|-------|--------|\n',
            '| SMS awareness to 5 lowest-IFI states | UIDAI Regional | 10M citizens |\n',
            '| Extended Saturday hours pilot | State operators | Top 50 urban districts |\n',
            '\n',
            '### Tier 2: Short-term (3-6 months)\n',
            '| Action | Owner | Target |\n',
            '|--------|-------|--------|\n',
            '| School biometric drives | State Education | 8 low-CLCR states |\n',
            '| Mobile update vans | District admin | High-migration areas |\n',
            '\n',
            '### Tier 3: Policy Reform (6-12 months)\n',
            '| Action | Owner | Expected Outcome |\n',
            '|--------|-------|------------------|\n',
            '| Link Aadhaar to bank/telecom renewals | MeitY | Natural refresh cycle |\n',
            '| Public Identity Health Dashboard | UIDAI HQ | State accountability |\n',
            '\n',
            '---\n',
            '\n',
            '## 5.3 Technical Reproducibility\n',
            '\n',
            '```python\n',
            '# To reproduce this analysis:\n',
            'pip install pandas numpy matplotlib seaborn geopandas\n',
            'jupyter notebook notebooks/UIDAI_1545.ipynb\n',
            '```\n',
            '\n',
            '| Component | Details |\n',
            '|-----------|--------|\n',
            '| Data | 4.8M+ records across 3 datasets |\n',
            '| Code | Modular Python in src/ directory |\n',
            '| Metrics | 7 engineered predictive metrics |\n',
            '| Visualizations | 25+ decision-driven charts |\n',
            '\n',
            '---\n',
            '\n',
            '<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-top: 40px;">\n',
            '<h2>Thank You for Reviewing Our Submission</h2>\n',
            '<p style="font-size: 1.1em; opacity: 0.9;">We built a prediction system, not just a trend report.</p>\n',
            '<p style="margin-top: 15px;"><strong>Team UIDAI_1545</strong> | IET Lucknow</p>\n',
            '<p style="font-style: italic; opacity: 0.7;">"From descriptive to predictive — specific districts, specific actions, specific timeline"</p>\n',
            '</div>'
        ]
    }
]


def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(notebook, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

def main():
    print("=" * 60)
    print("Formatting Notebook for Hackathon Submission")
    print("=" * 60)
    print("\nRequired sections:")
    print("  1. Problem Statement and Approach")
    print("  2. Datasets Used")
    print("  3. Methodology")
    print("  4. Data Analysis and Visualisation")
    print("  5. Key Findings and Recommendations")
    
    notebook = load_notebook(NOTEBOOK_PATH)
    original_count = len(notebook['cells'])
    print(f"\n📂 Original cells: {original_count}")
    
    # Insert submission sections at the beginning
    print("\n➕ Adding structured sections at beginning...")
    for i, cell in enumerate(SUBMISSION_SECTIONS):
        notebook['cells'].insert(i, cell)
    
    # Add conclusion at the end
    print("➕ Adding conclusions at end...")
    for cell in CONCLUSION_SECTION:
        notebook['cells'].append(cell)
    
    new_count = len(notebook['cells'])
    print(f"📊 New total cells: {new_count}")
    
    save_notebook(notebook, NOTEBOOK_PATH)
    print(f"\n✅ Notebook saved: {NOTEBOOK_PATH}")
    
    print("\n" + "=" * 60)
    print("SUBMISSION SECTIONS ADDED:")
    print("=" * 60)
    print("  ✅ 1. Problem Statement and Approach")
    print("  ✅ 2. Datasets Used (all columns documented)")
    print("  ✅ 3. Methodology (with code snippets)")
    print("  ✅ 4. Data Analysis header")
    print("  ✅ 5. Key Findings and Recommendations")
    print("=" * 60)
    print("\nNow export to HTML with code visible:")
    print("  jupyter nbconvert --to html notebooks/UIDAI_1545.ipynb")

if __name__ == "__main__":
    main()
