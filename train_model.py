import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# -----------------------------
# Generate Synthetic Training Data
# -----------------------------

np.random.seed(42)

data_size = 500

data = pd.DataFrame({
    "semantic_score": np.random.randint(30, 100, data_size),
    "skill_score": np.random.randint(20, 100, data_size),
    "action_score": np.random.randint(0, 25, data_size),
    "quant_score": np.random.randint(0, 20, data_size),
    "section_score": np.random.randint(0, 20, data_size),
})

# Hiring logic simulation
data["hired"] = (
    (0.4 * data["semantic_score"] +
     0.3 * data["skill_score"] +
     0.1 * data["action_score"] +
     0.1 * data["quant_score"] +
     0.1 * data["section_score"]) > 65
).astype(int)

# -----------------------------
# Train Model
# -----------------------------

X = data.drop("hired", axis=1)
y = data["hired"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Model Accuracy:", accuracy_score(y_test, predictions))

# Save model
joblib.dump(model, "hiring_model.pkl")

print("Model saved as hiring_model.pkl")