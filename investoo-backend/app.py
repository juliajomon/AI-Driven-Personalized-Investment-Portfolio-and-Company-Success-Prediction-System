from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib
import cvxpy as cp
import yfinance as yf
import os
import requests
import io
import re
import atexit
from datetime import datetime
import json
from database.portfolio_repository import save_portfolio, get_saved_portfolios
from database.search_repository import save_search, get_search_history
from database.users_repository import create_user, authenticate_user
from routes.decision_chat import decision_chat_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Register Blueprint for decision chat
app.register_blueprint(decision_chat_bp, url_prefix='')

SHEET_ID = "1aGdGywmxsmFlXcaF9Th0TM4BOsT7A9LFoRCQyMzE0Ew"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

MODEL_FILE = 'company_success_ensemble_model.pkl'
DATA_FILE = 'nifty_200_cleaned_for_ml.csv'
PREDICTIONS_FILE = 'nifty_200_final_predictions.csv'

model = None
df_preds = None

def get_clean_ticker(raw_name):
    if pd.isna(raw_name) or str(raw_name).strip() == "": return None
    
    cleaned_key = re.sub(r'[^a-z0-9]', '', str(raw_name).lower())

    skip_keys = [
        "tatacapital", "lenskart", "lgelectronics", "vishalmegamart", 
        "knowledgerealty", "hexaware", "smartworks", "swiggy", 
        "hyundaimotor", "oyoroom", "boat", "hdbfinancial", 
        "hdbfinancser", "altius", "billionbrains"
    ]
    for k in skip_keys:
        if k in cleaned_key: return "SKIP"

    mapping = {

        "motiloswalfin": "MOTILALOFS.NS",  "lindeindia": "LINDEINDIA.NS",    "linde": "LINDEINDIA.NS",
        "balkrishnainds": "BALKRISIND.NS",  "supremeinds": "SUPREMEIND.NS",
        "relianceindustr": "RELIANCE.NS",
        "infosys": "INFY.NS",
        "tcs": "TCS.NS",
        "hcltechnologies": "HCLTECH.NS",
        "wipro": "WIPRO.NS",
        "techmahindra": "TECHM.NS",
        "ltimindtree": "LTIM.NS",
        "bhartiairtel": "BHARTIARTL.NS",
        "sunpharmainds": "SUNPHARMA.NS",
        "hindunilever": "HINDUNILVR.NS",
        "itc": "ITC.NS",
        "larsentoubro": "LT.NS",
        "mm": "M&M.NS", "mahindramahindra": "M&M.NS",
        
        "hdfcbank": "HDFCBANK.NS",
        "icicibank": "ICICIBANK.NS",
        "axisbank": "AXISBANK.NS",
        "kotakmahbank": "KOTAKBANK.NS",
        "sbi": "SBIN.NS", "statebankofindia": "SBIN.NS",
        "bajajfinance": "BAJFINANCE.NS",
        "bajajfinserv": "BAJAJFINSV.NS",
        "jiofinancial": "JIOFIN.NS",
        "hdfclifeinsur": "HDFCLIFE.NS",
        "sbilifeinsuran": "SBILIFE.NS",
        "iciciprulife": "ICICIPRULI.NS",
        "powerfincorpn": "PFC.NS",
        "recltd": "RECLTD.NS", "rec": "RECLTD.NS",
        "cholamaninvfn": "CHOLAFIN.NS", "cholaminvf": "CHOLAFIN.NS",
        "shriramfinance": "SHRIRAMFIN.NS",
        "muthootfinance": "MUTHOOTFIN.NS",
        "bajajhousing": "BAJAJHFL.NS",
        "bankofbaroda": "BANKBARODA.NS",
        "punjabnatlbank": "PNB.NS",
        "canarabank": "CANBK.NS",
        "unionbanki": "UNIONBANK.NS",
        "indianbank": "INDIANB.NS",
        "idbibank": "IDBI.NS",
        "ausmallfinance": "AUBANK.NS",
        "idfcfirstbank": "IDFCFIRSTB.NS",
        "federalbank": "FEDERALBNK.NS",
        "bankofindia": "BANKINDIA.NS",
        "adityabirlacap": "ABCAPITAL.NS",
        "ltfinanceltd": "LTF.NS", "ltfinance": "LTF.NS",
        "mmfinserv": "M&MFIN.NS",
        "maxfinancial": "MFSL.NS",
        "sundaramfinance": "SUNDARMFIN.NS",
        "bankofmaha": "MAHABANK.NS",
        "authuminvest": "AIIL.NS", "authum": "AUTHUM.NS",

        "marutisuzuki": "MARUTI.NS",
        "tatamotors": "TATAMOTORS.NS",
        "bajajauto": "BAJAJ-AUTO.NS",
        "eichermotors": "EICHERMOT.NS",
        "tvsmotorco": "TVSMOTOR.NS",
        "heromotocorp": "HEROMOTOCO.NS",
        "ashokleyland": "ASHOKLEY.NS",
        "samvardhmothe": "MOTHERSON.NS", "motherson": "MOTHERSON.NS",
        "bharatforge": "BHARATFORG.NS",
        "tubeinvestments": "TIINDIA.NS",
        "escortskubota": "ESCORTS.NS",
        "bosch": "BOSCHLTD.NS",
        "schaefflerindia": "SCHAEFFLER.NS",
        "siemens": "SIEMENS.NS", "siemensenerin": "SIEMENS.NS",
        "cgpowerind": "CGPOWER.NS", "cgpower": "CGPOWER.NS",
        "bharatelectron": "BEL.NS",
        "cochinshipyard": "COCHINSHIP.NS",
        "mazagondock": "MAZDOCK.NS",
        "hitachienergy": "POWERINDIA.NS",
        "lttechnology": "LTTS.NS",
        "premierenergie": "PREMIERENE.NS",
        "kpitrtechnologi": "KPITTECH.NS",
        "mphasis": "MPHASIS.NS",
        "persistentsystems": "PERSISTENT.NS",
        "tataomm": "TATACOMM.NS",

        "ntpc": "NTPC.NS",
        "powergridcorpn": "POWERGRID.NS",
        "coalindia": "COALINDIA.NS",
        "iocl": "IOC.NS", "indianoilcorp": "IOC.NS",
        "bpcl": "BPCL.NS", "bharatpetr": "BPCL.NS",
        "gailindia": "GAIL.NS",
        "petronetlng": "PETRONET.NS", "petronet": "PETRONET.NS",
        "oilindia": "OIL.NS",
        "tatasteel": "TATASTEEL.NS",
        "jswsteel": "JSWSTEEL.NS",
        "hindalcoinds": "HINDALCO.NS",
        "vedanta": "VEDL.NS",
        "hindustanzinc": "HINDZINC.NS",
        "jindalsteel": "JINDALSTEL.NS",
        "jindalstain": "JSL.NS", "jindalstainless": "JSL.NS",
        "adanienterp": "ADANIENT.NS",
        "adanienergysol": "ADANIENSOL.NS",
        "adanitotalgas": "ATGL.NS",
        "adaniports": "ADANIPORTS.NS",
        "adanigreenener": "ADANIGREEN.NS",
        "adanipower": "ADANIPOWER.NS",
        "ambujacements": "AMBUJACEM.NS",
        "ultratechcem": "ULTRACEMCO.NS",
        "shreecement": "SHREECEM.NS",
        "jkcements": "JKCEMENT.NS",
        "grasiminds": "GRASIM.NS",
        "asianpaints": "ASIANPAINT.NS",
        "bergerpaints": "BERGEPAINT.NS",
        "pidilite": "PIDILITIND.NS", 
        "solarindustries": "SOLARINDS.NS",
        "piindustries": "PIIND.NS",
        "coromandelinter": "COROMANDEL.NS",
        "upl": "UPL.NS",
        "lloydsmetals": "LLOYDSME.NS",
        "tatapowerco": "TATAPOWER.NS",
        "jswenergy": "JSWENERGY.NS",
        "nhpc": "NHPC.NS",
        "sjvn": "SJVN.NS",
        "waareeenergies": "WAAREEENER.NS",
        "suzlonenergy": "SUZLON.NS",
        "torrentpower": "TORNTPOWER.NS",
        "gevernovatd": "GET&D.NS",
        "lindenindia": "LINDEINDIA.NS",
        "aplapollotubes": "APLAPOLLO.NS",
        "sail": "SAIL.NS", "nmdc": "NMDC.NS",

        "drreddyslabs": "DRREDDY.NS",
        "cipla": "CIPLA.NS",
        "divislab": "DIVISLAB.NS",
        "zyduslifesci": "ZYDUSLIFE.NS",
        "mankindpharma": "MANKIND.NS",
        "torrentpharma": "TORNTPHARM.NS",
        "lupin": "LUPIN.NS",
        "aurobindopharma": "AUROPHARMA.NS",
        "alkemlab": "ALKEM.NS",
        "abbottindia": "ABBOTINDIA.NS",
        "glenmarkpharma": "GLENMARK.NS",
        "glaxosmipharm": "GLAXO.NS",
        "apollohospitals": "APOLLOHOSP.NS",
        "maxhealthcare": "MAXHEALTH.NS",
        "fortishealth": "FORTIS.NS",
        "titancompany": "TITAN.NS",
        "nestleindia": "NESTLEIND.NS",
        "britanniainds": "BRITANNIA.NS",
        "godrejconsumer": "GODREJCP.NS",
        "tataconsumer": "TATACONSUM.NS",
        "daburindia": "DABUR.NS",
        "varunbeverages": "VBL.NS",
        "havellsindia": "HAVELLS.NS",
        "polycabindia": "POLYCAB.NS",
        "dixontechnolog": "DIXON.NS",
        "voltas": "VOLTAS.NS",
        "unitedspirits": "MCDOWELL-N.NS",
        "unitedbreweries": "UBL.NS",
        "radicokhaitan": "RADICO.NS",
        "colgatepalmoliv": "COLPAL.NS",
        "pageindustries": "PAGEIND.NS",
        "trent": "TRENT.NS",
        "avenuesuper": "DMART.NS",
        "zomato": "ZOMATO.NS",
        "pbfintech": "POLICYBZR.NS",
        "fsnecommerce": "NYKAA.NS",
        "infoedgindia": "NAUKRI.NS",
        "interglobeaviat": "INDIGO.NS",
        "irfc": "IRFC.NS",
        "railvikas": "RVNL.NS",
        "concor": "CONCOR.NS",
        "dlf": "DLF.NS",
        "godrejpropert": "GODREJPROP.NS",
        "oberoirealty": "OBEROIRLTY.NS",
        "prestigeestates": "PRESTIGE.NS",
        "lodhadevelopers": "LODHA.NS",
        "phoenixmills": "PHOENIXLTD.NS",
        "industowers": "INDUSTOWER.NS",
        "bhartihexacom": "BHARTIHEXA.NS",
        "indianhotelsc": "INDHOTEL.NS",
        "patanjalifoods": "PATANJALI.NS",
        "kalyanjewellers": "KALYANKJIL.NS",
        "nipponlifeind": "NAM-INDIA.NS",
        "jswinfrast": "JSWINFRA.NS",
        "godfreyphillips": "GODFRYPHLP.NS"
    }
    
    if cleaned_key in mapping: return mapping[cleaned_key]
    
    for key, val in mapping.items():
        if key in cleaned_key or cleaned_key in key:
            if len(key) > 3: return val
            
    clean = re.sub(r'[^a-zA-Z0-9]', '', str(raw_name)).upper().replace("LTD","").replace("INDIA","")
    return f"{clean}.NS"

