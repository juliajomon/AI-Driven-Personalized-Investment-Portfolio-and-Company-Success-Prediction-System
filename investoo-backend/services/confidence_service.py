def get_confidence_level(prob):

    if prob > 0.8:
        return "High Confidence"
    elif prob > 0.6:
        return "Moderate Confidence"
    else:
        return "Low Confidence"