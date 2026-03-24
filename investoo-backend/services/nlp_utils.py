import re
from services.company_utils import company_map

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s&]', '', text)
    return text


def extract_companies(query):
    query = normalize(query)

    found = []

    # 1. Exact phrase match (highest priority)
    for name in company_map:
        if f" {name} " in f" {query} ":
            found.append(name)

    # 2. Token match (word-level)
    if not found:
        tokens = query.split()
        for token in tokens:
            if token in company_map:
                found.append(token)

    # 3. Alias / partial safe match (long names only)
    if not found:
        for name in company_map:
            if len(name) > 3 and name in query:
                found.append(name)

    # Remove duplicates
    found = list(dict.fromkeys(found))

    # Output handling
    if len(found) >= 2:
        return company_map[found[0]], company_map[found[1]]

    if len(found) == 1:
        return company_map[found[0]], None

    return default_company, None