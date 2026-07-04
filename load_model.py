"""
Loads the trained model and TF-IDF vectorizer from disk.
Kept separate so the loading path/logic can be changed in one place
(e.g. switching to joblib, S3, a different filename, etc.).
"""

import joblib

MODEL_PATH = "fraud_model.pkl"
VECTORIZER_PATH = "fraud_vectorizer.pkl"


def load_model_and_vectorizer(model_path: str = MODEL_PATH,
                               vectorizer_path: str = VECTORIZER_PATH):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer