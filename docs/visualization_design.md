# 📊 Visualization Design Specifications

> **Phase 5 — Decision-Driving Charts for Competition Impact**

---

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Every chart answers a question** | Title = Question, not description |
| **Annotate decisions** | Threshold lines, quadrant labels |
| **Color = meaning** | Red = critical, Green = healthy |
| **Remove chartjunk** | No 3D, no decorative elements |

---

## Required Visualizations (8 Core Charts)

### Chart 1: IFI Choropleth Map
```
Type: India state choropleth
Data: IFI score per state
Color: Diverging (Red-Yellow-Green)
Title: "Where is Aadhaar Data Most Stale?"
Annotation: Label top 5 critical states
Decision: Identifies geographic intervention priorities
```

### Chart 2: State IFI Rankings (Lollipop)
```
Type: Horizontal lollipop chart
Data: IFI per state, sorted ascending
Color: Risk category (Critical/At-Risk/Healthy/Optimal)
Title: "Which States Need Identity Refresh Campaigns?"
Reference line: National average IFI
Decision: Creates priority list for UIDAI outreach
```

### Chart 3: CLCR Child Lifecycle Gap
```
Type: Diverging bar chart
Data: CLCR per state (deviation from 1.0)
Color: Below target = Red, Above = Green
Title: "Are Children Getting Mandatory Biometric Updates?"
Reference line: 1.0 (expected level)
Decision: Identifies states needing school biometric drives
```

### Chart 4: TAES Weekend Access Equity
```
Type: Bar chart with threshold
Data: TAES per state
Color: Below 0.70 = Red, Above = Blue
Title: "Which States Penalize Working Citizens?"
Reference line: 0.70 acceptable threshold
Decision: Weekend staffing recommendations
```

### Chart 5: Lifecycle Gap Scatter (Trivariate)
```
Type: Bubble scatter plot
X-axis: Child share of enrolments
Y-axis: Child bio update rate
Size: Total enrolments
Color: Quadrant (Gap/Working/Monitoring/Normal)
Title: "Where Are Lifecycle Transitions Failing?"
Quadrant labels: Critical annotation
Decision: Flagship differentiation chart
```

### Chart 6: Enrolment vs Update Scatter
```
Type: Scatter with regression
X-axis: Enrolments per 10k population
Y-axis: Update rate (IFI)
Color: Region
Title: "Does High Enrolment Mean Fresh Data?"
Annotation: Label outliers
Decision: Separates high-volume from high-quality states
```

### Chart 7: State × Month Activity Heatmap
```
Type: Heatmap
Rows: States (top 20)
Cols: Days/weeks in March
Color: Activity intensity
Title: "When and Where is Aadhaar Activity Concentrated?"
Decision: Identifies temporal patterns and gaps
```

### Chart 8: Composite Score Dashboard
```
Type: Radar/spider per top 10 states
Dimensions: IFI, CLCR, TAES, UCR, AAUP
Color: State grouping
Title: "Holistic Identity Health by State"
Decision: Multi-dimensional comparison
```

---

## Visualizations to REMOVE ⛔

| Current Chart | Why Remove | Replace With |
|---------------|------------|--------------|
| Basic pie (age distribution) | No decision value | Table in summary |
| Unnormalized state bars | Population confound | IFI rankings |
| Correlation matrix | Invalid for counts | Remove entirely |
| Anomaly scatter (current) | Unclear action | Lifecycle gap |
| Generic trend line | No insight | Weekend/weekday split |

---

## Chart Title Guidelines

| ❌ Bad Title | ✅ Good Title |
|-------------|--------------|
| "State-wise Enrolment Distribution" | "Which States Have Lowest Per-Capita Enrolment?" |
| "Age Group Breakdown" | "Is Child Coverage Matching Census Proportions?" |
| "Monthly Trend" | "When Did Activity Spike and Why?" |
| "Update Comparison" | "Which States Fail to Keep Aadhaar Fresh?" |

---

## Color Palette

```python
RISK_COLORS = {
    'Critical': '#dc3545',      # Red
    'At Risk': '#ffc107',       # Amber
    'Healthy': '#28a745',       # Green
    'Optimal': '#007bff',       # Blue
}

REGION_COLORS = {
    'North': '#4e79a7',
    'South': '#f28e2b',
    'East': '#e15759',
    'West': '#76b7b2',
    'Northeast': '#59a14f',
    'Central': '#edc948',
}
```

---

*Visualization specs complete. Charts designed for decision-making, not description.*
