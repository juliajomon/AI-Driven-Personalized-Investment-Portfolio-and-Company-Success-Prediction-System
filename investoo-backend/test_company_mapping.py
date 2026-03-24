from services.company_utils import company_map

# Test company mapping
test_companies = ["marico", "tcs", "drreddy", "heromotoco", "nestleind", "abbottindia"]

print("🔍 Testing company mapping:")
for company in test_companies:
    if company in company_map:
        print(f"{company} -> {company_map[company]}")
    else:
        print(f"{company} -> NOT FOUND")

print(f"\n🔍 Total companies in map: {len(company_map)}")
print(f"🔍 First 10 companies: {list(company_map.items())[:10]}")
