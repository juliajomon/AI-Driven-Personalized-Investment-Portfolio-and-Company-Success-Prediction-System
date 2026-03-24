from services.nlp_utils import extract_companies

# Test the NLP extraction directly
def test_nlp_extraction():
    
    test_queries = [
        "Why is MARICO in my portfolio?",
        "Why is MARICO.NS in my portfolio?", 
        "Why is TCS not in my portfolio?",
        "Why is TCS.NS not in my portfolio?",
        "Compare MARICO vs TCS",
        "What companies are in my portfolio?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        company1, company2 = extract_companies(query)
        print(f"Extracted: {company1}, {company2}")
        print("-" * 80)

if __name__ == "__main__":
    test_nlp_extraction()
