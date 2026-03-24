import requests

def test_portfolio_companies():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    # Test with actual companies from portfolio
    portfolio_companies = ["MARICO.NS", "DRREDDY.NS", "HEROMOTOCO.NS", "NESTLEIND.NS", "ABBOTINDIA.NS"]
    
    for company in portfolio_companies:
        print(f"\n🔍 Testing: {company}")
        
        test_data = {
            "query": f"Why is {company} in my portfolio?",
            "user_id": 2
        }
        
        response = requests.post(
            base_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Query: {test_data['query']}")
        print(f"Response: {response.json()['response']}")
        print("-" * 80)

if __name__ == "__main__":
    test_portfolio_companies()
