from services.prediction_service import get_company_prediction

def compare_companies(company1, company2):

    p1, f1 = get_company_prediction(company1)
    p2, f2 = get_company_prediction(company2)

    better = company1 if p1 > p2 else company2

    return {
        "company1": company1,
        "company2": company2,
        "prob1": p1,
        "prob2": p2,
        "better": better
    }