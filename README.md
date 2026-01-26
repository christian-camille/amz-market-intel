# Amazon Electronics: Market Intelligence & Predictive Modelling (2025/26)

## Project Overview
This project provides a data-driven deep dive into **42,000+ products** within the Amazon Electronics category. Beyond simple visualisations, this analysis identifies the algorithmic "gatekeepers" of sales velocity and develops a robust machine learning pipeline to forecast monthly units sold.

**The core challenge:** Moving beyond descriptive analytics to build a predictive model that survives a "Strict Validation" test by eliminating data leakage.

---

## Executive Summary
* **The "Strict" $R^2$ Score:** **0.796** (Verified after removing trailing indicators).
* **Primary Sales Driver:** **Absolute Price Point** (4.6x more influential than discount depth).
* **The Sponsored Multiplier:** Paid listings outpace organic sales by **6x** in high-rating tiers ($4.5+$ stars).
* **The Buy Box Gatekeeper:** Eligibility correlates with a **100% lift** in median sales volume.

---

## Data Engineering & Cleaning
To ensure a high-fidelity analysis, I implemented several advanced data reconciliation steps:
* **Feature Recovery:** Used Regex to extract "hidden" discount values from raw HTML badge metadata, increasing pricing feature density.
* **New Arrival Segmentation:** Isolated "New Arrivals" (0.0 ratings) to prevent model bias against unrated products.
* **Buy Box Logic:** Imputed `NaN` values in availability to reflect the absence of the "Add to Cart" button, allowing for a binary conversion analysis.

---

## Phase 1: Exploratory Data Analysis (EDA)

### 1. The "Long Tail" of E-commerce
The electronics market is dominated by a few "mega-winners." My analysis utilised **Logarithmic Transformations** to manage this skewness and ensure the model was not hijacked by outliers.

![Sales Distribution Histogram](https://user.fm/files/v2-fc21d1c647cb8185eab085a5bed029ce/skewness.png)

### 2. The Visibility Paradox
Marketing spend acts as a "cheat code" for visibility. However, I identified a **4.0-star "Quality Floor"**; below this threshold, neither sponsorship nor heavy discounting generated significant volume.

![Sponsored vs Organic by Rating Tier](https://user.fm/files/v2-b3ac84bf247d2045cd2286fce62bfedd/average%20sales.png)

### 3. The Buy Box Advantage
Amazon uses the "Add to Cart" button to enforce price competitiveness. Ineligible listings averaged a **31% higher price point**, leading to a massive drop in conversion.

![Buy Box Advantage](https://user.fm/files/v2-7147ea2afc1ec9a9af97cf7608b74c0a/median%20sales.png)

### 4. Statistical Hypothesis Testing

To validate key business assumptions, I performed **Mann-Whitney U tests** (non-parametric) to identify statistically significant drivers of performance:

* **Coupon Efficacy:** Products with coupons showed a **250% increase** in median sales volume compared to those without. The result was highly significant ($p \approx 0$), proving coupons are a primary conversion trigger.
* **Sustainability Pricing:** Contrary to common industry assumptions, "Eco-friendly" tags did not command a price premium ($p = 1.0$), suggesting that price-competitiveness still outweighs sustainability markers in the electronics segment.

---

## Phase 2: Predictive Modelling (Random Forest)

### The Data Leakage Investigation
Initially, the model achieved an $R^2$ of **0.87**. However, a critical investigation revealed that `total_reviews` and `is_best_seller` were acting as **trailing indicators** (leakage). 

To ensure the model could predict success for *new* products, I conducted a feature ablation study. The resulting **"Strict Model"** focused purely on pre-purchase metadata.



### Model Performance
* **Algorithm:** Random Forest Regressor
* **Target:** `Log1p(purchased_last_month)`
* **Strict $R^2$:** **0.796**
* **Mean Absolute Error (MAE):** ~211 units (Highly accurate given the "bucketed" nature of Amazon sales data).

![Feature Importance](https://user.fm/files/v2-753e959a5a03cf53f6f29e59cb1f629c/random%20forest.png)

---

## Model Reliability & Validation
The final parity plot shows high symmetry and a strong diagonal trend, proving that the model accurately captures market dynamics across all price points and categories.

![Parity Plot](https://user.fm/files/v2-8d27d174f6ccfdeba58fd74d4fb82353/strict.png)

---

## Key Business Recommendations
1. **Price Over Percent:** Focus on the **final price point** rather than the discount percentage. Consumers are price-sensitive, not discount-sensitive.
2. **Secure the Buy Box:** Algorithmic visibility (the Buy Box) is worth a 100% increase in median sales. Adjust pricing dynamically to stay below the "suppression threshold."
3. **The 4.0-Star Rule:** Do not scale marketing spend for products with a rating below 4.0. The ROI is significantly higher when applied to products that have already cleared the quality floor.

---

## Technologies Used
* **Python** (Pandas, NumPy)
* **Scikit-Learn** (Random Forest, Model Evaluation)
* **Visualisation:** Seaborn, Matplotlib
* **Data Auditing:** Regular Expressions (re)