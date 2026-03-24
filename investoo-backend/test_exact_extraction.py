import requests

def test_detailed_extraction():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    # Test with exact company names from portfolio
    test_cases = [
        {
            "name": "Exact MARICO",
            "data": {
                "query": "Why is MARICO in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Exact MARICO.NS",
            "data": {
                "query": "Why is MARICO.NS in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Exact TCS.NS",
            "data": {
                "query": "Why is TCS.NS not in my portfolio?",
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
    test_detailed_extraction()
