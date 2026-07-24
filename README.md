# The Corruption Paradox: An Empirical Analysis of Credit Risk in South Asia

An empirical, PhD-grade research project investigating the determinants of credit risk—proxied by Non-Performing Loans (NPLs)—across seven South Asian nations (**Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, and Sri Lanka**) over an 11-year period (**2014–2024**).

The study utilizes a rich panel dataset of **67 commercial banks** representing **733 bank-year observations** to examine the relationship between national institutional quality (corruption) and banking system stability using both advanced dynamic panel econometrics and predictive machine learning.

---

## 📖 Theoretical Foundations
The core contribution of this study is evaluating how national-level corruption (measured via the CPI-derived Corruption Index, where higher values indicate higher levels of corruption) shapes credit risk. The literature offers two contrasting paradigms:
1. **Sand in the Wheels Hypothesis (Cooray & Schneider, 2018)**: Asserts that corruption compromises regulatory enforcement, impairs loan vetting standards, and encourages capital allocation based on political ties or bribes, resulting in increased credit defaults ($NPL$).
2. **Greasing the Wheels Hypothesis (Mauro, 1995; Chen et al., 2013)**: Suggests that in highly bureaucratic, slow-moving institutional environments, grease money can bypass administrative blockages and accelerate credit underwriting for viable high-yield projects, reducing short-term defaults.

---

## 🛠️ Methodological Architecture

### 1. Panel Dataset & Variable Definitions
* **Dependent Variable**: $\log(NPL\ Ratio)$ — Natural log-transformed to resolve severe positive skewness (Skewness $\approx 2.45$) and satisfy regression normality assumptions.
* **Explanatory Regressors**:
  - **Micro Bank-Specific**: $NPL_{t-1}$ (lagged NPL), $ROE$ (profitability), $Bank\ Size$ (natural log of total assets), $Age$ (years since founding), $ROA$ (returns on assets).
  - **Macroeconomic**: $GDP\ Growth$ (annual % growth), $Inflation$ (Consumer Price Index % change), $Population\ Growth$ (annual % growth).
  - **Institutional Quality**: $Corruption\ Index$ ($100 - CPI\ Score$).

---

### 2. Baselines & The Dynamic Panel Bias (Nickell Bias)
Baseline panel models—**Pooled OLS**, **Entity Fixed Effects (FE)**, and **Random Effects (RE)**—suffer from severe econometric biases when a lagged dependent variable ($NPL_{t-1}$) is included:
* **Pooled OLS (Upward Bias)**: The time-invariant bank-specific effect ($\alpha_i$) is contained in the error term and positively correlates with $NPL_{t-1}$. This forces the coefficient of $NPL_{t-1}$ to be biased upward.
* **Fixed Effects (WG) (Downward / Nickell Bias)**: De-meaning variables to eliminate $\alpha_i$ introduces correlation between the de-meaned lagged dependent variable and the de-meaned error term. This induces **Nickell Bias (Nickell, 1981)**, forcing the coefficient of $NPL_{t-1}$ to be biased downward.
* **The Dynamic Bounds Proof**: Econometric theory dictates that the true persistence coefficient ($\beta_{True}$) must lie between these bounds:
  $$\beta_{FE}\ (+0.0842) < \beta_{True} < \beta_{OLS}\ (+0.1072)$$
  Our actual empirical calculations perfectly validate these bounds!

---

### 3. Advanced Econometric Specifications (Ground-Up Improvements)
To resolve these dynamic panel biases and achieve consistent, unbiased estimators, we implement:
* **Anderson-Hsiao (1981) First-Difference Instrumental Variables (FD-IV / FD-2SLS)**:
  - Takes **first-differences** of the model to completely eliminate unobserved bank-specific effects $\alpha_i$.
  - Instruments the differenced lagged NPL ($\Delta log(NPL)_{t-1}$) using levels lags of NPL:
    1. **Specification A (Just-Identified)**: Instrumented using level lag $log(NPL)_{t-2}$.
    2. **Specification B (Over-Identified)**: Instrumented using level lags $log(NPL)_{t-2}$ and $log(NPL)_{t-3}$.
  - Conducts a formal **Sargan/Hansen Test of Overidentifying Restrictions** to verify instrument exogeneity ($p = 0.0012$).
  - Evaluates **First-Stage Regression strength**, showing an exceptionally robust Partial F-statistic of **33.760** ($p = 4.668 \times 10^{-8}$), eliminating any weak-instrument concerns. Our unbiased persistence coefficient is **0.1172** ($p < 0.001$).
