"""
Text cleaning used before TF-IDF vectorization.
MUST stay identical to the preprocessing used in the training notebook —
any change here will make the vectorizer see different tokens than the
model was trained on.
"""

import re


def preprocess_text(text: str):
    """
    Lowercases and de-obfuscates common spam tricks, then flags a few
    keyword-based signals used as engineered features.

    Returns:
        cleaned_text (str), has_url (int), has_money (int), has_urgency (int)
    """
    msg = str(text).lower()

    # Normalize common obfuscations used in spam
    msg = msg.replace("@", "a")   # fr@ud   → fraud
    msg = msg.replace("0", "o")   # 0tp     → otp
    msg = msg.replace("1", "i")   # 1ncome  → income
    msg = msg.replace("$", "s")   # ca$h    → cash
    msg = msg.replace("3", "e")   # fr3e    → free

    # Remove extra whitespace
    msg = re.sub(r"\s+", " ", msg).strip()

    has_url = 1 if ("http" in msg or "www" in msg or "bit.ly" in msg
                    or "tinyurl" in msg) else 0
    has_money = 1 if any(c in msg for c in ["rs", "₹", "£", "$", "inr",
                                             "lakh", "crore"]) else 0
    has_urgency = 1 if any(w in msg for w in ["urgent", "immediately", "hurry",
                                               "asap", "expire", "act now",
                                               "last chance"]) else 0
    return msg, has_url, has_money, has_urgency