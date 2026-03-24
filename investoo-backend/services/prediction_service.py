import joblib
import numpy as np
import pandas as pd
import os

# 🔹 Load model
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'company_success_ensemble_model.pkl')
model = joblib.load(model_path)

# 🔹 Load CSV
csv_path = r"E:\AI-Driven-Personalized-Investment-Portfolio-and-Company-Success-Prediction-System\investoo-backend\nifty_200_final_predictions.csv"
print(f"🔍 Current working directory: {os.getcwd()}")
print(f"🔍 CSV path: {csv_path}")
print(f"🔍 CSV exists: {os.path.exists(csv_path)}")
df = pd.read_csv(csv_path)

# 🔥 Ensure column names are clean
df.columns = df.columns.str.strip()


def get_company_features(company):

    # 🔥 Match ticker (try both with and without .NS)
    if not company.endswith('.NS'):
        company = company + '.NS'
    
    row = df[df["Ticker"] == company]

    if row.empty:
        print("Company not found in CSV:", company)
        return np.array([[0.5] * 17])  # fallback

    # 🔥 Drop non-feature columns (Ticker, Name, Sector, AI_Success_Probability, AI_Recommendation)
    feature_values = row.drop(columns=["Ticker", "Name", "Sector", "AI_Success_Probability", "AI_Recommendation"], errors='ignore').values

    return feature_values


def get_company_prediction(company):

    features = get_company_features(company)
    
    # Create feature names that match what the model expects
    feature_names = [
        "Market_Cap", "Revenue_CAGR_5Y", "Net_Profit_Margin_5Y_Avg", "ROE", 
        "Debt_to_Equity", "Current_Ratio", "Trailing_PE", "Altman_Z_Score", 
        "Op_Margin_Stability", "Free_Cash_Flow", "Interest_Coverage", 
        "Inventory_Turnover", "Debt_Reduction_Trend", "Asset_Turnover", 
        "Receivables_Turnover", "RnA_Intensity", "Cash_Conversion_Efficiency"
    ]
    
    # Create DataFrame with proper column names
    features_df = pd.DataFrame(features, columns=feature_names)
    
    prob = model.predict_proba(features_df)[0][1]

    return round(prob, 2), features