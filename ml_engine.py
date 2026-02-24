import numpy as np
import joblib
import os

MODEL_PATH = "hiring_model.pkl"

# Load model safely
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None


def predict_hiring_probability(analysis):
    try:
        if model is None:
            return 0.0

        # Ensure consistent feature order
        feature_array = np.array([
            analysis.get("match_score", 0),
            analysis.get("skill_match_percentage", 0),
            analysis.get("experience_match", 0),
            analysis.get("education_match", 0)
        ]).reshape(1, -1)

        # Check expected feature count
        if feature_array.shape[1] != model.n_features_in_:
            return 0.0

        probability = model.predict_proba(feature_array)[0][1]
        return round(float(probability), 2)

    except Exception:
        return 0.0