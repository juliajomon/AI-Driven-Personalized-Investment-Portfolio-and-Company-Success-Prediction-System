import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_user_portfolio(user_id):
    """
    Fetch user's portfolio from database using existing saved_portfolios table
    Returns list of company tickers in portfolio
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print(f"🔍 DB Connection: Connected successfully")
        print(f"🔍 Querying saved_portfolios for user_id: {user_id}")
        
        cursor.execute("""
            SELECT portfolio_json 
            FROM saved_portfolios 
            WHERE user_id = %s
        """, (user_id,))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Extract company symbols from portfolio JSON
        portfolio_companies = []
        
        for row in results:
            portfolio_json = row.get('portfolio_json', '[]')
            if isinstance(portfolio_json, str):
                try:
                    portfolio_data = json.loads(portfolio_json)
                except:
                    portfolio_data = []
            elif isinstance(portfolio_json, (list, dict)):
                portfolio_data = portfolio_json
            else:
                portfolio_data = []
            
            # Extract company symbols from portfolio data
            for item in portfolio_data:
                if isinstance(item, dict):
                    # Look for ticker field first, then symbol
                    ticker = item.get('ticker', item.get('symbol', ''))
                    if ticker:
                        portfolio_companies.append(ticker)
                elif isinstance(item, str):
                    portfolio_companies.append(item)
        
        # Normalize company names
        def normalize(name):
            return name.replace(".NS", "").upper().strip()
        
        portfolio_companies = [normalize(c) for c in portfolio_companies]
        
        # Debug: Log portfolio status
        if portfolio_companies:
            print(f"✅ Found {len(portfolio_companies)} companies in saved_portfolios for user {user_id}: {portfolio_companies}")
        else:
            print(f"ℹ️ No portfolio found for user {user_id}")
            
        return portfolio_companies
        
    except Exception as e:
        print("Portfolio fetch error:", e)
        return []
