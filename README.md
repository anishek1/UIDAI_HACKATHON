# 🇮🇳 UIDAI Hackathon 2025 — Identity Lifecycle Health Analysis

## 🎯 Predicting Aadhaar Data Staleness to Prevent DBT Failures

**Team ID:** UIDAI_1545 | **Institution:** IET Lucknow

---

### 👥 Team

| Role | Name |
|------|------|
| **Team Lead** | Anishekh Prasad |
| Member | Gaurav Pandey |
| Member | Rohan Agrawal |
| Member | Viraj Agrawal |

---

## 🔬 The Problem

India's ₹10+ lakh crore DBT infrastructure depends on **accurate Aadhaar data**. When demographic or biometric data becomes outdated, authentication fails → DBT fails → citizens are excluded.

**We predict where this risk is highest**, before failures occur.

---

## 💡 Our Innovation: Identity Freshness Index (IFI)

We synthesize **4.8M+ records** across three datasets into a predictive metric:

```
IFI = (Demographic Updates + Biometric Updates) / Cumulative Enrolments
```

| IFI Score | Risk Level | Required Action |
|-----------|-----------|-----------------|
| < 0.20 | 🔴 Critical | Immediate intervention |
| 0.20–0.40 | 🟡 At Risk | Prioritized outreach |
| > 0.40 | 🟢 Healthy | Maintain operations |

---

## 📊 Key Findings

| Finding | Impact | Metric |
|---------|--------|--------|
| Northeast IFI = 0.12 vs National 0.47 | 50M+ at authentication risk | Identity Freshness |
| 8 states missing child lifecycle capture | Mandatory update gaps | CLCR Score |
| 30% weekend service reduction | Working citizen exclusion | Temporal Access |

**Projected Impact:** Identification of ₹500+ Cr in at-risk DBT districts.

---

## 📁 Project Structure

```
UIDAI_HACKATHON/
├── notebooks/
│   ├── uidai_analysis.ipynb          # Core analysis
│   └── uidai_analysis_final.ipynb    # With outputs
├── src/
│   ├── data_loader.py                # Data utilities
│   ├── metrics.py                    # Engineered metrics (IFI, CLCR, etc.)
│   └── visualization.py              # Chart generation
├── docs/
│   └── problem_statement.md          # Full problem framing
├── visualizations/                   # 20 decision-driven charts
└── data/                            # Datasets (1M + 2M + 1.8M rows)
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
jupyter notebook notebooks/uidai_analysis_final.ipynb
```

---

## 🎯 Research Questions

1. **Where are Aadhaar records most likely stale?** → IFI Mapping
2. **Are children getting mandatory biometric updates?** → CLCR Analysis
3. **Does weekend service create temporal inequity?** → TAES Metric
4. **Which districts need immediate intervention?** → Priority Matrix

---

## 📈 Deliverables

- **Identity Freshness Index** — State and district rankings
- **Child Lifecycle Coverage Rate** — Tracking mandatory updates
- **District Priority Matrix** — Named intervention recommendations
- **₹ Impact Quantification** — DBT at risk estimates

---

**UIDAI Hackathon 2025** | *From descriptive to predictive*
