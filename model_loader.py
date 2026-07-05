"""
Loads the trained model and TF-IDF vectorizer from disk.
Kept separate so the loading path/logic can be changed in one place
(e.g. switching to joblib, S3, a different filename, etc.).
"""

import os
import joblib

# Resolve paths relative to this file's own directory, not the process's
# current working directory — this matters on Streamlit Cloud where the
# app may be launched from a different cwd than the script's folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fraud_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "fraud_vectorizer.pkl")


def load_model_and_vectorizer(model_path: str = MODEL_PATH,
                               vectorizer_path: str = VECTORIZER_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Make sure fraud_model.pkl is committed to your repo "
            "(check .gitignore and GitHub's 100MB file size limit)."
        )
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(
            f"Vectorizer file not found at {vectorizer_path}. "
            "Make sure fraud_vectorizer.pkl is committed to your repo "
            "(check .gitignore and GitHub's 100MB file size limit)."
        )
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer