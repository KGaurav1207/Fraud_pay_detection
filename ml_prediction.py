"""
Builds the exact 8007-feature input (8000 TF-IDF + 7 engineered features)
the model was trained on, and returns its raw prediction.

Engineered feature order MUST match training:
["length", "num_digits", "has_link", "has_money", "has_urgency",
 "num_caps", "num_special"]
"""

import re
import numpy as np
from scipy.sparse import hstack

from text_preprocessing import preprocess_text


def predict_message(text: str, model, vectorizer):
    """
    Returns:
        pred (0 or 1), conf (float, the winning class's probability)
    """
    cleaned, has_url, has_money, has_urgency = preprocess_text(text)

    tfidf_vec = vectorizer.transform([cleaned])

    length = len(text)
    num_digits = sum(c.isdigit() for c in text)
    num_caps = sum(1 for c in text if c.isupper())
    num_special = len(re.findall(r"[!?@#%]", text))

    engineered = np.array([[
        length,
        num_digits,
        has_url,
        has_money,
        has_urgency,
        num_caps,
        num_special
    ]])

    final_input = hstack([tfidf_vec, engineered])

    pred = model.predict(final_input)[0]
    proba = model.predict_proba(final_input)[0]
    conf = proba.max()
    return pred, conf