from flask import Blueprint, request, jsonify
from services.prediction_service import get_company_prediction
from services.explanation_service import get_feature_contributions
from services.comparison_service import compare_companies
from services.nlp_utils import extract_companies
from services.confidence_service import get_confidence_level
from services.prompt_service import generate_response
from database.portfolio_service import get_user_portfolio

decision_chat_bp = Blueprint('decision_chat', __name__)


# 🔹 Normalize ticker
def normalize_ticker(t):
    return t.replace(".NS", "").upper().strip() if t else t


@decision_chat_bp.route('/decision-chat', methods=['POST'])
def decision_chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"response": "Invalid request"}), 400

        query = data.get("query", "").strip()
        user_id = data.get("user_id", "")

        print("QUERY:", query)
        print("USER_ID:", user_id)

    

        # 🔥 1. HANDLE PORTFOLIO FIRST (NO NLP NEEDED)
        if "portfolio" in query_lower:
            portfolio_companies = []

            if user_id:
                portfolio_companies = get_user_portfolio(user_id)

            portfolio_companies = [normalize_ticker(c) for c in portfolio_companies]

            if not portfolio_companies:
                return jsonify({
                    "response": "Your portfolio is empty. Add companies to get started."
                })

            return jsonify({
                "response": f"Your portfolio contains {len(portfolio_companies)} companies: {', '.join(portfolio_companies)}."
            })

        # 🔥 NLP extraction (NO DEFAULT FALLBACK)
        # 🔥 2. Only now extract companies
        c1, c2 = extract_companies(query, None)

        if not c1:
            return jsonify({
                "response": "Please mention a valid company (e.g., TCS, Infosys, Reliance)"
            }), 400

        # 🔹 Prediction
        try:
            prediction, features = get_company_prediction(company)
        except Exception as e:
            print("MODEL ERROR:", e)
            return jsonify({"response": "Model error occurred"}), 500

        print("PREDICTION:", prediction)

        # 🔹 Feature contributions
        try:
            feature_contrib = get_feature_contributions(features)
        except Exception as e:
            print("SHAP ERROR:", e)
            feature_contrib = {
                "ROE": 0.2,
                "Growth": 0.3,
                "Debt": -0.1
            }

        # 🔹 Confidence
        confidence = get_confidence_level(prediction)

        # 🔹 Context
        context = {
            "company": company,
            "company_name": company_name,
            "prediction": prediction,
            "features": feature_contrib,
            "confidence": confidence,
            "portfolio_companies": portfolio_companies
        }

        # 🔹 Optional portfolio data
        context["portfolio"] = data.get("context", {})

        # 🔥 Comparison
        if c2:
            try:
                comp_data = compare_companies(c1, c2)

                comp_data["company1_name"] = normalize_ticker(comp_data["company1"])
                comp_data["company2_name"] = normalize_ticker(comp_data["company2"])

                context["comparison"] = comp_data

            except Exception as e:
                print("COMPARISON ERROR:", e)

        print("CONTEXT:", context)

        # 🔥 Generate response
        response = generate_response(query, context)

        return jsonify({"response": response})

    except Exception as e:
        print("FATAL ERROR:", str(e))
        return jsonify({"response": "Server error occurred"}), 500