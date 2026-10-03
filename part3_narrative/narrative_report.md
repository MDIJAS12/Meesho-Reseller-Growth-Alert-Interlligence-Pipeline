# Narrative Report

## 3.2 — Worked Narratives

### May Ethnic Wear — +77.1% MoM

**Context:**  
This measures Ethnic Wear revenue growth from April to May 2026, comparing April revenue of INR 104520.77 with May revenue of INR 185107.61.

**Insight — Fact:**  
Ethnic Wear revenue increased by **77.1%** from April to May 2026. This result is classified as **flagged** by the Part 2 growth-detection engine.

**Implication — Hypothesis:**  
As a next step, the regional manager should check which regions and reseller aliases contributed to the increase and review inventory and order fulfillment capacity alongside the revenue increase. The reason for the increase is a hypothesis and is not proven by the supplied data.

### Self-Score — May Narrative

- **Specificity:** Pass — The narrative names Ethnic Wear and states the exact April, May, and 77.1% values.
- **Audience fit:** Pass — The wording focuses on what a regional manager should understand and act on.
- **Completeness:** Pass — Context, Insight, and Implication are all present.
- **Actionability:** Pass — The recommendation gives specific checks on regional/reseller contribution and inventory/order fulfillment.

### June Ethnic Wear — -58.74% MoM

**Context:**  
This measures Ethnic Wear revenue growth from May to June 2026, comparing May revenue of INR 185107.61 with June revenue of INR 76371.53.

**Insight — Fact:**  
Ethnic Wear revenue decreased by **58.74%** from May to June 2026. This result is classified as **flagged** by the Part 2 growth-detection engine.

**Implication — Hypothesis:**  
As a next step, the regional manager should check regional and reseller-alias order activity and review whether inventory availability or fulfillment issues could explain the decline. These possible causes are hypotheses and are not proven by the supplied data.

### Self-Score — June Narrative

- **Specificity:** Pass — The narrative names Ethnic Wear and states the exact May, June, and -58.74% values.
- **Audience fit:** Pass — The wording focuses on information and actions relevant to a regional manager.
- **Completeness:** Pass — Context, Insight, and Implication are all present.
- **Actionability:** Pass — The recommendation identifies specific order-activity and inventory/fulfillment checks.

## 3.3 — Chart-Choice Justification

### 1. Which month had the highest total revenue?

**Chart type: Column chart (bar chart).**

A column chart is appropriate because this is a univariate comparison of total revenue across three months. Each month is one category and revenue is the numeric measure. The chart should use a zero-based y-axis so the differences are not visually exaggerated, and the message should be clear within 10 seconds. A legend is unnecessary because there is only one series.

### 2. What percentage share does Ethnic Wear represent of April's total revenue?

**Chart type: Donut chart.**

A donut chart is appropriate because this question asks for the share of one category within a single total, which is a univariate part-to-whole comparison. Ethnic Wear represents INR 104520.77 of April's total revenue of INR 419417.43, giving a 24.92% share. The chart should make the 24.92% share clear within 10 seconds. No legend is necessary if the category and percentage are labeled directly.

### 3. How do the four regions compare on total revenue?

**Chart type: Column chart (bar chart).**

A column chart is appropriate because this is a univariate comparison of total revenue across four regions. Each region is a category and total revenue is the numeric measure. The chart should use a zero-based y-axis so the comparison is not visually exaggerated, and the differences should be understandable within 10 seconds. A legend is unnecessary because there is only one series.

## 3.4 — Masked Top-Reseller Narrative

The Part 1 top-reseller query identified five resellers with total spend above INR 50000. In the West region, **ALIAS-19** recorded INR 75295.09 and **ALIAS-22** recorded INR 73882.33. In the South region, **ALIAS-12** recorded INR 69936.46. In the North region, **ALIAS-06** recorded INR 64238.97 and **ALIAS-05** recorded INR 61825.02.

**Fact:** These are the five highest total-spend resellers returned by the Part 1 query among resellers whose total spend exceeded INR 50000.

**Action:** A regional manager should review the order activity and category mix associated with these coded aliases before making decisions about reseller support or inventory allocation.

The raw reseller names are intentionally excluded from this external-facing narrative.