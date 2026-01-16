# 🇮🇳 UIDAI Hackathon 2025 — Identity Lifecycle Health Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Competition%20Ready-brightgreen)

## 🎯 Predicting Aadhaar Data Staleness to Prevent DBT Failures

**Team ID:** UIDAI_1545 | **Institution:** IET Lucknow

> *"From descriptive to predictive — specific districts, specific actions, specific timeline"*

---

## ⚡ Quick Results

| Finding | Metric | Impact |
|---------|--------|--------|
| 🔴 Northeast IFI Gap | IFI = 0.12 vs National 0.47 | 50M+ at authentication risk |
| 🟡 8 States Below CLCR | Child lifecycle capture failing | Mandatory updates missed |
| 🔵 30% Weekend Drop | Working citizen exclusion | Temporal inequity |
| 💰 **₹6,000 Cr/year** | DBT at risk from staleness | Addressable impact |

---

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/your-repo/UIDAI_HACKATHON.git
cd UIDAI_HACKATHON
pip install -r requirements.txt

# Run analysis
jupyter notebook notebooks/MASTER_file_FINAL.ipynb

# View interactive dashboard
start dashboard/index.html  # Windows
open dashboard/index.html   # macOS
```

---

## 👥 Team

| Role | Name |
|------|------|
| **Team Lead** | Anishekh Prasad |
| Member | Gaurav Pandey |
| Member | Rohan Agrawal |
| Member | Viraj Agrawal |

---

## 🔬 The Problem

India's ₹10+ lakh crore DBT infrastructure depends on **accurate Aadhaar data**. When demographic or biometric data becomes outdated:

```
Stale Data → Authentication Failure → DBT Rejection → Citizen Exclusion
```

**We predict where this risk is highest**, before failures occur.

---

## 💡 Our Innovation: 7 Engineered Metrics

We synthesize **4.8M+ records** across three datasets into predictive metrics:

### Core Metrics
| Metric | Formula | Purpose |
|--------|---------|---------|
| **IFI** | (Demo + Bio Updates) / Enrolments | Identity Freshness Index |
| **CLCR** | Child Bio Updates / Expected | Child Lifecycle Capture Rate |
| **TAES** | Weekend Avg / Weekday Avg | Temporal Access Equity Score |
| **UCR** | Active Districts / Total | Update Completeness Ratio |
| **AAUP** | Per-capita vs National Avg | Age-Adjusted Update Propensity |

### 🆕 New in v3.0
| Metric | Purpose |
|--------|---------|
| **RPS** | Risk Prediction Score - DBT failure probability |
| **EGS** | Equity Gap Score - Regional disparity measure |

---

## 📊 IFI Risk Categories

| IFI Score | Risk Level | Required Action |
|-----------|-----------|-----------------| 
| < 0.15 | 🔴 Critical | Immediate intervention |
| 0.15–0.25 | 🟡 At Risk | Prioritized outreach |
| 0.25–0.40 | 🟢 Healthy | Regular monitoring |
| > 0.40 | 🔵 Optimal | Maintain operations |

---

## 📁 Project Structure

```
UIDAI_HACKATHON/
├── 📓 notebooks/
│   └── MASTER_file_FINAL.ipynb    # Complete analysis
├── 📊 dashboard/                   # 🆕 Interactive web dashboard
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── 🔧 src/
│   ├── metrics.py                  # 7 engineered metrics
│   ├── premium_viz.py              # 🆕 Enhanced visualizations
│   ├── visualization.py            # Chart generation
│   ├── utils.py                    # 🆕 Utility functions
│   ├── data_loader.py              # Data utilities
│   └── state_mapping.py            # Geographic mapping
├── 📈 visualizations/              # 28 decision-driven charts
├── 📄 docs/
│   ├── problem_statement.md
│   ├── analytical_design.md
│   ├── action_framework.md
│   ├── jury_defense.md
│   └── visualization_design.md
├── 💾 data/
│   ├── raw/                        # 3 datasets (4.8M rows)
│   └── processed/                  # Computed metrics
├── config.yaml                     # Central configuration
└── requirements.txt
```

---

## 🖥️ Interactive Dashboard

Open `dashboard/index.html` in any browser for:

- 📊 **KPI Cards** with animated counters
- 🗺️ **Interactive Charts** with Chart.js
- 🔍 **State Comparison Tool** 
- 🎛️ **Region & Risk Filters**
- 📥 **Data Export** functionality

---

## 🎯 Research Questions Answered

1. **Where are Aadhaar records most likely stale?** → IFI Mapping
2. **Are children getting mandatory biometric updates?** → CLCR Analysis
3. **Does weekend service create temporal inequity?** → TAES Metric
4. **Which districts need immediate intervention?** → Priority Matrix
5. **🆕 What is the predicted DBT failure risk?** → RPS Score

---

## 📈 Key Deliverables

- ✅ **Identity Freshness Index** — State and district rankings
- ✅ **Child Lifecycle Coverage Rate** — Tracking mandatory updates
- ✅ **District Priority Matrix** — Named intervention recommendations
- ✅ **₹ Impact Quantification** — DBT at risk estimates
- ✅ **🆕 Risk Prediction Score** — Proactive failure prevention
- ✅ **🆕 Interactive Dashboard** — Browser-based visualization

---

## 🔧 Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
geopandas>=0.13.0
scipy>=1.10.0
pyyaml>=6.0
```

---

## 📄 License

MIT License - See LICENSE file for details.

---

**UIDAI Hackathon 2025** | *Predicting identity staleness to protect ₹10 lakh crore in DBT*

**Team UIDAI_1545** | IET Lucknow
