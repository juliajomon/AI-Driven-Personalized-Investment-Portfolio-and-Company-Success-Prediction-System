from services.prompt_service import generate_response

# Test the prompt service directly with correct company data
def test_prompt_service_direct():
    
    # Test case 1: MARICO is in portfolio
    context1 = {
        "company": "MARICO.NS",
        "prediction": 0.65,
        "features": {"ROE": 0.15, "Growth": 0.12},
        "confidence": "Moderate Confidence",
        "portfolio_companies": ["MARICO", "DRREDDY", "HEROMOTOCO", "NESTLEIND", "ABBOTINDIA"]
    }
    
    print("🔍 Test 1: MARICO in portfolio")
    response1 = generate_response("Why is MARICO in my portfolio?", context1)
    print(f"Response: {response1}")
    print("-" * 80)
    
    # Test case 2: TCS is not in portfolio
    context2 = {
        "company": "TCS.NS", 
        "prediction": 0.97,
        "features": {"ROE": 0.25, "Growth": 0.18},
        "confidence": "High Confidence",
        "portfolio_companies": ["MARICO", "DRREDDY", "HEROMOTOCO", "NESTLEIND", "ABBOTINDIA"]
    }
    
    print("🔍 Test 2: TCS not in portfolio")
    response2 = generate_response("Why is TCS not in my portfolio?", context2)
    print(f"Response: {response2}")
    print("-" * 80)
    
    # Test case 3: General portfolio query
    context3 = {
        "company": "",
        "prediction": 0,
        "features": {},
        "confidence": "Moderate Confidence",
        "portfolio_companies": ["MARICO", "DRREDDY", "HEROMOTOCO", "NESTLEIND", "ABBOTINDIA"]
    }
    
    print("🔍 Test 3: General portfolio query")
    response3 = generate_response("What companies are in my portfolio?", context3)
    print(f"Response: {response3}")

if __name__ == "__main__":
    test_prompt_service_direct()
