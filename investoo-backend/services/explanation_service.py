import shap
import numpy as np
import joblib
import os

# Use the existing model file from the root directory
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'company_success_ensemble_model.pkl')
model = joblib.load(model_path)

# Use a masker for SHAP with the VotingClassifier
sample_data = np.array([[
    0.5, 0.7, 0.2, 0.6, 0.3, 1.5, 15.0, 2.1, 0.8, 100000, 5.2, 6.0, -0.1, 0.9, 8.0, 0.05, 1.2
]])
explainer = shap.Explainer(model.predict_proba, shap.sample(sample_data, 100))

feature_names = [
    "Market_Cap", "Revenue_CAGR_5Y", "Net_Profit_Margin_5Y_Avg", "ROE", 
    "Debt_to_Equity", "Current_Ratio", "Trailing_PE", "Altman_Z_Score", 
    "Op_Margin_Stability", "Free_Cash_Flow", "Interest_Coverage", 
    "Inventory_Turnover", "Debt_Reduction_Trend", "Asset_Turnover", 
    "Receivables_Turnover", "RnA_Intensity", "Cash_Conversion_Efficiency"
]

def get_feature_contributions(features):

    shap_values = explainer(features)

    # Handle multi-class SHAP values (take the mean across classes or use class 1)
    if len(shap_values.values.shape) > 1:
        values = shap_values.values[0]  # Take first sample
        if len(values.shape) > 1:
            values = values.mean(axis=0)  # Average across classes if multi-class
    else:
        values = shap_values.values[0]

    result = {}

    for i, val in enumerate(values):
        result[feature_names[i]] = round(float(val), 3)

    return result