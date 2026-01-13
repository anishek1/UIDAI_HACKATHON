# 🇮🇳 UIDAI Hackathon - Aadhaar Data Analysis

## Bridging the Digital Identity Gap

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

</div>

---

## What's This About?

I analyzed nearly **5 million data points** from UIDAI's Aadhaar datasets to find patterns that could actually help improve the system. The goal was simple: figure out where the gaps are and what can be done about them.

### What I Found

| Finding | What It Means |
|---------|---------------|
| **North vs Northeast gap** | Northern states have 15x more enrolments - NE needs more attention |
| **Weekend drop-off** | 30% fewer people enrol on weekends - probably need extended hours |
| **Kids lagging behind** | Some states have really low child enrolment - school drives could help |
| **Biometric updates vary a lot** | Big differences in how states handle child biometric updates |

### The Numbers

- ~2.5M enrolments analyzed
- ~10M demographic updates
- ~9M biometric updates
- 36 states/UTs covered
- 700+ districts

---

## Project Files

```
UIDAI_HACKATHON/
├── README.md                    # You're reading this
├── requirements.txt             # What you need to install
├── data/
│   ├── raw/                     # Original CSVs (12 files)
│   └── processed/               # Cleaned versions
├── notebooks/
│   ├── uidai_analysis.ipynb     # The code
│   └── uidai_analysis_final.ipynb  # With all outputs (5.6MB)
├── src/
│   ├── data_loader.py           # Helper functions
│   └── visualization.py         # Chart templates
└── visualizations/              # 19 charts saved as PNGs
```

---

## Charts I Made

19 visualizations covering:
- Basic stats (age groups, state comparisons)
- Time patterns (daily trends, weekday vs weekend)
- Deep dives (district level, heatmaps, correlation)
- The interesting stuff (regional gaps, accessibility issues)

---

## How to Run This

```bash
# 1. Get the code
git clone https://github.com/yourusername/UIDAI_HACKATHON.git
cd UIDAI_HACKATHON

# 2. Install packages
pip install -r requirements.txt

# 3. Add the data to data/raw/

# 4. Open the notebook
jupyter notebook notebooks/uidai_analysis.ipynb
```

---

## What UIDAI Could Do

**Quick fixes:**
- Keep centres open on weekends
- Run enrolment drives in schools

**Bigger projects:**
- Mobile units for Northeast
- Dashboard to track demand
- Reminder system for kids' biometric updates

---

## Built With

- Python, Pandas, Matplotlib, Seaborn, Plotly, Jupyter

---

**By Anish | UIDAI Hackathon 2025**
