import joblib
import numpy as np

try:
    model = joblib.load("hiring_model.pkl")
except:
    model = None


def predict_hiring_probability(analysis):

    if model is None:
        return 0

    # Extract ONLY required features
    features = [
        analysis.get("semantic_score", 0),
        analysis.get("skill_score", 0),
        analysis.get("action_score", 0),
        analysis.get("quant_score", 0),
        analysis.get("section_score", 0),
    ]

    feature_array = np.array(features).reshape(1, -1)

    probability = model.predict_proba(feature_array)[0][1]

    return round(probability * 100, 2)