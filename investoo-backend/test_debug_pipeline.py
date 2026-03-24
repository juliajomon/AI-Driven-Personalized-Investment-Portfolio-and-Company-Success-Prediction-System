import requests

def test_debug_pipeline():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    # Test with exact company name
    test_data = {
        "query": "Why is MARICO in my portfolio?",
        "user_id": 2
    }
    
    print(f"🔍 Testing: {test_data['query']}")
    print(f"Expected: MARICO should be in portfolio")
    
    response = requests.post(
        base_url,
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"Response: {result['response']}")
    
    # Also test with TCS
    test_data2 = {
        "query": "Why is TCS not in my portfolio?",
        "user_id": 2
    }
    
    print(f"\n🔍 Testing: {test_data2['query']}")
    print(f"Expected: TCS should not be in portfolio")
    
    response2 = requests.post(
        base_url,
        json=test_data2,
        headers={"Content-Type": "application/json"}
    )
    
    result2 = response2.json()
    print(f"Response: {result2['response']}")

if __name__ == "__main__":
    test_debug_pipeline()
