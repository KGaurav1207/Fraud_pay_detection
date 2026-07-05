# 🛡️ FraudPayGuard – Indian SMS Fraud Detection System

A machine learning–based SMS fraud detection system designed to identify fraudulent and suspicious SMS messages commonly seen in the Indian digital payment ecosystem.

The project combines a TF-IDF based text classification model with handcrafted rule-based fraud signals to improve the detection of banking scams, phishing attempts, KYC fraud, UPI scams, and impersonation attacks.

**🔗 Live demo:** [fraudpaydetection-5t7zfq9mzb3tvg5klll5lu.streamlit.app](https://fraudpaydetection-5t7zfq9mzb3tvg5klll5lu.streamlit.app/)

---

## 📌 Features

- Detects SMS as **FRAUD**, **SUSPICIOUS**, or **SAFE**
- RandomForest classifier trained on TF-IDF text features + engineered numerical features
- Rule-based engine for India-specific fraud patterns
- Confidence score and detected-signal explanation for every prediction
- Deployed live as an interactive web app via Streamlit Community Cloud

---

## 🏗️ Project Pipeline

```
SMS Message
      │
      ▼
Text Preprocessing
      │
      ▼
Feature Extraction
(TF-IDF + Engineered Features)
      │
      ▼
Machine Learning Model (RandomForest)
      │
      ▼
Fraud Signal Extraction
(Rule Engine)
      │
      ▼
Decision Engine
      │
      ▼
SAFE / SUSPICIOUS / FRAUD
```

---

## 📊 Machine Learning Models

Three models were trained and compared using GridSearchCV (5-fold CV, optimized for F1):

| Model | Best Params | F1 Score |
|--------|----------|----------|
| Logistic Regression | `C=100` | 0.9969 |
| **Random Forest** ✅ | `n_estimators=100, max_depth=None` | **0.9990** |
| XGBoost | `n_estimators=300, max_depth=6, learning_rate=0.1` | 0.9918 |

**RandomForestClassifier** was selected as the final deployed model based on the highest validation F1 score.

---

## 🔍 Feature Engineering

### Text Features
- TF-IDF vectors — unigrams, bigrams, trigrams (max 8,000 features)

### Engineered Numerical Features
(in the exact order the model expects)
1. Message length
2. Digit count
3. Presence of a URL/link
4. Presence of money-related words (`rs`, `₹`, `lakh`, `crore`, etc.)
5. Presence of urgency-related words (`urgent`, `immediately`, `act now`, etc.)
6. Uppercase character count
7. Special character count

---

## 🛡️ Rule-Based Fraud Detection

Alongside the ML model, a rule engine detects India-specific fraud patterns including:

- OTP scams
- KYC fraud
- Bank account blocking scams
- Phishing links
- Prize and lottery scams
- RBI/TRAI impersonation
- Aadhaar and PAN fraud
- UPI payment scams
- Job and investment scams
- Urgency-based social engineering

The rule engine's signals combine with the ML prediction in a decision layer that can escalate a message to `FRAUD`/`SUSPICIOUS` or override it back down to `SAFE` (e.g. a legitimate OTP message that includes a "do not share this code" warning).

---

## 📈 Model Performance

Evaluated on a held-out test set (1,938 messages, stratified 80/20 split, upsampling applied only to the training set to avoid leakage).

| Metric | Score |
|---------|--------|
| Accuracy | 99.90% |
| Precision | 100.00% |
| Recall | 100.00% |
| F1 Score | 100.00% |
| ROC-AUC | 1.0000 |

**Edge-case / adversarial test suite** — 40 hand-crafted messages across 20 fraud categories (OTP scams, phishing, impersonation, obfuscated spam, legitimate transactional messages, etc.), evaluated through the full `analyze_message()` pipeline (ML model + rule engine):

| Metric | Score |
|---------|--------|
| Correct classifications | 39 / 40 |
| Accuracy | 97.5% |

> ⚠️ **Note:** The near-perfect held-out test scores are worth treating with some caution — they likely reflect that fraud/spam and legitimate messages are linguistically quite distinct in this dataset (especially the synthetic Indian fraud samples), rather than the model being flawless on real-world, unseen SMS traffic. The edge-case suite is a more realistic stress test, and its single miss (an impersonation message classified as FRAUD instead of the intended SUSPICIOUS) shows where the rule engine's thresholds could still be tuned.

---

## 📂 Project Structure

```
fraudpayguard/
│
├── FraudPayDetection.ipynb    # Model training & experimentation
├── fraud_model.pkl            # Trained RandomForest model
├── fraud_vectorizer.pkl       # Fitted TF-IDF vectorizer
│
├── Fraud_detection_app.py     # Streamlit UI (entry point)
├── model_loader.py            # Loads model + vectorizer
├── text_preprocessing.py      # Text cleaning / de-obfuscation
├── ml_prediction.py           # Builds feature vector, runs model
├── fraud_signals.py           # Rule-based signal keyword matching
├── fraud_analyzer.py          # Combines ML + rules into final decision
│
├── SMSSpamCollection          # UCI SMS Spam dataset (raw)
├── spam.csv                   # Kaggle spam dataset
├── final_dataset.csv          # Combined/cleaned training dataset
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

`requirements.txt` should include, at minimum:
```
pandas
numpy
scikit-learn
scipy
streamlit
joblib
```
(`joblib` is pulled in automatically as a scikit-learn dependency, but `streamlit` must be listed explicitly for local runs and for Streamlit Cloud to build correctly.)

---

## ▶️ Usage

### Run the Streamlit app locally
```bash
streamlit run Fraud_detection_app.py
```

### Run the notebook (training / experimentation)
```bash
jupyter notebook FraudPayDetection.ipynb
```

### Use the pipeline directly in Python
```python
from model_loader import load_model_and_vectorizer
from fraud_analyzer import analyze_message

model, vectorizer = load_model_and_vectorizer()

message = "Your SBI account has been blocked. Verify immediately."
result = analyze_message(message, model, vectorizer)
print(result)
```

Example output:
```
{
  "classification": "FRAUD",
  "confidence": 0.97,
  "signals": ["ACCOUNT_THREAT", "SUSPICIOUS_LINK", "PHISHING_ATTEMPT"],
  "explanation": "Detected ACCOUNT_THREAT, SUSPICIOUS_LINK, PHISHING_ATTEMPT — indicates potential fraud behavior."
}
```

---

## 🇮🇳 India-Specific Detection

The project recognizes fraud patterns commonly seen in India, including:

- UPI fraud (Google Pay, PhonePe, Paytm)
- Bank impersonation (SBI, HDFC, ICICI)
- RBI / TRAI impersonation
- Aadhaar and PAN scams
- KYC scams

---

## 🚀 Future Improvements

- FastAPI backend for programmatic access alongside the Streamlit UI
- Multilingual SMS support
- IndicBERT / mBERT integration for deeper language understanding
- Continuous model retraining pipeline
- Docker deployment

---

## 📚 Datasets

- SMS Spam Collection (UCI)
- Kaggle Spam Dataset
- Custom Indian fraud SMS samples

---

## 📝 License

This project was developed for educational purposes and portfolio demonstration.