def safe_loc(df, key, default=pd.Series(dtype='float64')):
    if df.empty: return default
    try: return df.loc[key] if key in df.index else default
    except: return default

def regularize_cov(matrix, eps=1e-8):
    mat = np.array(matrix, dtype=float)
    if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
        raise ValueError("Covariance matrix must be square.")

    min_eig = np.min(np.real(np.linalg.eigvals(mat)))
    if min_eig < eps:
        mat += np.eye(mat.shape[0]) * (eps - min_eig + 1e-8)
    return mat

def fetch_hybrid_data(row):
    ticker = row['Ticker']
    try:
        sheet_roe = float(str(row.get('ROE %', 0)).replace(',', ''))
        sheet_pe = float(str(row.get('P/E', 0)).replace(',', ''))
        sheet_debt = float(str(row.get('Debt / Eq', 0)).replace(',', ''))
        sheet_curr_ratio = float(str(row.get('Current ratio', 0)).replace(',', ''))
        sheet_sales_growth = float(str(row.get('Sales growth %', 0)).replace(',', ''))
        sheet_mkt_cap = float(str(row.get('Mar Cap Rs.Cr.', 0)).replace(',', ''))
    except:
        sheet_roe = sheet_pe = sheet_debt = sheet_curr_ratio = sheet_sales_growth = sheet_mkt_cap = 0

    kpis = {
        'Ticker': ticker, 'Name': row.get('Name', 'Unknown'), 'Sector': 'Unknown',
        'Market_Cap': sheet_mkt_cap, 'Revenue_CAGR_5Y': sheet_sales_growth / 100.0,
        'Net_Profit_Margin_5Y_Avg': float(str(row.get('NPM Ann %', 0)).replace(',', '')) / 100.0,
        'ROE': sheet_roe, 'Debt_to_Equity': sheet_debt, 'Current_Ratio': sheet_curr_ratio,
        'Trailing_PE': sheet_pe, 'Altman_Z_Score': np.nan, 'Op_Margin_Stability': np.nan,
        'Free_Cash_Flow': np.nan, 'Interest_Coverage': np.nan, 'Inventory_Turnover': np.nan,
        'Debt_Reduction_Trend': np.nan, 'Asset_Turnover': np.nan,
        'Receivables_Turnover': np.nan, 'RnA_Intensity': np.nan, 'Cash_Conversion_Efficiency': np.nan
    }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        fin = stock.financials
        bs = stock.balance_sheet
        cf = stock.cashflow

        if 'sector' in info: kpis['Sector'] = info['sector']
        
        revenue = safe_loc(fin, 'Total Revenue')
        ebit = safe_loc(fin, 'EBIT')
        total_assets = safe_loc(bs, 'Total Assets')
        op_cash = safe_loc(cf, 'Operating Cash Flow')
        capex = safe_loc(cf, 'Capital Expenditure')
        interest = safe_loc(fin, 'Interest Expense')
        net_income = safe_loc(fin, 'Net Income')
        receivables = safe_loc(bs, 'Receivables')
        rnd = safe_loc(fin, 'Research And Development')
        total_debt = safe_loc(bs, 'Total Debt')

        def get_stability(series): return 1 / (series.std() + 1e-5) if len(series) > 2 else np.nan
        def get_slope(series): return np.polyfit(np.arange(len(series.dropna())), series.dropna().values, 1)[0] if len(series.dropna()) > 2 else np.nan

        if not revenue.empty and not ebit.empty: kpis['Op_Margin_Stability'] = get_stability(ebit / revenue)
        if not op_cash.empty: kpis['Free_Cash_Flow'] = op_cash.iloc[0] + (capex.iloc[0] if not capex.empty else 0)
        if not ebit.empty and not interest.empty and interest.iloc[0] != 0: kpis['Interest_Coverage'] = ebit.iloc[0] / interest.iloc[0]
        if not total_debt.empty: kpis['Debt_Reduction_Trend'] = get_slope(total_debt)
        if not revenue.empty and not total_assets.empty and total_assets.iloc[0] != 0: kpis['Asset_Turnover'] = revenue.iloc[0] / total_assets.iloc[0]
        if not revenue.empty and not receivables.empty and receivables.iloc[0] != 0: kpis['Receivables_Turnover'] = revenue.iloc[0] / receivables.iloc[0]
        if not rnd.empty and not revenue.empty and revenue.iloc[0] != 0: kpis['RnA_Intensity'] = rnd.iloc[0] / revenue.iloc[0]
        if not op_cash.empty and not net_income.empty and net_income.iloc[0] != 0: kpis['Cash_Conversion_Efficiency'] = op_cash.iloc[0] / net_income.iloc[0]

        try:
            curr_assets = safe_loc(bs, 'Current Assets').iloc[0]
            curr_liab = safe_loc(bs, 'Current Liabilities').iloc[0]
            working_cap = curr_assets - curr_liab
            retained_earn = safe_loc(bs, 'Retained Earnings').iloc[0]
            ta = total_assets.iloc[0]
            A, B, C = working_cap/ta, retained_earn/ta, ebit.iloc[0]/ta
            D = kpis['Market_Cap'] / (safe_loc(bs, 'Total Liabilities Net Minority Interest').iloc[0])
            E = revenue.iloc[0] / ta
            kpis['Altman_Z_Score'] = (1.2*A) + (1.4*B) + (3.3*C) + (0.6*D) + (1.0*E)
        except:
            kpis['Altman_Z_Score'] = (sheet_roe/10.0) + sheet_curr_ratio - sheet_debt + 2.0
    except: pass
    return kpis

