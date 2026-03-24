import requests
import traceback

def test_with_error():
    base_url = "http://127.0.0.1:5000/decision-chat"
    
    # Test simple portfolio query
    test_data = {
        "query": "What companies are in my portfolio?",
        "user_id": 2
    }
    
    print(f"🔍 Testing: {test_data['query']}")
    
    try:
        response = requests.post(
            base_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Request error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_with_error()
