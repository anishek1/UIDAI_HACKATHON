# 🚀 UIDAI Hackathon — 5-Minute Quick Tour

> **For Jury Members: A fast-track guide to our Identity Lifecycle Health Analysis**

---

## ⚡ What We Built

We created **7 predictive metrics** that identify where Aadhaar data staleness risks DBT failures — before they happen.

**Key Innovation:** Our **Identity Freshness Index (IFI)** synthesizes enrolment, demographic, and biometric data into a single predictive score.

---

## 🎯 Core Findings (30 seconds)

| 🔴 Critical | 🟡 Concerning | 💰 Impact |
|-------------|---------------|-----------|
| Northeast IFI = 0.12 (vs 0.47 national) | 8 states failing child lifecycle capture | ₹6,000 Cr DBT at risk annually |
| 50M+ citizens at authentication risk | 30% weekend service reduction | Addressable with targeted interventions |

---

## 📊 Demo Flow

### Step 1: Open Interactive Dashboard
```
dashboard/index.html
```
- See animated KPI cards
- Explore state comparisons
- Filter by region/risk level

### Step 2: View Key Visualizations
Located in `visualizations/` folder:

| Chart | What It Shows |
|-------|---------------|
| `chart1_ifi_rankings.png` | State-wise IFI with risk colors |
| `india_choropleth_ifi.png` | Geographic staleness risk |
| `chart6_metrics_heatmap.png` | Multi-metric comparison |
| `district_priority.png` | Intervention priority matrix |

### Step 3: Run Notebook (Optional)
```
notebooks/MASTER_file_FINAL.ipynb
```
Reproduces all analysis from raw data.

---

## 💡 What Makes Us Different

| Other Teams | Our Approach |
|-------------|--------------|
| Trend analysis | **Predictive metrics** |
| Generic insights | **Named districts + timelines** |
| Describe data | **Quantify ₹ impact** |
| 5 charts | **28 decision-driven visualizations** |
| Static visuals | **Interactive web dashboard** |

---

## 🎯 Our 7 Metrics

1. **IFI** — Identity Freshness Index
2. **CLCR** — Child Lifecycle Capture Rate  
3. **TAES** — Temporal Access Equity Score
4. **UCR** — Update Completeness Ratio
5. **AAUP** — Age-Adjusted Update Propensity
6. **RPS** — Risk Prediction Score *(NEW)*
7. **EGS** — Equity Gap Score *(NEW)*

---

## 📱 Technical Highlights

- **4.8M+ records** processed across 3 datasets
- **36 states/UTs** analyzed
- **500+ districts** mapped
- **Python + Pandas + GeoPandas**
- **Chart.js interactive dashboard**

---

## 🏆 Jury Questions We're Ready For

| Question | Our Answer |
|----------|-----------|
| "How is this different from EDA?" | We created 7 derived metrics — IFI doesn't exist in raw data |
| "Why should UIDAI care?" | ₹6,000 Cr DBT at risk from staleness |
| "Are recommendations actionable?" | Named districts + specific owners + timelines |

---

## 📁 Quick Links

| Resource | Path |
|----------|------|
| Main Analysis | `notebooks/MASTER_file_FINAL.ipynb` |
| Dashboard | `dashboard/index.html` |
| Visualizations | `visualizations/*.png` |
| Action Framework | `docs/action_framework.md` |
| Jury Defense | `docs/jury_defense.md` |

---

**Team UIDAI_1545** | IET Lucknow | *From descriptive to predictive*