def perform_full_update(force=False):
    now = datetime.now()
    
    if not force:
        if now.weekday() != 0 or now.hour != 8:
            print(f" Skipping scheduled update. Time: {now}. Next run: Monday 8 AM.")
            return

    print("\n PERFORMING SYSTEM UPDATE (This takes 2-3 mins)...")
    try:
        global df_preds, model
        
        print("   ⬇️  Downloading Market Data...")
        response = requests.get(CSV_URL)
        df_sheet = pd.read_csv(io.BytesIO(response.content))
        df_sheet = df_sheet[df_sheet['Name'] != 'Name'].dropna(subset=['Name'])
        
        new_data = []
        for i, row in df_sheet.iterrows():
            ticker = get_clean_ticker(row['Name'])
            if ticker and ticker != "SKIP":
                row['Ticker'] = ticker
                kpis = fetch_hybrid_data(row)
                if kpis: new_data.append(kpis)
        
        df_new = pd.DataFrame(new_data)
        df_new = df_new.replace([np.inf, -np.inf], np.nan)
        
        print("   🧹 Cleaning Data...")
        numeric_cols = df_new.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df_new[col].isnull().all(): df_new[col] = 0.0
            
        imputer = SimpleImputer(strategy='median')
        df_new[numeric_cols] = imputer.fit_transform(df_new[numeric_cols])
        df_new = df_new.fillna(0)
        
        print("  Training AI Model...")
        feature_cols = [
            'Market_Cap', 'Revenue_CAGR_5Y', 'Net_Profit_Margin_5Y_Avg', 'ROE', 
            'Debt_to_Equity', 'Current_Ratio', 'Trailing_PE', 'Altman_Z_Score', 
            'Op_Margin_Stability', 'Free_Cash_Flow', 'Interest_Coverage', 
            'Inventory_Turnover', 'Debt_Reduction_Trend', 'Asset_Turnover', 
            'Receivables_Turnover', 'RnA_Intensity', 'Cash_Conversion_Efficiency'
        ]
        
        for col in feature_cols:
            if col not in df_new.columns: df_new[col] = 0.0
            
        X = df_new[feature_cols]
        y = ((df_new['ROE'] > 12) & (df_new['Altman_Z_Score'] > 1.8)).astype(int)
        
        if y.sum() < 5: # Fallback if not enough "Success" rows
             y = (df_new['ROE'] > 10).astype(int)

        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
        
        ensemble = VotingClassifier(estimators=[('rf', rf), ('xgb', xgb)], voting='soft')
        ensemble.fit(X, y)
        model = ensemble 
        
        probs = ensemble.predict_proba(X)[:, 1]
        df_new['AI_Success_Probability'] = (probs * 100).round(2)
        df_new['AI_Recommendation'] = df_new['AI_Success_Probability'].apply(
            lambda x: "Strong Buy" if x >= 80 else "Buy" if x >= 60 else "Hold" if x >= 40 else "Avoid"
        )

        print("   Saving Files Locally...")
        df_new.to_csv(DATA_FILE, index=False)
        df_new.to_csv(PREDICTIONS_FILE, index=False)
        joblib.dump(ensemble, MODEL_FILE)
        
        df_preds = df_new
        print(" UPDATE COMPLETE & LOADED.")
        
    except Exception as e:
        print(f" Update Failed: {e}")

