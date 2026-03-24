import requests

def test_company_extraction():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    test_cases = [
        {
            "name": "Why Marico",
            "data": {
                "query": "Why is Marico in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Why not TCS", 
            "data": {
                "query": "Why is TCS not in my portfolio?",
                "user_id": 2
            }
        },
        {
            "name": "Direct Marico",
            "data": {
                "query": "Marico",
                "user_id": 2
            }
        },
        {
            "name": "Direct TCS",
            "data": {
                "query": "TCS", 
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
    test_company_extraction()
