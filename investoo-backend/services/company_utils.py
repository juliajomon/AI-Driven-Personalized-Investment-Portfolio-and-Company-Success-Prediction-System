import pandas as pd
from rapidfuzz import process

def load_company_map():
    df = pd.read_csv("nifty_200_final_predictions.csv") 

    company_map = {}

    for _, row in df.iterrows():
        name = row["Name"].lower()
        ticker = row["Ticker"]

        # full name
        company_map[name] = ticker

        # short name (first word)
        short = name.split()[0]
        company_map[short] = ticker

    return company_map



company_map = load_company_map()

def extract_companies(query, default=None):
    query = query.lower()

    matches = process.extract(
        query,
        company_map.keys(),
        limit=2,
        score_cutoff=70
    )

    if not matches:
        return default, None

    tickers = [company_map[m[0]] for m in matches]

    if len(tickers) == 1:
        return tickers[0], None

    return tickers[0], tickers[1]