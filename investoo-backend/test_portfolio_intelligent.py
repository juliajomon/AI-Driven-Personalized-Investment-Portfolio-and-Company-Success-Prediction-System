import requests

def test_portfolio_queries():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    test_cases = [
        {
            "name": "Portfolio Overview",
            "data": {
                "query": "What companies are in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Why Marico in portfolio",
            "data": {
                "query": "Why is Marico in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Why not TCS in portfolio",
            "data": {
                "query": "Why is TCS not in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Compare Marico vs TCS",
            "data": {
                "query": "Compare Marico vs TCS",
                "user_id": 2
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n🔍 Testing: {test['name']}")
        print(f"Query: {test['data']['query']}")
        
        response = requests.post(
            base_url,
            json=test['data'],
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response: {response.json()['response']}")
        print("-" * 80)

if __name__ == "__main__":
    test_portfolio_queries()
