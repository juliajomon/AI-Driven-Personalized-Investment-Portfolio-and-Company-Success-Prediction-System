import requests

def test_simple():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    # Test simple portfolio query
    test_data = {
        "query": "What companies are in my portfolio?",
        "user_id": 2
    }
    
    print(f"🔍 Testing: {test_data['query']}")
    
    response = requests.post(
        base_url,
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test simple company query
    test_data2 = {
        "query": "Why is TCS not in my portfolio?",
        "user_id": 2
    }
    
    print(f"\n🔍 Testing: {test_data2['query']}")
    
    response2 = requests.post(
        base_url,
        json=test_data2,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")

if __name__ == "__main__":
    test_simple()
