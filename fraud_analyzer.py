"""
The final decision engine: combines the raw ML prediction with the
rule-based signals and a set of override rules to produce a
SAFE / SUSPICIOUS / FRAUD classification.
"""

from text_preprocessing import preprocess_text
from ml_prediction import predict_message
from fraud_signals import extract_signals, generate_explanation

OTP_SAFE_PHRASES = [
    "do not share", "don't share", "dont share",
    "never share", "do not disclose", "don't disclose",
    "never disclose", "not share", "do not reveal", "don't reveal"
]
OTP_TRIGGERS = ["otp", "verification code", "security code", "login code", "one-time password"]

TRANSACTIONAL_SAFE_PATTERNS = [
    "debited", "credited", "delivered", "shipment",
    "out for delivery", "order #", "txn id", "upi ref",
    "bill due", "emi due"
]

BILL_SAFE_PATTERNS = [
    "bill due", "bill of rs", "bill of ₹",
    "emi due", "emi of rs", "emi of ₹",
    "statement due", "minimum due", "payment due"
]

DANGEROUS_SIGNALS = {"SUSPICIOUS_LINK", "PRIZE_BAIT", "MONEY_SCAM", "URGENCY_PRESSURE"}

PRIZE_WORDS = [
    "winner", "lucky", "won", "prize", "reward", "lottery",
    "congratulations", "claim now", "call now to claim",
    "bumper prize", "jackpot", "spin and win", "gift card"
]


def analyze_message(text: str, model, vectorizer) -> dict:
    """
    Returns a dict:
        {"classification": "SAFE"|"SUSPICIOUS"|"FRAUD",
         "confidence": float,
         "signals": list[str],
         "explanation": str}
    """
    cleaned, _url, _money, _urgency = preprocess_text(text)
    pred, conf = predict_message(text, model, vectorizer)
    signals = extract_signals(cleaned)
    msg = text.lower()

    # --- SAFE OTP override ---
    if any(t in msg for t in OTP_TRIGGERS) and any(p in msg for p in OTP_SAFE_PHRASES):
        return {
            "classification": "SAFE",
            "confidence": round(conf, 3),
            "signals": [],
            "explanation": "Legitimate OTP message — contains privacy/safety warning."
        }

    # --- SAFE transactional override ---
    if any(p in msg for p in TRANSACTIONAL_SAFE_PATTERNS) and not signals:
        return {
            "classification": "SAFE",
            "confidence": round(conf, 3),
            "signals": signals,
            "explanation": "Legitimate transactional message."
        }

    # --- Bill / EMI safe override ---
    if (any(p in msg for p in BILL_SAFE_PATTERNS)
            and not any(s in signals for s in DANGEROUS_SIGNALS)):
        return {
            "classification": "SAFE",
            "confidence": round(conf, 3),
            "signals": [],
            "explanation": "Legitimate bill or EMI notification."
        }

    # --- Expand PRIZE_BAIT ---
    if any(w in msg for w in PRIZE_WORDS) and "PRIZE_BAIT" not in signals:
        signals.append("PRIZE_BAIT")

    has_link = "SUSPICIOUS_LINK" in signals
    has_prize = "PRIZE_BAIT" in signals
    has_phishing = "PHISHING_ATTEMPT" in signals
    has_account = "ACCOUNT_THREAT" in signals
    has_bank = "BANK_FRAUD" in signals
    has_cred = "CREDENTIAL_THEFT" in signals
    has_imperso = "IMPERSONATION" in signals
    has_money = "MONEY_SCAM" in signals
    has_urgency = "URGENCY_PRESSURE" in signals
    has_job = "JOB_INVESTMENT_SCAM" in signals
    has_otp = "OTP_SCAM" in signals

    # --- Combination rules (two signals together = always FRAUD) ---
    if has_link and has_prize:
        label, conf = "FRAUD", max(conf, 0.97)
    elif has_link and has_phishing:
        label, conf = "FRAUD", max(conf, 0.96)
    elif has_link and has_account:
        label, conf = "FRAUD", max(conf, 0.95)
    elif has_link and has_bank:
        label, conf = "FRAUD", max(conf, 0.95)
    elif has_link and has_cred:
        label, conf = "FRAUD", max(conf, 0.95)
    elif has_link and has_imperso:
        label, conf = "FRAUD", max(conf, 0.92)
    elif has_link and has_urgency:
        label, conf = "FRAUD", max(conf, 0.90)
    elif has_link and has_otp:
        label, conf = "FRAUD", max(conf, 0.90)
    elif has_phishing and has_urgency:
        label, conf = "FRAUD", max(conf, 0.88)
    elif has_account and has_urgency:
        label, conf = "FRAUD", max(conf, 0.88)
    elif has_imperso and has_urgency:
        label, conf = "FRAUD", max(conf, 0.88)
    elif has_bank and has_urgency:
        label, conf = "FRAUD", max(conf, 0.90)
    elif has_cred and has_urgency:
        label, conf = "FRAUD", max(conf, 0.90)

    # --- Single signal rules ---
    elif has_prize:
        label, conf = "FRAUD", max(conf, 0.80)
    elif has_money and pred == 1:
        label, conf = "FRAUD", max(conf, 0.90)
    elif has_job and pred == 1:
        label, conf = "FRAUD", max(conf, 0.88)
    elif has_bank or has_cred:
        label = "FRAUD" if pred == 1 else "SUSPICIOUS"
        conf = max(conf, 0.80)
    elif has_imperso:
        label, conf = "SUSPICIOUS", max(conf, 0.78)
    elif has_phishing or has_account:
        label = "SUSPICIOUS" if pred == 0 else "FRAUD"
        conf = max(conf, 0.75)
    elif has_money or has_job:
        label, conf = "SUSPICIOUS", max(conf, 0.75)
    elif has_urgency and pred == 1:
        label, conf = "FRAUD", max(conf, 0.80)
    elif has_urgency:
        label, conf = "SUSPICIOUS", max(conf, 0.65)
    elif has_otp:
        label, conf = "SUSPICIOUS", max(conf, 0.75)

    # --- ML model fallback ---
    else:
        if pred == 1:
            label = "FRAUD" if conf >= 0.75 else "SUSPICIOUS"
        else:
            label = "SAFE" if conf >= 0.60 else "SUSPICIOUS"

    return {
        "classification": label,
        "confidence": round(conf, 3),
        "signals": signals,
        "explanation": generate_explanation(label, signals)
    }