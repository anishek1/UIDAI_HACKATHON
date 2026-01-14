# 📊 Data Strategy & Assumptions

> **Phase 2 — Understanding What Our Data Can and Cannot Tell Us**

---

## Dataset Overview

| Dataset | Records | Columns | Granularity | Date Range |
|---------|---------|---------|-------------|------------|
| **Enrolment** | ~1M rows | `date, state, district, pincode, age_0_5, age_5_17, age_18_greater` | PIN code level | March 2025 |
| **Demographic Updates** | ~2M rows | `date, state, district, pincode, demo_age_5_17, demo_age_17_` | PIN code level | March 2025 |
| **Biometric Updates** | ~1.8M rows | `date, state, district, pincode, bio_age_5_17, bio_age_17_` | PIN code level | March 2025 |

---

## ✅ What CAN Be Inferred

| Signal | Inference | Confidence |
|--------|-----------|------------|
| High enrolment + low update ratio | Potentially stale records | ✅ Strong |
| Biometric update spikes in 5-17 age | Mandatory 5-year update compliance | ✅ Strong |
| Weekend vs weekday volume differences | Service accessibility patterns | ✅ Strong |
| State-level update/enrolment ratios | Regional identity "freshness" | ✅ Strong |
| PIN code patterns (first 2 digits) | Urban/rural proxy by postal zone | ⚠️ Medium |
| District-level age group patterns | Population lifecycle stage | ⚠️ Medium |
| Temporal spikes on specific dates | Event-driven activity (schemes, drives) | ⚠️ Medium |

---

## ❌ What CANNOT Be Inferred (Hard Constraints)

| Limitation | Impact on Analysis |
|------------|-------------------|
| **No individual linkage** | Cannot track same person across datasets |
| **No resident demographics** | Cannot stratify by income, caste, occupation |
| **No authentication failure data** | Cannot directly validate "staleness = failure" |
| **No center geolocation** | Cannot model distance-to-service |
| **No rejection/error rates** | Cannot see where enrolments fail |
| **No historical baseline** | March 2025 snapshot only; no YoY comparison |
| **Age bucket coarseness** | 18+ covers ages 18-100+; loses resolution |

---

## ⚠️ Hidden Biases & Reporting Artifacts

### 1. Operator Capacity Artifact
Low numbers in a district may reflect **few operators**, not low demand. A district with 2 operators will always show lower volume than one with 20.

**Mitigation:** Normalize by population, not absolute counts.

### 2. Data Dump Timing Bias
If files are batch-uploaded at end-of-day/week, **intraday patterns may be artificial**.

**Mitigation:** Focus on day-of-week patterns, not hour-of-day.

### 3. State Digitization Variance
Some state UIDAI offices report more granularly than others. A state with 100% digital reporting will appear more active than one with 60%.

**Mitigation:** Acknowledge in limitations; compare within states, not just across.

### 4. Zero Inflation Problem
Districts with 0 activity may be:
- True zeros (no demand)
- Missing data (reporting gap)
- Holiday/closure (center not operating)

**Mitigation:** Flag zero districts separately; don't include in averages.

### 5. Age Bucket Asymmetry
- Enrolment has 3 age groups: 0-5, 5-17, 18+
- Updates have 2 age groups: 5-17, 17+

**Mitigation:** Map 18+ ↔ 17+ for cross-dataset comparison; acknowledge mismatch.

---

## 📐 Derived Metrics Specification

### Metric 1: Identity Freshness Index (IFI)
```
IFI_district = (Sum(demo_updates) + Sum(bio_updates)) / Sum(enrolments)
```
- **Unit:** Ratio (0 to 1+)
- **Interpretation:** Higher = more actively maintained identity data
- **Aggregation:** District → State → National

### Metric 2: Child Lifecycle Capture Rate (CLCR)
```
CLCR_state = bio_age_5_17 / (enrol_age_5_17 × 0.20)
```
- **Assumption:** 20% of 5-17 cohort should update annually (5-year cycle)
- **Interpretation:** <1 = under-updating; >1 = over-serviced

### Metric 3: Temporal Access Equity Score (TAES)
```
TAES_state = (Avg_weekend_daily) / (Avg_weekday_daily)
```
- **Range:** 0 (no weekend service) to 1 (equal access)
- **Interpretation:** Lower = worse access for working citizens

### Metric 4: Update Completeness Ratio (UCR)
```
UCR_state = (Districts with >100 updates) / (Total districts in state)
```
- **Range:** 0 to 1
- **Interpretation:** Service coverage across state geography

### Metric 5: Age-Adjusted Update Propensity (AAUP)
```
AAUP_state = (update_17+ per capita) / (national average per capita)
```
- **Requires:** Census population data
- **Range:** <1 (under-updating) to >1 (over-updating)

---

## 📦 External Data Requirements

| Data Source | Purpose | Status |
|-------------|---------|--------|
| **Census 2011 State Population** | Per-capita normalization | 🟡 Needed |
| **Census 2011 District Population** | District-level IFI accuracy | 🟡 Needed |
| **India State Shapefiles** | Choropleth mapping | 🟡 Needed |
| **UIDAI Regional Office List** | Operator capacity context | 🟢 Optional |
| **PIN code to Urban/Rural mapping** | Urban/rural stratification | 🟢 Optional |

---

## 🔗 Cross-Dataset Join Strategy

```
Enrolment ──┐
            ├──→ JOIN on (date, state, district) → Unified Analysis Table
Demographic ─┤
Biometric ───┘
```

**Join Key:** `(date, state, district)` — not PIN code (too sparse)

**Handling Mismatches:**
- Left join from Enrolment (primary dataset)
- Fill missing update values with 0 (assumption: no activity = no update)

---

## ✅ Validation Checkpoints

| Check | Expected | Action if Failed |
|-------|----------|------------------|
| Sum of age groups = total | Match within 0.1% | Investigate data corruption |
| All states present | 36 states/UTs | Flag missing regions |
| Date range continuous | No gaps > 1 day | Interpolate or flag |
| District names standardized | Consistent spelling | Apply name mapping |

---

*Data constraints documented. Metrics specified. Ready for Phase 3: Analytical Design.*
