# AI-Workforce-Transformation-Decision-Support-Framework
Khung hỗ trợ quyết định chuyển đổi lực lượng lao động bằng AI: Ưu tiên đầu tư AI và chiến lược nhân lực cho các tổ chức Việt Nam
Bạn có thể xem báo cáo phân tích chi tiết tại:
👉 [Truy cập Dashboard tại đây](https://ai-workforce-transformation-decision-support-framework-2rwmlzx.streamlit.app/)
------
A data-driven Decision Support System (DSS) that helps organizations prioritize AI investment opportunities and develop workforce transformation strategies by integrating AI capability, workforce readiness, and economic exposure indicators.
---

# Business Problem

Organizations are under increasing pressure to adopt Artificial Intelligence. However, a critical question remains:

> **Which occupations should be prioritized for AI investment while minimizing workforce transition risk?**

Most existing approaches focus only on technological capability, overlooking workforce readiness and business impact.

This project addresses that challenge by providing a quantitative Decision Support Framework for AI investment prioritization and workforce strategy planning.

---

# Research Questions

The framework is designed to answer six key questions:

1. Which occupations can AI effectively perform?
2. How ready are workers to collaborate with AI?
3. Where are the largest workforce transition risks?
4. Which occupations create the greatest economic impact?
5. Which occupations should receive AI investment first?
6. What workforce strategy should organizations adopt?

---

# Framework Overview

```
                AI Capability
                      │
                      ▼
            Worker Readiness
                      │
                      ▼
           Economic Exposure
      (WEI + PEI + Criticality)
                      │
                      ▼
       AI Prioritization Engine
      (AIPS & Workforce Risk)
                      │
                      ▼
 Strategic Workforce Recommendation
```

---

# Core Decision Metrics

The framework introduces several analytical indicators.

| Metric | Description |
|---------|-------------|
| **Cap** | AI Capability Score |
| **Read** | Worker Readiness Score |
| **WEI** | Workforce Exposure Index |
| **PEI** | Payroll Exposure Index |
| **CI** | Criticality Index |
| **Economic Exposure** | Combined economic impact indicator |
| **AIPS** | AI Investment Priority Score |
| **WTRS** | Workforce Transition Risk Score |

---

# Decision Logic

The recommendation engine classifies occupations into four strategic categories.

| Strategy | Description |
|-----------|-------------|
| Deploy AI | High AI capability, high workforce readiness |
| Reskill Workforce | High AI capability but low workforce readiness |
| Human-AI Collaboration | Moderate automation with human oversight |
| Human-led | Human-centered occupations |

---

# Dashboard Modules

### 1. Executive Overview

- Business KPIs
- AI readiness summary
- Workforce transition overview

---

### 2. AI Capability Analysis

Evaluate occupations based on AI capability.

Outputs:

- Capability ranking
- Industry comparison
- Occupation-level analysis

---

### 3. Workforce Readiness Analysis

Measure employee readiness toward AI adoption.

Outputs:

- Readiness distribution
- Human acceptance analysis
- Capability vs Readiness comparison

---

### 4. Workforce Transition Risk Analysis

Identify occupations with the highest workforce transition risk.

Outputs:

- WTRS ranking
- Risk segmentation
- Occupation diagnostics

---

### 5. Economic Prioritization Engine

Evaluate occupations according to:

- Workforce Exposure
- Payroll Exposure
- Criticality
- AI Investment Priority

Outputs:

- Economic Opportunity Map
- Investment Ranking
- Strategy Matrix

---

### 6. Scenario Simulation

Interactive simulation allowing users to adjust:

- Technology Readiness
- Workforce Readiness
- Institutional Readiness

Outputs:

- Updated AI Capability
- Updated Readiness
- Updated AIPS
- Updated WTRS
- Strategy changes

---

### 7. Strategic Action Plan

Generate executive recommendations based on analytical results.

Recommendations include:

- AI Pilot Candidates
- Reskilling Priorities
- Human-AI Collaboration Opportunities
- Human-led Occupations

---

# Technologies

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Scikit-learn

---

# Project Structure

```
AI-Workforce-Transformation/
│
├── data/
│   ├── master_dataset.csv
│   └── processed_dataset.csv
│
├── pages/
│   ├── Executive Dashboard.py
│   ├── AI Capability.py
│   ├── Workforce Readiness.py
│   ├── Workforce Transition Risk.py
│   ├── Economic Prioritization.py
│   ├── Scenario Simulation.py
│   └── Strategic Action Plan.py
│
├── utils/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

---

# Methodology

1. Data Integration
2. Data Cleaning
3. Feature Engineering
4. Min-Max Normalization
5. Composite Index Construction
6. Decision Rule Engine
7. Interactive Visualization
8. Scenario Simulation
9. Strategic Recommendation

---

# Key Features

- Multi-dimensional workforce analysis
- Composite business indicators
- Decision Support System (DSS)
- AI investment prioritization
- Workforce transition assessment
- Interactive scenario simulation
- Executive dashboard
- Strategy recommendation engine

---

# Business Value

Instead of predicting which jobs will disappear, this framework helps organizations answer:

- Where should AI investment begin?
- Which occupations create the greatest business value?
- Which workforce segments require reskilling?
- Where should AI complement humans instead of replacing them?
- How can organizations balance automation opportunities with workforce transition risk?

The dashboard supports evidence-based strategic decision-making rather than rule-of-thumb AI adoption.

---

# Future Improvements

- Machine Learning-based recommendation engine
- Time-series workforce forecasting
- Cost-benefit simulation
- Industry benchmarking
- Generative AI strategy assistant
- Real-time enterprise integration
