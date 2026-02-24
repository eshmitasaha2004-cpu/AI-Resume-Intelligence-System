import joblib
import numpy as np

model = joblib.load("hiring_model.pkl")


def predict_hiring_probability(features_dict):

    feature_order = [
        "semantic_score",
        "skill_score",
        "action_score",
        "quant_score",
        "section_score",
    ]

    feature_values = np.array(
        [[features_dict[feature] for feature in feature_order]]
    )

    probability = model.predict_proba(feature_values)[0][1]

    return round(probability * 100, 2)