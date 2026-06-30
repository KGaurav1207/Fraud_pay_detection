# 🛡️ FraudPayGuard – Indian SMS Fraud Detection System

A machine learning–based SMS fraud detection system designed to identify fraudulent and suspicious SMS messages commonly seen in the Indian digital payment ecosystem.

The project combines a TF-IDF based text classification model with handcrafted rule-based fraud signals to improve the detection of banking scams, phishing attempts, KYC fraud, UPI scams, and impersonation attacks.

---

## 📌 Features

- Detects SMS as **FRAUD**, **SUSPICIOUS**, or **SAFE**
- Machine learning classifier trained on public spam datasets
- Rule-based engine for India-specific fraud patterns
- TF-IDF text vectorization with engineered numerical features
- Confidence score and explanation for every prediction
- Designed for easy deployment using FastAPI

---

# 🏗️ Project Pipeline

```
SMS Message
      │
      ▼
Text Preprocessing
      │
      ▼
Feature Extraction
(TF-IDF + Numerical Features)
      │
      ▼
Machine Learning Model
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

# 📊 Machine Learning Models

The following models were trained and compared:

| Model | Purpose |
|--------|----------|
| Logistic Regression | Baseline text classifier |
| Random Forest | Non-linear classification |
| XGBoost | Gradient boosting model |

The final model was selected based on validation performance.

---

# 🔍 Feature Engineering

### Text Features

- TF-IDF vectors
- Unigrams
- Bigrams
- Trigrams

### Numerical Features

- Message length
- Word count
- Digit count
- Uppercase character count
- Special character count
- Presence of URLs
- Presence of money-related words
- Presence of urgency-related words

---

# 🛡️ Rule-Based Fraud Detection

Along with the ML model, the project uses handcrafted rules to detect common fraud patterns including:

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

This hybrid approach improves interpretability and helps detect fraud patterns that may not be well represented in the training dataset.

---

# 📈 Model Performance

Evaluated on a held-out test set.

| Metric | Score |
|---------|--------|
| Accuracy | XX.XX% |
| Precision | XX.XX% |
| Recall | XX.XX% |
| F1 Score | XX.XX% |
| ROC-AUC | XX.XX |

*(Replace these values with your exact results.)*

---

# 📂 Project Structure

```
fraudpayguard/
│
├── fraud_pay_fixed.ipynb
├── fraud_model.pkl
├── fraud_vectorizer.pkl
├── final.pkl
├── SMSSpamCollection
├── spam.csv
├── README.md
```

---

# ⚙️ Installation

```bash
pip install pandas numpy scikit-learn xgboost matplotlib scipy
```

---

# ▶️ Usage

Run the notebook:

```bash
jupyter notebook fraud_pay_fixed.ipynb
```

Example prediction:

```python
message = "Your SBI account has been blocked. Verify immediately."

result = analyze_message(message)

print(result)
```

Output

```
Classification : FRAUD

Confidence : 97%

Detected Signals

✓ Account Threat

✓ Suspicious Link

✓ Phishing Attempt
```

---

# 🇮🇳 India-Specific Detection

The project is designed to recognize fraud patterns commonly seen in India, including:

- UPI fraud
- Google Pay
- PhonePe
- Paytm
- SBI
- HDFC
- ICICI
- RBI impersonation
- TRAI scams
- Aadhaar fraud
- PAN scams
- KYC scams

---

# 🚀 Future Improvements

- FastAPI deployment
- Streamlit web interface
- Multilingual SMS support
- IndicBERT / mBERT integration
- Continuous model retraining
- Docker deployment

---

# 📚 Datasets

- SMS Spam Collection (UCI)
- Kaggle Spam Dataset
- Custom Indian fraud SMS samples

---

# 📝 License

This project was developed for educational purposes and portfolio demonstration.