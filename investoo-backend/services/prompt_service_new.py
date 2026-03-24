def generate_response(query, context):
    query = query.lower()
    
    company = context.get("company", "")
    prediction = context.get("prediction", 0)
    features = context.get("features", {})
    confidence = context.get("confidence", "Moderate Confidence")
    comparison = context.get("comparison")
    portfolio = context.get("portfolio", {})
    portfolio_companies = context.get("portfolio_companies", [])

    # 🔹 Normalize company names
    def normalize(name):
        return name.replace(".NS", "").upper().strip()
    
    company_name = normalize(company)
    portfolio_companies = [normalize(c) for c in portfolio_companies]

    # 🔥 PORTFOLIO-BASED RESPONSES
    if "portfolio" in query:
        if not portfolio_companies:
            return (
                "You haven't saved any portfolio yet. Please add companies to your portfolio "
                "to get personalized insights about your investments."
            )
        
        return (
            f"Your portfolio includes {', '.join(portfolio_companies)}. "
            f"These companies were selected based on their success probabilities and "
            f"risk-return profiles to optimize your investment strategy."
        )

    # 🔥 WHY IN PORTFOLIO
    if "why" in query and company and company in portfolio_companies:
        if prediction > 0.8:
            return (
                f"{company_name} is in your portfolio because it shows strong potential "
                f"with a high success probability of {prediction} and {confidence}. "
                f"This makes it a valuable addition to your investment strategy."
            )
        elif prediction > 0.6:
            return (
                f"{company_name} is in your portfolio as a moderate-risk investment "
                f"with a success probability of {prediction} and {confidence}. "
                f"It provides balanced growth potential."
            )
        else:
            return (
                f"{company_name} is in your portfolio but shows lower success probability "
                f"of {prediction} with {confidence}. "
                f"Consider reviewing this position or diversifying further."
            )

    # 🔥 WHY NOT IN PORTFOLIO
    if "why not" in query and company and company not in portfolio_companies:
        if prediction > 0.8:
            return (
                f"{company_name} is not in your portfolio despite having strong potential "
                f"(success probability: {prediction}, {confidence}). "
                f"You might consider adding it for better returns, but ensure it aligns with your risk strategy."
            )
        elif prediction > 0.6:
            return (
                f"{company_name} is not in your portfolio. It shows moderate potential "
                f"(success probability: {prediction}, {confidence}) but your current portfolio "
                f"may already provide similar exposure with better diversification."
            )
        else:
            return (
                f"{company_name} is not in your portfolio, which is wise given its "
                f"low success probability of {prediction} and {confidence}. "
                f"Your current portfolio selection appears more prudent."
            )

    # 🔥 COMPARISON WITH PORTFOLIO CONTEXT
    if "compare" in query or "vs" in query:
        if comparison:
            better = normalize(comparison['better'])
            prob1 = comparison['prob1']
            prob2 = comparison['prob2']
            company1 = normalize(comparison.get('company1', comparison['company1']))
            company2 = normalize(comparison.get('company2', comparison['company2']))
            
            result = f"{better} ({prob1}) performs better than {company2} ({prob2})."
            
            # Add portfolio context
            if better in portfolio_companies:
                result += f" Since {better} is already in your portfolio, your current allocation is optimal."
            elif company2 in portfolio_companies:
                result += f" Consider rebalancing to include {better} for improved returns."
            else:
                result += f" Both companies are not in your current portfolio."
                
            return result

    # 🔥 GENERAL COMPANY ANALYSIS
    if company:
        if prediction > 0.8:
            return (
                f"{company_name} shows strong investment potential with high success probability "
                f"of {prediction} and {confidence}. "
                f"{'This is a strong buy candidate' if company not in portfolio_companies else 'This continues to be a solid portfolio holding'}."
            )
        elif prediction > 0.6:
            return (
                f"{company_name} shows moderate investment potential with success probability "
                f"of {prediction} and {confidence}. "
                f"{'Suitable for balanced portfolios' if company not in portfolio_companies else 'Continues to provide balanced growth'}."
            )
        else:
            return (
                f"{company_name} shows high-risk characteristics with low success probability "
                f"of {prediction} and {confidence}. "
                f"{'Only consider for high-risk tolerance' if company not in portfolio_companies else 'Monitor this position closely'}."
            )

    # 🔥 DEFAULT RESPONSE
    return (
        f"The company {company_name} has a success probability of {prediction} "
        f"with {confidence}. "
        f"{'This suggests strong investment potential' if prediction > 0.7 else 'This indicates moderate investment potential' if prediction > 0.4 else 'This suggests high investment risk'}."
    )
