"""
India-specific rule-based fraud signal detection, used alongside the ML
model to catch patterns (OTP scams, KYC fraud, impersonation, etc.) that
may be under-represented in the training data.
"""

SIGNAL_KEYWORDS = {
    "OTP_SCAM": ["otp"],
    "ACCOUNT_THREAT": [
        "account blocked", "account suspended", "account deactivated",
        "account on hold", "account will be closed", "account disabled",
        "account frozen", "account terminated"
    ],
    "PHISHING_ATTEMPT": [
        "verify", "verification", "confirm your", "update your",
        "validate", "reactivate", "re-verify", "re-confirm",
        "complete your kyc", "kyc pending", "kyc expired",
        "submit your details", "enter your details"
    ],
    "SUSPICIOUS_LINK": [
        "http", "www", "bit.ly", "tinyurl", "t.co",
        "shorturl", "ow.ly", "rb.gy", "cutt.ly", "tiny.cc"
    ],
    "PRIZE_BAIT": [
        "won", "winner", "prize", "lottery", "lucky draw",
        "you have been selected for prize", "selected as winner",
        "chosen as winner", "chosen for reward",
        "reward", "gift card", "voucher",
        "cashback offer", "special offer", "exclusive offer",
        "bumper prize", "jackpot", "spin and win",
        "congratulations", "claim your prize", "claim now",
        "call now to claim", "collect your reward"
    ],
    "BANK_FRAUD": [
        "card number", "cvv", "expiry date", "card details",
        "net banking", "internet banking", "bank login",
        "bank account number", "ifsc", "debit card", "credit card",
        "atm pin", "pin number", "card pin", "upi pin",
        "upi id", "google pay", "phonepe", "paytm"
    ],
    "CREDENTIAL_THEFT": [
        "password", "username", "login", "sign in", "user id",
        "aadhar", "aadhaar", "pan card", "pan number",
        "date of birth", "dob", "mother's maiden", "security question"
    ],
    "IMPERSONATION": [
        "rbi", "reserve bank", "sebi", "income tax", "it department",
        "irdai", "trai", "government of india", "ministry",
        "police", "cyber crime", "court notice", "legal notice",
        "uidai", "npci", "sbi", "hdfc", "icici", "axis bank",
        "amazon", "flipkart", "swiggy", "zomato", "irctc",
        "airtel", "jio", "bsnl", "vodafone"
    ],
    "MONEY_SCAM": [
        "transfer now", "send money", "transfer money", "wire transfer",
        "pay now", "payment pending", "pay immediately",
        "deposit now", "fund your wallet", "recharge now",
        "processing fee", "registration fee", "advance fee",
        "tax fee", "customs fee", "release fee", "handling fee"
    ],
    "JOB_INVESTMENT_SCAM": [
        "work from home", "earn daily", "earn weekly",
        "part time job", "data entry job", "typing job",
        "investment opportunity", "high returns", "guaranteed returns",
        "double your money", "triple your money", "profit guaranteed",
        "no risk investment", "crypto investment", "trading profit",
        "refer and earn", "mlm", "network marketing"
    ],
    "URGENCY_PRESSURE": [
        "urgent", "immediately", "right now", "hurry",
        "last chance", "final notice", "expire today",
        "expires in", "limited time", "act now", "do it now",
        "within 24 hours", "within 2 hours", "before midnight",
        "today only", "don't delay", "asap"
    ],
}


def extract_signals(text: str):
    """Returns a list of matched signal names (order preserved)."""
    msg = text.lower()
    signals = []
    for signal_name, keywords in SIGNAL_KEYWORDS.items():
        if any(keyword in msg for keyword in keywords):
            signals.append(signal_name)
    return signals


def generate_explanation(label: str, signals: list):
    if signals:
        return f"Detected {', '.join(signals)} — indicates potential {label.lower()} behavior."
    return "No strong fraud indicators detected by rule engine; classified by ML model."