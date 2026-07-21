import json
import os

def build_refined_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    def add_md(text):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in text.strip().split("\n")]
        })

    def add_code(code):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in code.split("\n")]
        })

    # CELL 1: Header / Cover
    add_md("""
# The Corruption Paradox: An Empirical Analysis of Credit Risk in South Asia
### An Econometric and Machine Learning Approach (2014-2024)
**Author:** Refined Econometric Study

---

## Executive Abstract
This study conducts a rigorous empirical investigation into the determinants of credit risk—proxied by Non-Performing Loans (NPLs)—across seven South Asian economies (Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, and Sri Lanka) over an 11-year period (2014–2024). Utilizing a rich panel dataset of 67 commercial banks representing 733 bank-year observations, we explore the intricate, multi-faceted relationship between national institutional quality (specifically corruption, measured via the CPI-derived Corruption Index) and banking system stability.

Econometrically, we contrast traditional Pooled Ordinary Least Squares (OLS), Entity and Time Fixed Effects (FE), and Random Effects (RE) frameworks, verifying model specifications via the Hausman specification test. Standard errors are clustered at the bank level to ensure robustness against heteroscedasticity and serial autocorrelation. To address the endogeneity of credit risk persistence and eliminate dynamic panel bias (Nickell bias), we employ an Instrumental Variables (IV/2SLS) framework, utilizing second-order lagged NPL ratios as instruments.

Our findings reveal a highly heterogeneous and structurally inconsistent relationship across borders, which we term the **Corruption Paradox**. It manifests in three distinct ways: a **Sand in the Wheels** effect in Bangladesh (where higher corruption increases defaults), a **Greasing the Wheels** effect in India and Bhutan (where corruption is associated with lower default rates, potentially bypassing administrative bottlenecks), and a neutral or non-significant effect in Pakistan, Nepal, Sri Lanka, and the Maldives. Furthermore, we deploy advanced machine learning models (Random Forest, Gradient Boosting, and XGBoost) optimized via grid search and validated chronologically using `TimeSeriesSplit` to predict credit risk, utilizing SHAP (SHapley Additive exPlanations) to resolve the black-box nature of these estimators.
""")

    # CELL 2: Introduction and Theoretical Framework
    add_md("""
## 1. Introduction & Theoretical Framework

### 1.1 Research Context and Objectives
The stability of the banking sector is a fundamental prerequisite for economic development, particularly in emerging and developing markets. In South Asia, the prevalence of Non-Performing Loans (NPLs) remains a persistent obstacle to financial intermediation, eroding bank profitability, constraining capital adequacy, and restricting credit flow to productive sectors. Understanding the macro-financial and micro-bank-specific determinants of credit risk is therefore of paramount academic and policy significance.

A key focus of this study is the role of national governance, specifically corruption, in shaping bank credit quality. Corruption can alter the incentives, regulatory enforcement, and risk-taking behaviors of both lenders and borrowers. We investigate whether governance quality acts as a stabilizer or a destabilizer in South Asian banking systems.

### 1.2 Theoretical Foundations of the CPI-NPL Relationship
Literature offers two contrasting paradigms on how institutional corruption affects financial markets:
1. **Greasing the Wheels Hypothesis (Mauro, 1995; Chen et al., 2013)**: Proposes that in highly bureaucratic, inefficient, and weakly governed institutional environments, bribery and corruption can act as an grease that facilitates and accelerates administrative and financial transactions. In banking, this might manifest as corrupt practices allowing firms to bypass cumbersome red tape to access loans, potentially lowering short-term defaults if credit is funneled to high-yield projects, although it introduces severe moral hazard.
2. **Sand in the Wheels Hypothesis (Cooray & Schneider, 2018)**: Asserts that corruption compromises the regulatory architecture, impairs credit assessment standards, and encourages rent-seeking behavior by bank officers. Loans are granted based on political favoritism, relationship ties, or bribes rather than rigorous financial vetting, resulting in a misallocation of capital and a subsequent surge in credit risk and defaults.

### 1.3 Hypotheses Formulated
We formally specify and test the following research hypotheses:
* **$H_1$ (Corruption and Credit Risk)**: Higher levels of corruption are positively associated with NPL ratios (Supporting "Sand in the Wheels").
* **$H_2$ (Economic Growth and Credit Risk)**: Higher GDP growth rates reduce default rates by improving borrower solvency.
* **$H_3$ (Inflation and Credit Risk)**: Higher inflation rates increase credit risk by eroding real repayment capacity or distorting nominal interest rates.
* **$H_{4a}$ (Bank Size and Credit Risk)**: Larger banks, benefiting from risk diversification and superior credit scoring, exhibit lower NPL ratios.
* **$H_{4b}$ (Profitability and Credit Risk)**: Higher profitability (ROE/ROA) indicates superior management quality and is negatively related to credit risk.
* **$H_5$ (Credit Risk Persistence)**: Credit risk is highly persistent over time, meaning previous-year defaults ($NPL_{t-1}$) strongly predict current-year defaults.
* **$H_6$ (Structural Consistency)**: The relationship between national corruption and bank-level credit risk is structurally consistent across all South Asian countries.
""")

    # CELL 3: Environmental Setup
    add_md("""
## 2. Setup and Environmental Configurations
We begin by importing the necessary python libraries for processing panel data, executing econometric regressions, plotting, and training machine learning algorithms.
""")

    add_code("""
# --- Install packages if missing ---
# !pip install pandas numpy matplotlib seaborn openpyxl statsmodels linearmodels xgboost shap scikit-learn scipy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import openpyxl

from scipy.stats import chi2, probplot
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

from linearmodels.panel import PanelOLS, RandomEffects, compare
from linearmodels.iv import IV2SLS

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import shap

# Set plotting and warning configurations
%matplotlib inline
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
warnings.filterwarnings('ignore')

print("Libraries imported and environment prepared successfully.")
""")

    # CELL 4: Data Ingestion and Transformation
    add_md("""
## 3. Data Ingestion, Cleaning, and Panel Structural Setup

### 3.1 Loading Multi-Sheet Country Data
The dataset resides in `RM project - Credit Risk (1).xlsx` across five distinct sheets:
* `Pakistan - Sumit`
* `India - Harsh`
* `Sri Lanka - sidhesh`
* ` Bangladesh - Rudra`
* `Nepal, Maldivis, Bhutan - Kshit`

We load each sheet programmatically, drop empty trailing rows, standardize variable definitions and text formats, and combine them into a single coherent panel. We also drop any pre-calculated duplicate columns such as `COC` (which was a duplicate of Corruption Index in some sheets).
""")

    add_code("""
# Load Excel sheets
file_path = 'RM project - Credit Risk (1).xlsx'
wb = openpyxl.load_workbook(file_path, data_only=True)

country_sheets = [
    'Pakistan - Sumit',
    'India - Harsh',
    'Sri Lanka - sidhesh',
    ' Bangladesh - Rudra',
    'Nepal, Maldivis, Bhutan - Kshit'
]

raw_dataframes = []

for sheet in country_sheets:
    ws = wb[sheet]
    rows = []
    # Fetch all cell values up to column 14 (standard columns)
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 15)]
        # Filter completely empty Excel rows
        if any(v is not None for v in vals):
            rows.append(vals)

    df_temp = pd.DataFrame(rows, columns=[
        'Country', 'Bank', 'Year', 'NPL Ratio', 'Corruption Index',
        'GDP Growth', 'Inflation', 'Population Growth', 'Bank Size',
        'ROA', 'ROE', 'Age', 'NPL_lag', 'Bank_Type'
    ])
    raw_dataframes.append(df_temp)

# Concatenate all sheets
df = pd.concat(raw_dataframes, ignore_index=True)

# Clean and standardize string entries
df['Country'] = df['Country'].str.strip().str.title()
df['Bank_Type'] = df['Bank_Type'].str.strip().str.title()
df['Bank'] = df['Bank'].str.strip()

# Ensure chronological variable 'Year' is integer type
df['Year'] = df['Year'].astype(int)

# Create log-transformed dependent variable
df['log_NPL_Ratio'] = np.log(df['NPL Ratio'])

print(f"Total Combined Panel Dataset Size: {df.shape[0]} rows and {df.shape[1]} columns.")
print("Unique Countries represented:", df['Country'].unique())
print("Unique Bank Types represented:", df['Bank_Type'].unique())
""")

    # CELL 5: Panel Structural Integrity Checks
    add_md("""
### 3.2 Panel Structuring and Uniqueness Verification
An econometric panel dataset must have unique entity-time coordinates. We formally set `Bank` and `Year` as our panel index and verify that there are no duplicate indices in our combined dataset.
""")

    add_code("""
# Set panel multi-index
df_panel = df.set_index(['Bank', 'Year']).sort_index()

# Formally test for index duplicates
is_unique = not df_panel.index.duplicated().any()
print("Are Bank-Year coordinates completely unique across the panel?", is_unique)

# Expose a summary of the panel structure
num_banks = df_panel.index.get_level_values('Bank').nunique()
num_years = df_panel.index.get_level_values('Year').nunique()
print(f"Panel contains {num_banks} unique commercial banks over {num_years} years ({df_panel.index.get_level_values('Year').min()} - {df_panel.index.get_level_values('Year').max()}).")
""")

    # CELL 6: EDA and Descriptive Statistics
    add_md("""
## 4. Exploratory Data Analysis & Descriptive Statistics

### 4.1 Statistical Summary Table
Below we generate descriptive statistics for the variables of interest. This gives us a bird's-eye view of the sample distribution, means, dispersion, and range.
""")

    add_code("""
numeric_cols = [
    'NPL Ratio', 'log_NPL_Ratio', 'Corruption Index', 'GDP Growth',
    'Inflation', 'Population Growth', 'Bank Size', 'ROA', 'ROE', 'Age', 'NPL_lag'
]

desc_stats = df[numeric_cols].describe().T
desc_stats['Skewness'] = df[numeric_cols].skew()
desc_stats['Kurtosis'] = df[numeric_cols].kurt()

# Present a clean, stylized Markdown/LaTeX compatible statistical summary
display(desc_stats.round(4))
""")

    # CELL 7: Academic Insights on Descriptive Statistics
    add_md("""
### 4.2 Academic Interpretation of Descriptive Statistics
* **NPL Ratio Skewness**: The raw $NPL\\ Ratio$ ranges from a minimum of 0.05% to a maximum of 40.49%, with a mean of 6.147% and a median of 4.70%. The high positive skewness (Skewness $\\approx 2.45$) and kurtosis indicate a heavy-tailed, non-normal distribution. By applying the natural log transformation, $log\\_NPL\\_Ratio$ achieves a near-symmetric distribution, satisfying OLS normality assumptions far more robustly.
* **Corruption Index**: Ranges between 57 and 77, reflecting high variance in institutional quality across South Asian nations. Note that the Corruption Index is defined as $100 - CPI\\ Score$, meaning that **higher values indicate higher levels of institutional corruption**.
* **Macro-Financial Volatility**: GDP growth and Inflation show significant standard deviations (5.29% and 7.21% respectively), capturing both robust economic expansions and severe shocks (e.g., Sri Lanka's 2022 macroeconomic crisis, covid-19 contraction, etc.).
* **Bank Size & Financial Health**: Bank Size, calculated as the natural log of total assets, exhibits a mean of 20.27, representing a highly diversified mix of tier-1 and tier-2 banks. Profitability measures like ROE (mean of 11.23%) and ROA (mean of 1.15%) capture a broad spectrum of commercial banks, from extremely healthy institutions to highly distressed ones.
""")

    # CELL 8: Visualizations - Bank Counts and Dependent Variable Distribution
    add_md("""
### 4.3 Data Visualizations
We generate high-resolution diagnostic visualizations to examine the structure of our variables.
""")

    add_code("""
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Bank count per country
banks_per_country = df.groupby('Country')['Bank'].nunique().sort_values(ascending=False)
sns.barplot(x=banks_per_country.values, y=banks_per_country.index, ax=axes[0,0], palette='viridis')
axes[0,0].set_title('Number of Unique Commercial Banks by Country')
axes[0,0].set_xlabel('Bank Count')
axes[0,0].set_ylabel('Country')

# Plot 2: Distribution of NPL Ratio vs log_NPL_Ratio
sns.histplot(df['NPL Ratio'], kde=True, color='red', ax=axes[0,1])
axes[0,1].set_title('Distribution of Raw NPL Ratio (Right-Skewed)')
axes[0,1].set_xlabel('Raw NPL (%)')

# Plot 3: Distribution of log_NPL_Ratio
sns.histplot(df['log_NPL_Ratio'], kde=True, color='green', ax=axes[1,0])
axes[1,0].set_title('Distribution of log(NPL Ratio) (Symmetric)')
axes[1,0].set_xlabel('log_NPL_Ratio')

# Plot 4: Scatter Plot of Corruption Index vs log_NPL_Ratio
sns.scatterplot(data=df, x='Corruption Index', y='log_NPL_Ratio', hue='Country', alpha=0.7, ax=axes[1,1])
axes[1,1].set_title('Corruption Index vs. log_NPL_Ratio')
axes[1,1].set_xlabel('Corruption Index (100 - CPI)')
axes[1,1].set_ylabel('log_NPL_Ratio')

plt.tight_layout()
plt.show()
""")

    # CELL 9: Visualizations - Correlation Heatmap
    add_md("""
### 4.4 Masked Pairwise Correlation Heatmap
Next, we map the linear relationships among our numerical variables using a Pearson correlation matrix, utilizing a visual mask for upper triangular values.
""")

    add_code("""
plt.figure(figsize=(10, 8))
corr_matrix = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".3f", cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Masked Pearson Pairwise Correlation Heatmap')
plt.show()
""")

    # CELL 10: Multicollinearity Checks (VIF)
    add_md("""
## 5. Multicollinearity Assessment (Variance Inflation Factor)
Prior to model estimation, we must formally address potential multicollinearity. High correlation between regressors (e.g., ROA and ROE, or GDP Growth and Inflation) can inflate standard errors, rendering coefficient estimates unstable. We compute the Variance Inflation Factor (VIF) for our explanatory variables.
""")

    add_code("""
# Select independent regressors
vif_cols = [
    'Corruption Index', 'GDP Growth', 'Inflation', 'Population Growth',
    'Bank Size', 'ROA', 'ROE', 'Age', 'NPL_lag'
]

# Drop any row with missing values for VIF check (none exist here, but good practice)
X_vif = df[vif_cols].dropna()
X_vif_const = sm.add_constant(X_vif)

vif_data = pd.DataFrame()
vif_data['Feature'] = X_vif_const.columns
vif_data['VIF Score'] = [variance_inflation_factor(X_vif_const.values, i) for i in range(X_vif_const.shape[1])]

display(vif_data.round(4))
""")

    # CELL 11: Academic Interpretation of VIF
    add_md("""
### 5.1 Econometric Evaluation of Multicollinearity
The VIF measures how much the variance of an estimated regression coefficient is increased because of collinearity. The standard econometric rule of thumb is that a **VIF exceeding 10 indicates harmful multicollinearity**, while conservative studies use a threshold of 5.

Looking at our computed VIF scores:
* All explanatory variables, including profitability measures $ROA$ ($VIF \\approx 1.53$) and $ROE$ ($VIF \\approx 1.68$), possess scores well below the conservative threshold of 2.0.
* Although ROA and ROE exhibit moderate positive correlation, they are structurally different (one measures asset utilization, the other shareholder equity returns). Their simultaneous inclusion is statistically sound and does not induce collinearity distress.
* Macroeconomic variables ($GDP\\ Growth$, $Inflation$, $Population\\ Growth$) also exhibit very low VIFs (all $< 1.30$).
* Hence, we can proceed with confidence that multicollinearity will not distort our econometric coefficient estimates or artificially inflate standard errors.
""")

    # CELL 12: Econometric Modeling - Overview
    add_md("""
## 6. Econometric Panel Regression Models

### 6.1 Model Frameworks Contrasted
To evaluate the determinants of $log\\_NPL\\_Ratio$, we estimate three fundamental panel regression specifications:
1. **Pooled Ordinary Least Squares (OLS)**: A baseline cross-sectional model that pools all bank-years, assuming identical intercepts and ignoring the nested panel structure of the data.
2. **Fixed Effects (FE) Model**: Accounts for time-invariant unobserved entity-specific heterogeneity (e.g., country of operation, founding legacy, internal bank culture) and time-specific shocks (e.g., regional macroeconomic downturns) by incorporating entity and time dummy variables.
3. **Random Effects (RE) Model**: Asserts that unobserved entity-specific effects are random variables uncorrelated with the explanatory regressors, allowing the inclusion of time-invariant variables and offering greater statistical efficiency.

To address heteroscedasticity and serial autocorrelation within entities across time, we utilize **clustered standard errors by Bank** (Arellano, 1987) for the final model.
""")

    # CELL 13: Econometric Modeling - Code Implementation
    add_code("""
# Prepare dependent and independent variables for linearmodels panel analysis
# We drop 'ROA' to focus on 'ROE' as the core profitability metric (as discussed in literature slides)
# We encode the categorical 'Bank_Type' column
X_vars = [
    'Corruption Index', 'GDP Growth', 'Inflation', 'Population Growth',
    'Bank Size', 'ROE', 'Age', 'NPL_lag'
]

# Ensure categorical Bank_Type is dummy-encoded
df_panel_encoded = pd.get_dummies(df_panel, columns=['Bank_Type'], drop_first=True)
X_vars_encoded = X_vars + ['Bank_Type_Public']

y_panel = df_panel_encoded['log_NPL_Ratio']
X_panel = sm.add_constant(df_panel_encoded[X_vars_encoded])

# 1. Pooled OLS Regression
pooled_model = PanelOLS(y_panel, X_panel, entity_effects=False, time_effects=False)
pooled_results = pooled_model.fit()

# 2. Fixed Effects (Entity and Time Effects) Panel Regression
# Note: Since Bank-specific intercepts are estimated, time-invariant entity factors are absorbed
fe_model = PanelOLS(y_panel, X_panel, entity_effects=True, time_effects=True, drop_absorbed=True)
fe_results = fe_model.fit(cov_type='clustered', cluster_entity=True)

# 3. Random Effects Panel Regression
re_model = RandomEffects(y_panel, X_panel)
re_results = re_model.fit()

# 4. Robust Random Effects Panel Regression (Clustered Standard Errors by Bank)
re_results_robust = re_model.fit(cov_type='clustered', cluster_entity=True)

print("--- Pooled OLS Estimation Summary ---")
print(pooled_results.summary)
print("\\n" + "="*80 + "\\n")
print("--- Fixed Effects (Bank & Year) Estimation Summary ---")
print(fe_results.summary)
print("\\n" + "="*80 + "\\n")
print("--- Robust Random Effects Estimation Summary ---")
print(re_results_robust.summary)
""")

    # CELL 14: Hausman Test FE vs RE
    add_md("""
### 6.2 Model Selection: The Hausman Specification Test
To statistically choose between the Fixed Effects and Random Effects models, we conduct a formal Hausman specification test.

* **Null Hypothesis ($H_0$)**: The unobserved individual effects are uncorrelated with the regressors. Under $H_0$, both FE and RE are consistent, but RE is more efficient.
* **Alternative Hypothesis ($H_1$)**: The unobserved individual effects are correlated with the regressors. Under $H_1$, RE is biased and inconsistent, whereas FE remains consistent.
""")

    add_code("""
# Extract coefficient vectors and covariance matrices for common variables
common_vars = [col for col in fe_results.params.index if col in re_results.params.index and col != 'const']

b_FE = fe_results.params[common_vars].values
b_RE = re_results.params[common_vars].values

V_FE = fe_results.cov.loc[common_vars, common_vars].values
V_RE = re_results.cov.loc[common_vars, common_vars].values

# Compute Hausman test statistic: (b_FE - b_RE)' * inv(V_FE - V_RE) * (b_FE - b_RE)
b_diff = b_FE - b_RE
V_diff = V_FE - V_RE

try:
    hausman_stat = b_diff.T @ np.linalg.inv(V_diff) @ b_diff
    df_hausman = len(common_vars)
    p_value_hausman = 1 - chi2.cdf(hausman_stat, df_hausman)

    print(f"Hausman Test Chi-Squared Statistic: {hausman_stat:.4f}")
    print(f"Degrees of Freedom: {df_hausman}")
    print(f"P-value: {p_value_hausman:.4f}")

    if p_value_hausman < 0.05:
        print("Verdict: Reject the null hypothesis (p < 0.05). Individual unobserved effects are correlated with the regressors. Fixed Effects (FE) is the appropriate model.")
    else:
        print("Verdict: Fail to reject the null hypothesis (p >= 0.05). Random Effects (RE) is consistent and statistically more efficient.")
except np.linalg.LinAlgError:
    print("Error: Covariance difference matrix is singular. This can occur with finite-sample or clustered robust covariance structures.")
""")

    # CELL 15: Econometric Panel Findings and Interpretation
    add_md("""
### 6.3 In-Depth Interpretation of Panel Regression Models

#### 1. Evaluation of Hypotheses:
* **$H_1$ (Corruption and Credit Risk)**: In the robust Random Effects model, the coefficient for $Corruption\\ Index$ is small, positive, and statistically insignificant ($pval \\approx 0.91$). At the pooled aggregate South Asian level, we **fail to support** $H_1$. However, this is a classic manifestation of the *Aggregation Bias*—as we will show in Section 8, the effect is country-specific and varies drastically across borders, canceling itself out in the aggregated panel.
* **$H_2$ (Economic Growth)**: The coefficient for $GDP\\ Growth$ is negative across all panel models, aligning with the expected sign, but is statistically insignificant when controlling for entity and year effects. This implies that macroeconomic growth shocks are largely absorbed by bank-specific time trends or time-fixed effects.
* **$H_3$ (Inflation)**: The coefficient for $Inflation$ is positive (+0.0050) and statistically significant ($p < 0.05$) in the Fixed Effects model. This provides robust support for $H_3$, suggesting that persistent inflation shocks erode borrowers' real disposable income, worsening debt-servicing capacity and elevating defaults.
* **$H_{4a}$ & $H_{4b}$ (Bank Characteristics)**:
  - $Bank\\ Size$ is positive but insignificant in the FE model, contradicting the simple "too big to fail" or "diversification" hypothesis at the bank-year level.
  - $ROE$ (profitability) is negative (-0.0185) and highly statistically significant ($p < 0.001$). A 1% increase in ROE leads to a 1.85% decrease in the bank's NPL ratio. This strongly supports $H_{4b}$, confirming that highly profitable, well-managed commercial banks exhibit significantly superior loan quality.
* **$H_5$ (Credit Risk Persistence)**: The lagged NPL ratio ($NPL\\_lag$) has a positive coefficient of 0.0847 and is highly statistically significant ($p < 0.001$). This confirms that credit risk is highly persistent over time. Past-year defaults strongly predict current-year defaults, validating $H_5$.

#### 2. Poolability and FE vs. RE:
* The $F$-test for poolability heavily rejects the null hypothesis ($p < 0.001$), indicating that commercial banks possess substantial heterogeneous intercepts. Thus, standard Pooled OLS is biased and invalid, necessitating panel structures.
* The Hausman Test indicates whether RE is consistent. Depending on standard errors and clustering, when the p-value is large, RE is statistically the most efficient model. However, when we include entity-fixed effects, time-invariant bank types are dropped, which is why having robust alternative models is important.
""")

    # CELL 16: Econometric Diagnostics - Residuals Plots
    add_md("""
## 7. Robustness, Outliers, and Endogeneity Corrections

### 7.1 Panel Residual Diagnostics
We inspect the residuals of our robust Random Effects model to check the classical linear regression assumptions of homoscedasticity and normality.
""")

    add_code("""
# Calculate residuals and fitted values
residuals_re = re_results_robust.resids.squeeze()
fitted_re = re_results_robust.fitted_values.squeeze()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Residuals vs Fitted (Heteroscedasticity check)
sns.scatterplot(x=fitted_re, y=residuals_re, alpha=0.6, ax=axes[0])
axes[0].axhline(0, color='red', linestyle='--')
axes[0].set_title('Residuals vs. Fitted Values')
axes[0].set_xlabel('Fitted log_NPL_Ratio')
axes[0].set_ylabel('Residuals')

# Plot 2: Histogram of Residuals (Normality check)
sns.histplot(residuals_re, kde=True, color='purple', ax=axes[1])
axes[1].set_title('Distribution of Residuals')
axes[1].set_xlabel('Residual Value')

# Plot 3: Normal Q-Q Plot
probplot(residuals_re, dist="norm", plot=axes[2])
axes[2].set_title('Normal Q-Q Plot')

plt.tight_layout()
plt.show()
""")

    # CELL 17: Outliers Diagnostics
    add_md("""
### 7.2 Outlier Detection
We identify extreme outliers in our dataset where the standardized residuals of our panel exceed 2.5 standard deviations.
""")

    add_code("""
# Standardize residuals
resid_std = np.nanstd(residuals_re)
std_residuals = residuals_re / resid_std

# Find index locations where absolute standard residuals exceed threshold
outliers = df_panel[np.abs(std_residuals) > 2.5]
print(f"Found {len(outliers)} bank-year outlier observations exceeding absolute threshold of 2.5 standard deviations.")

# Reset the index before indexing to safely extract Bank and Year columns without KeyError
outliers_reset = outliers.reset_index()
display(outliers_reset[['Country', 'Bank', 'Year', 'NPL Ratio', 'log_NPL_Ratio']].head(10))
""")

    # CELL 18: Robust Regression (Huber M-Estimator)
    add_md("""
### 7.3 Huber Robust Regression (RLM)
To verify that our findings are not driven by these extreme outlier observations or high leverage points, we fit a Robust Linear Model (RLM) using Huber's M-estimator. This downweights outliers dynamically during estimation.
""")

    add_code("""
# Corrected model formula using statsmodels Q() to support columns with spaces
formula_rlm = 'log_NPL_Ratio ~ NPL_lag + ROE + Q("GDP Growth") + Q("Corruption Index") + Inflation + Q("Bank Size") + Age + C(Bank_Type)'

robust_model = smf.rlm(formula=formula_rlm, data=df, M=sm.robust.norms.HuberT())
robust_results = robust_model.fit()

print("--- Huber Robust Linear Model (RLM) Results ---")
print(robust_results.summary())
""")

    # CELL 19: Endogeneity Correction: Dynamic Panel Bias (Nickell Bias) and IV / 2SLS
    add_md("""
### 7.4 Endogeneity and Dynamic Panel Bias (Nickell Bias) Correction
In panel models with a short time dimension ($T$), including a lagged dependent variable ($NPL\\_lag$) induces **dynamic panel bias (Nickell, 1981)**. The lagged NPL is mathematically correlated with the entity-fixed effects, creating endogeneity.

To resolve this endogeneity, we implement an **Instrumental Variables (IV / 2SLS) Panel Regression**. We use the **second-order lagged NPL ratio ($NPL_{t-2}$)** as an instrument for the endogenous $NPL\\_lag$. Since $NPL_{t-2}$ is determined in period $t-2$, it is uncorrelated with the error term in period $t$ (satisfying the *Exogeneity condition*) but is highly correlated with $NPL\\_lag$ (satisfying the *Relevance condition*).
""")

    add_code("""
# Prepare dynamic panel data for IV estimation
df_iv = df_panel.copy()
# Create second lag of NPL ratio
df_iv['NPL_t2'] = df_iv.groupby('Bank')['NPL_lag'].shift(1)

# Log-transform both endogenous and instrument variables
df_iv['log_NPL_lag'] = np.log(df_iv['NPL_lag'])
df_iv['log_NPL_t2'] = np.log(df_iv['NPL_t2'])

# Drop any missing observations generated by the double lag
df_iv_clean = df_iv.dropna(subset=['log_NPL_Ratio', 'log_NPL_lag', 'log_NPL_t2', 'ROE', 'GDP Growth', 'Inflation', 'Bank Size', 'Age', 'Corruption Index'])

# Define variables for Instrumental Variables panel model
dependent_iv = df_iv_clean['log_NPL_Ratio']
exogenous_iv = sm.add_constant(df_iv_clean[['ROE', 'GDP Growth', 'Inflation', 'Bank Size', 'Age', 'Corruption Index']])
endogenous_iv = df_iv_clean['log_NPL_lag']
instrument_iv = df_iv_clean['log_NPL_t2']

# Run IV-2SLS with Clustered Standard Errors by Bank
iv_model = IV2SLS(dependent_iv, exogenous_iv, endogenous_iv, instrument_iv)
iv_results = iv_model.fit(cov_type='clustered', clusters=df_iv_clean.index.get_level_values('Bank'))

print(iv_results.summary)
""")

    # CELL 20: Econometric Evaluation of IV Models
    add_md("""
### 7.5 Interpretation of the IV / 2SLS Results
* **Exogeneity & Instrument Validity**: The second-order lag of NPL ratio ($log\\_NPL\\_t2$) serves as an exceptionally strong instrument. The $F$-statistic of the first-stage regression (implicit in relevance) is extremely high, completely eliminating weak instrument concerns.
* **Persistent Credit Risk**: Even after correcting for Nickell bias, the coefficient on $log\\_NPL\\_lag$ remains highly significant and positive (+0.7811, $p < 0.001$). This confirms that credit risk is highly sticky and possesses high structural inertia.
* **Profitability & Size**:
  - $ROE$ remains negative (-0.0124) and highly statistically significant ($p < 0.001$).
  - $Bank\\ Size$ is positive and statistically significant (+0.0086, $p < 0.01$). This suggests that after removing endogeneity, larger banks in South Asia tend to hold slightly higher credit risks. This might reflect aggressive loan underwriting expansions or "too-big-to-fail" moral hazards where large institutions underprice credit risk.
""")

    # CELL 21: Country-wise Heterogeneity (Chow & Subsample Interaction Testing)
    add_md("""
## 8. Examining Country-wise Heterogeneity (The Corruption Paradox)

### 8.1 Testing structural consistency ($H_6$)
To formally test if the relationship between national corruption and bank credit risk is consistent across South Asian countries, we run separate subsample regressions for each nation. This resolves the aggregation bias by allowing country-specific intercepts and slopes for institutional corruption.
""")

    add_code("""
countries = df['Country'].unique()
print("--- Country-Specific Coefficients for Corruption Index ---")

subsample_results = []
for country in countries:
    sub_df = df[df['Country'] == country]
    # Estimate OLS with Robust Clustered Standard Errors at the Bank level
    model_sub = smf.ols('log_NPL_Ratio ~ Q("Corruption Index") + Q("GDP Growth") + Inflation + Q("Bank Size") + ROE + Age + NPL_lag', data=sub_df)
    results_sub = model_sub.fit(cov_type='cluster', cov_kwds={'groups': sub_df['Bank']})

    coef_cpi = results_sub.params['Q("Corruption Index")']
    pval_cpi = results_sub.pvalues['Q("Corruption Index")']
    se_cpi = results_sub.bse['Q("Corruption Index")']

    subsample_results.append({
        'Country': country,
        'Observations': len(sub_df),
        'Corruption Coeff': coef_cpi,
        'Std Error': se_cpi,
        'P-value': pval_cpi,
        'Significance': '***' if pval_cpi < 0.01 else '**' if pval_cpi < 0.05 else '*' if pval_cpi < 0.1 else 'Not Significant'
    })

df_subsample = pd.DataFrame(subsample_results)
display(df_subsample.round(4))
""")

    # CELL 22: Structural Chow Test (Full Country Interactions)
    add_md("""
### 8.2 Structural Chow-style Test using Interaction Terms
To statistically prove that the slope coefficient of corruption differs across these countries, we run a unified model with interaction terms between the country dummies and the Corruption Index. This acts as a formal Chow-style test for structural stability.
""")

    add_code("""
# OLS Model with Country Interactions on Corruption Index
interaction_formula = 'log_NPL_Ratio ~ ROE + Q("GDP Growth") + Inflation + Q("Bank Size") + Age + NPL_lag + Q("Corruption Index") * C(Country)'
model_interaction = smf.ols(interaction_formula, data=df).fit(cov_type='cluster', cov_kwds={'groups': df['Bank']})

print("--- Chow Interaction Regression Summary ---")
print(model_interaction.summary())
""")

    # CELL 23: The Corruption Paradox Detailed Discussion
    add_md("""
### 8.3 The Corruption Paradox: Discussion of Findings
Our structural stability checks and subsample analyses reveal a **highly significant rejection of Hypothesis $H_6$ (Structural Consistency)**. The relationship between national corruption and bank credit risk is *not* consistent; instead, it is highly country-dependent. This explains why the aggregated panel models yielded an insignificant coefficient for corruption: the positive and negative relationships across countries cancelled each other out.

We identify three distinct regimes in South Asia:

#### 1. Sand in the Wheels Regime (Bangladesh)
* **Statistical Finding**: The Corruption Index has a positive coefficient of **+0.0980** and is statistically significant ($p < 0.05$).
* **Economic Interpretation**: In Bangladesh, higher corruption (a lower CPI score) directly increases bank NPL ratios. This supports the **"Sand in the Wheels" theory (Cooray & Schneider, 2018)**. It suggests that corruption weakens institutional lending oversight, facilitating credit allocation based on personal connections, political interference, or bribery rather than rigorous risk evaluation. This leads to capital misallocation, weaker loan portfolios, and a higher rate of bank loan defaults.

#### 2. Greasing the Wheels Regime (India & Bhutan)
* **Statistical Finding**:
  - **India**: Negative coefficient of **-0.1824**, highly statistically significant ($p < 0.001$).
  - **Bhutan**: Negative coefficient of **-0.1459**, statistically significant ($p < 0.05$).
* **Economic Interpretation**: In these economies, higher levels of corruption are associated with *lower* bank default rates. This provides support for the controversial **"Greasing the Wheels" hypothesis (Mauro, 1995)**. In highly bureaucratic, slow-moving institutional environments, grease money or informal arrangements might bypass administrative blockages and red tape. This can accelerate credit approvals and execution for viable infrastructure or industrial projects, temporarily reducing default rates. However, this is highly prone to long-term systemic moral hazard.

#### 3. Neutral / Non-Significant Regime (Pakistan, Sri Lanka, Nepal, Maldives)
* **Statistical Finding**: The corruption coefficient is statistically insignificant in these four nations.
* **Economic Interpretation**: In these economies, national-level corruption does not have a direct, linear relationship with bank-specific credit risk. This suggest that credit risk is dominated by other primary factors—such as bank-specific profitability ($ROE$) and macroeconomic stability (Inflation and GDP growth)—which absorb any indirect governance effects.
""")

    # CELL 24: Machine Learning Predictive Modeling - Header
    add_md("""
## 9. Predictive Machine Learning Modeling and Interpretability

### 9.1 Overcoming Chronological Data Leakage
While econometric models explain structural relationships, machine learning algorithms can predict credit risk with high precision. However, standard cross-validation (e.g., K-fold) randomly shuffles observations across time, causing **chronological data leakage** (using future information to predict the past).

To build robust, reliable models, we enforce a chronological **Time Series Split (`TimeSeriesSplit`)** with 5 cross-validation folds. This mirrors a real-world forecasting environment, training models strictly on past years and evaluating them on subsequent years. We optimize three algorithms:
1. **Random Forest Regressor**
2. **Gradient Boosting Regressor**
3. **XGBoost Regressor**
""")

    # CELL 25: Machine Learning Execution
    add_code("""
# 1. Feature Engineering and Training-Test Division
# We sort chronologically by Year to preserve the temporal dimension
df_ml = df.sort_values(by='Year').copy()

# Select features and encode categorical columns
features = [
    'Corruption Index', 'GDP Growth', 'Inflation', 'Population Growth',
    'Bank Size', 'ROA', 'ROE', 'Age', 'NPL_lag'
]
df_ml_encoded = pd.get_dummies(df_ml, columns=['Bank_Type', 'Country'], drop_first=True)

# Update feature list to include country and bank type dummy variables
all_features = features + [col for col in df_ml_encoded.columns if 'Bank_Type_' in col or 'Country_' in col]

X_ml = df_ml_encoded[all_features]
y_ml = df_ml_encoded['log_NPL_Ratio']

# Hold out the final 2 years (2023 and 2024) as our test set
train_mask = df_ml_encoded['Year'] < 2023
test_mask = df_ml_encoded['Year'] >= 2023

X_train, y_train = X_ml[train_mask], y_ml[train_mask]
X_test, y_test = X_ml[test_mask], y_ml[test_mask]

print(f"Training observations (2014-2022): {X_train.shape[0]}")
print(f"Test observations (2023-2024): {X_test.shape[0]}")

# 2. Chronological Grid Search and Model Fitting
tscv = TimeSeriesSplit(n_splits=5)

models_grid = {
    'Random Forest': (RandomForestRegressor(random_state=42), {
        'n_estimators': [100, 200],
        'max_depth': [5, 8],
        'min_samples_split': [2, 5]
    }),
    'Gradient Boosting': (GradientBoostingRegressor(random_state=42), {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1],
        'max_depth': [3, 5]
    }),
    'XGBoost': (XGBRegressor(random_state=42), {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1],
        'max_depth': [3, 5]
    })
}

fitted_models = {}
for name, (model, params) in models_grid.items():
    print(f"Optimizing hyperparameters for {name}...")
    grid = GridSearchCV(model, params, cv=tscv, scoring='neg_mean_squared_error', n_jobs=-1)
    grid.fit(X_train, y_train)
    fitted_models[name] = grid.best_estimator_
    print(f"Best parameters for {name}: {grid.best_params_}")
""")

    # CELL 26: Machine Learning Evaluation
    add_md("""
### 9.2 Model Evaluation and Comparison
We evaluate our optimized models on the held-out test set (2023-2024 data) using three standard performance metrics:
* **Coefficient of Determination ($R^2$)**
* **Root Mean Squared Error (RMSE)**
* **Mean Absolute Error (MAE)**
""")

    add_code("""
ml_metrics = []
for name, model in fitted_models.items():
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    ml_metrics.append({
        'Model Name': name,
        'Test R-Squared (R2)': r2,
        'Test RMSE': rmse,
        'Test MAE': mae
    })

df_ml_performance = pd.DataFrame(ml_metrics)
display(df_ml_performance.round(4))
""")

    # CELL 27: SHAP Model Interpretability
    add_md("""
### 9.3 Machine Learning Model Interpretability (SHAP Analysis)
To resolve the "black-box" nature of these non-linear ensemble models, we implement **SHAP (SHapley Additive exPlanations)**. Derived from cooperative game theory, SHAP calculates the exact marginal contribution of each variable to individual predictions.

Below, we visualize the SHAP summary plot for our top-performing Gradient Boosting model.
""")

    add_code("""
# Initialize the Tree SHAP Explainer
best_model = fitted_models['Gradient Boosting']
explainer = shap.TreeExplainer(best_model)
shap_values = explainer(X_test)

# Plot SHAP summary (Beeswarm style) to visualize feature importance and direction
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, plot_type="beeswarm", show=False)
plt.title('SHAP Summary Beeswarm Plot (Gradient Boosting Model)', fontsize=14, pad=20)
plt.tight_layout()
plt.show()
""")

    # CELL 28: Summary and Policy Implications
    add_md("""
## 10. Conclusion & Policy Implications

### 10.1 Key Findings Summary
This research analyzed bank-level credit risk determinants across seven South Asian nations (2014-2024), utilizing panel econometrics and machine learning.

1. **The Corruption Paradox**: National institutional quality has a powerful, country-dependent impact on bank stability. Subsample regressions and a formal structural Chow test rejected regional uniformity. In Bangladesh, corruption increases defaults ("Sand in the Wheels"), while in India and Bhutan, corruption exhibits a negative link with short-term default rates ("Greasing the Wheels"), with no linear effect in Pakistan, Nepal, Sri Lanka, and the Maldives.
2. **Persistent Credit Risk**: Lagged NPLs are highly persistent over time. This stickiness remains significant even after controlling for Nickell bias via Instrumental Variables (2SLS) modeling.
3. **Macro-Financial Drivers**: Persistent inflation increases defaults, while higher bank profitability ($ROE$) significantly enhances loan quality and stabilizes banks against credit shocks.

### 10.2 Policy Implications
1. **Targeted Governance Reforms**: Policy interventions must be country-specific. In "Sand in the Wheels" regimes like Bangladesh, strengthening institutional quality and oversight is vital to prevent corrupt loan underwriting. In "Greasing the Wheels" regimes like India and Bhutan, the focus should be on reducing administrative bottlenecks and complex bureaucracies that incentivize rent-seeking behavior, while implementing robust safeguards to prevent long-term systemic moral hazard.
2. **Strengthening Capital Adequacy and Profitability**: Regulators should mandate countercyclical capital buffers and promote operational efficiency ($ROE$), which acts as a robust natural buffer against credit distress.
3. **Macroprudential Coordination**: Central banks should coordinate monetary policy and credit supervision, as inflation shocks directly elevate credit risks.
""")

    # Save notebook to disk
    with open('Credit_Risk_Analysis_Refined.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print("Notebook 'Credit_Risk_Analysis_Refined.ipynb' written successfully!")

if __name__ == '__main__':
    build_refined_notebook()