@app.route('/', methods=['GET'])
def home(): return jsonify({"status": "online"})

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    if df_preds is None: return jsonify({"error": "Data not ready"}), 500
    return jsonify(df_preds.head(50).to_dict(orient='records'))


@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user_id = create_user(email, password)
        # simple token placeholder (frontend only uses presence)
        return jsonify({"user_id": user_id, "token": f"user-{user_id}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user_id = authenticate_user(email, password)
        if not user_id:
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({"user_id": user_id, "token": f"user-{user_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    try:
        data = request.json or {}
        investment_amount = float(data.get('amount', 100000))
        target_return_pct = float(data.get('target_return', 20)) / 100.0 
        user_id = data.get('user_id')
        if user_id is None:
            return jsonify({"error": "user_id is required"}), 400
        
        if df_preds is None: return jsonify({"error": "Server data missing/loading."}), 500

        candidates = df_preds[df_preds['AI_Success_Probability'] > 80].copy()
        candidates = candidates.sort_values(by='AI_Success_Probability', ascending=False).head(15)
        tickers = candidates['Ticker'].tolist()
        
        if len(tickers) < 2: return jsonify({"error": "Not enough strong buy stocks."}), 400

        prices = yf.download(tickers, period="1y", progress=False, threads=False)['Close']
        prices = prices.dropna(axis=1, thresh=int(len(prices)*0.9)).fillna(method='ffill').fillna(method='bfill')
        valid_tickers = prices.columns.tolist()

        returns = prices.pct_change().dropna()
        mu = returns.mean().values * 252
        Sigma = np.cov(returns.values, rowvar=False) * 252
        n = len(valid_tickers)

        if np.isnan(Sigma).any(): return jsonify({"error": "Unstable market data."}), 500

        w_primary = cp.Variable(n)
        risk_primary = cp.quad_form(w_primary, Sigma)
        
        primary_constraints = [
            cp.sum(w_primary) == 1, w_primary >= 0, w_primary <= 0.30, 
            (mu @ w_primary) >= target_return_pct
        ]
        prob_primary = cp.Problem(cp.Minimize(risk_primary), primary_constraints)
        prob_primary.solve(solver=cp.OSQP)

        
        is_gmvp_fallback = False
        if w_primary.value is None or prob_primary.status not in ["optimal", "optimal_inaccurate"]:
            
            w_gmvp = cp.Variable(n)
            gmvp_constraints = [cp.sum(w_gmvp) == 1, w_gmvp >= 0, w_gmvp <= 0.30]
            prob_gmvp = cp.Problem(cp.Minimize(cp.quad_form(w_gmvp, Sigma)), gmvp_constraints)
            prob_gmvp.solve(solver=cp.OSQP)
            
            if w_gmvp.value is None: return jsonify({"error": "Optimization failed completely."}), 500
            
            weights = w_gmvp.value
            is_gmvp_fallback = True
        else:
            weights = w_primary.value

        final_exp_return = float(np.dot(weights, mu))
        final_risk = float(np.sqrt(np.dot(Sigma @ weights, weights)))
        final_sharpe = final_exp_return / final_risk

        allocation = []
        for i, t in enumerate(valid_tickers):
            weight = float(weights[i])
            if weight > 0.01:
                meta = candidates[candidates['Ticker'] == t]
                name = meta['Name'].values[0] if not meta.empty else t
                sector = meta['Sector'].values[0] if not meta.empty else "Unknown"

                allocation.append({
                    "ticker": t,
                    "name": name,
                    "sector": sector,
                    "weight": round(weight, 4),
                    "value": round(weight * investment_amount, 2)
                })

        # persist this search in search_history (all runs)
        try:
            portfolio_json = json.dumps(allocation)
            save_search(
                user_id=int(user_id) if user_id is not None else 1,
                amount=float(investment_amount),
                risk_rate=float(final_risk * 100.0),
                expected_return=float(final_exp_return * 100.0),
                portfolio_json=portfolio_json,
            )
        except Exception as e:
            print(f" Search history save error: {e}")

        warning_level = "SUCCESS"
        warning_message = f"Optimal solution found. Target achieved ({final_exp_return*100:.1f}%) with high efficiency (Sharpe: {final_sharpe:.2f})."
        
        if final_exp_return > 0.05 and final_sharpe < 1.05:
            warning_level = "ADJUST"
            
            if is_gmvp_fallback:
                warning_message = f"HIGH RISK WARNING: Volatility ({final_risk*100:.1f}%) is high for your return. Sharpe Ratio ({final_sharpe:.2f}) is below the efficiency standard (1.25). Lower your target return to reduce risk."

            else:
                warning_message = f"WARNING: Portfolio is at minimum risk (GMVP). Sharpe ({final_sharpe:.2f}) is low. Increase your target return to improve efficiency."
       
        return jsonify({
            "status": warning_level,
            "message": warning_message,
            "portfolio": sorted(allocation, key=lambda x: x['weight'], reverse=True),
            "metrics": {
                "expected_return": round(final_exp_return * 100, 2),
                "estimated_risk": round(final_risk * 100, 2),
                "sharpe_ratio": round(final_sharpe, 2)
            }
        })

    except Exception as e:
        print(f" Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
@app.route('/api/save-portfolio', methods=['POST'])
def save_portfolio_route():
    try:
        data = request.get_json(silent=True) or {}

        # accept both snake_case and camelCase from frontend
        user_id = data.get('user_id', None)
        if user_id is None:
            user_id = data.get('userId', None)

        amount = data.get('amount', None)

        risk_rate = data.get('risk_rate', None)
        if risk_rate is None:
            risk_rate = data.get('riskRate', None)

        expected_return = data.get('expected_return', None)
        if expected_return is None:
            expected_return = data.get('expectedReturn', None)

        portfolio = data.get('portfolio') or []

        missing = []
        if user_id is None:
            missing.append("user_id")
        if amount is None:
            missing.append("amount")
        if expected_return is None:
            missing.append("expected_return")

        if missing:
            return jsonify(
                {
                    "error": "Missing required fields",
                    "missing": missing,
                    "received_keys": list(data.keys()),
                }
            ), 400

        portfolio_id = save_portfolio(
            int(user_id),
            float(amount),
            float(risk_rate) if risk_rate is not None else None,
            float(expected_return),
            json.dumps(portfolio),
        )

        return jsonify({"id": portfolio_id}), 201

    except Exception as e:
        print("SAVE ERROR:", e)
        return jsonify({"error": str(e)}), 500
@app.route('/api/search-history', methods=['GET'])
def get_search_history_route():
    try:
        user_id = request.args.get('user_id', default=1, type=int)
        history = get_search_history(user_id)
        return jsonify(history)
    except Exception as e:
        print(f" Get search history error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/saved-portfolios', methods=['GET'])
def get_saved_portfolios_route():
    try:
        user_id = request.args.get('user_id', type=int)
        if user_id is None:
            return jsonify({"error": "user_id is required"}), 400
        portfolios = get_saved_portfolios(user_id=user_id)
        return jsonify(portfolios)
    except Exception as e:
        print(f" Get saved portfolios error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 5. STARTUP (With Self-Healing)
if __name__ == "__main__":
    print(" Server Starting...")

    try:
        if os.path.exists(PREDICTIONS_FILE) and os.path.exists(MODEL_FILE):
            print(" Found existing data. Loading...")
            model = joblib.load(MODEL_FILE)
            df_preds = pd.read_csv(PREDICTIONS_FILE)
            print(f"   - Loaded {len(df_preds)} stocks.")
        else:
            print("\n  Data files missing. Running INITIAL SETUP (This takes ~2 mins)...")
            perform_full_update(force=True)

    except Exception as e:
        print(f"\n Critical Artifact Error ({e}). Running REBUILD...")
        perform_full_update(force=True)

    print(f"\n Serving on http://127.0.0.1:5000")
    app.run(debug=True, port=5000, use_reloader=False)