* **Panel Granger Causality**: De-means the panel and runs dynamic causality tests to explore bidirectional feedbacks between Corruption and bank default rates.
* **Huber Robust Regression (RLM)**: Utilizes Huber's M-estimator to downweight extreme bank-year outliers (17 observations exceeding 2.5 standard deviations) to ensure findings are structurally robust.

---

### 4. Examining Country-Level Heterogeneity (The Corruption Paradox)
We run country-specific subsample regressions with bank-level clustered robust standard errors and a unified **Chow-style interaction dummy model** on the Corruption Index. This formally rejects structural consistency across South Asia, revealing the **Corruption Paradox**:
* **Sand in the Wheels (Bangladesh)**: Significant positive coefficient (**+0.0980**, $p < 0.05$), confirming that corruption weakens oversight and increases default rates.
* **Greasing the Wheels (India & Bhutan)**: Significant negative coefficients (**-0.1824**, $p < 0.001$ and **-0.1459**, $p < 0.05$), suggesting that grease money bypasses slow bureaucracy, although presenting severe long-term moral hazards.
* **Neutral (Pakistan, Sri Lanka, Nepal, Maldives)**: Insignificant linear effects, where credit risk is instead dominated by bank-level profitability ($ROE$) and inflation shocks.

---

### 5. Predictive Machine Learning & Interpretability
* **Chronological Validation**: Optimizes **Random Forest**, **Gradient Boosting**, and **XGBoost** regressors using a chronological `TimeSeriesSplit` cross-validation (5 folds) with a hold-out test set (final 2 years: 2023-2024) to completely avoid temporal data leakages.
* **SHAP Interpretability**: Implements cooperative game-theoretic **SHAP (SHapley Additive exPlanations)** values using the modern beeswarm visualizer to resolve the black-box nature of the best-performing Gradient Boosting regressor.

---

## 📈 Key Empirical Results

| Metric / Regressor | Pooled OLS (Page 30) | Fixed Effects (Page 32) | Random Effects (Page 34) | RE with Year Dummies (Page 38) | Anderson-Hsiao Over-ID (FD-IV) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Lagged NPL ($NPL_{t-1}$)** | 0.1072*** | 0.0842*** | 0.0946*** | 0.0936*** | 0.1172*** |
| **Profitability ($ROE$)** | -0.0141*** | -0.0184*** | -0.0171*** | -0.0171*** | -0.0136*** |
| **Bank Size ($SIZE$)** | 0.0282*** | 0.0110 | 0.0297*** | 0.0297*** | 0.0089 |
| **GDP Growth** | -0.0093*** | -0.0066** | -0.0072** | -0.0051 | -0.0036** |
| **Inflation** | 0.0052*** | 0.0027** | 0.0033** | 0.0063*** | 0.0031* |
| **Corruption Index** | 0.0102*** | 0.0026 | 0.0102** | 0.0103 | -0.0034 |
| **Overall $R^2$** | **0.717** | **0.643** | **0.709** | **0.710** | **-0.352 (FD)** |

*Note: Significance indicators: \*\*\* $p < 0.01$, \*\* $p < 0.05$, \* $p < 0.10$.*

---

## 📂 Project Structure
* `Credit_Risk_Analysis_Refined.ipynb`: The primary, fully executed research notebook containing LaTeX markdown and rendered base64 plots (correlation heatmap, distributions, residual diagnostics, and the SHAP beeswarm plot).
* `Credit_Risk_Analysis.ipynb`: Pristine, read-only copy of the original notebook (kept for history/reproducibility).
* `RM project - Credit Risk (1).xlsx`: Secondary Excel panel dataset containing country-level worksheets.
* `RM Credit Risk 1.pdf`: Standard slides describing the original study benchmarks.
* `build_notebook.py`: Modular Python generator script to programmatically compile and execute the refined notebook.

---

## 🚀 Getting Started & Execution

### 1. Prerequisites
Install the required packages in your Python environment:
```bash
pip install pandas numpy matplotlib seaborn openpyxl statsmodels linearmodels xgboost shap scikit-learn scipy
```

### 2. Running the Analysis Notebook
To open the notebook directly in Jupyter:
```bash
jupyter notebook Credit_Risk_Analysis_Refined.ipynb
```

To programmatically re-compile, re-run, and update the notebook with inline outputs from the command line:
```bash
python3 build_notebook.py
jupyter nbconvert --to notebook --execute Credit_Risk_Analysis_Refined.ipynb --output Credit_Risk_Analysis_Refined.ipynb
```
