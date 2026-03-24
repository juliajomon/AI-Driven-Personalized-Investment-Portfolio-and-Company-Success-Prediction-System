import requests

# Test portfolio query
test_data = {
    "query": "What companies are in my portfolio?",
    "user_id": 2  # User with saved portfolio
}

response = requests.post(
    "http://127.0.0.1:5000/decision-chat",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

print("Response:", response.json())
