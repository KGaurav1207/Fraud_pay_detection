import streamlit as st

from model_loader import load_model_and_vectorizer
from fraud_analyzer import analyze_message


# Page configuration
st.set_page_config(
    page_title="Fraud Detection App",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def get_model_and_vectorizer():
    return load_model_and_vectorizer()

model, vectorizer = get_model_and_vectorizer()


# UI
st.title("🛡️ Fraud Detection App - SMS Fraud Detection")

user_input = st.text_area("Enter the SMS message to check for fraud:", height=150)
predict_button = st.button("Check the message")

if predict_button:
    if user_input.strip() == "":
        st.warning("Please enter a message to check for fraud.")
    else:
        result = analyze_message(user_input, model, vectorizer)
        label = result["classification"]
        confidence_pct = result["confidence"] * 100

        if label == "FRAUD":
            st.error(f"⚠️ Likely Fraudulent Message! (FRAUD)\nConfidence: {confidence_pct:.2f}%")
        elif label == "SUSPICIOUS":
            st.warning(f"🟡 Suspicious Message — needs caution.\nConfidence: {confidence_pct:.2f}%")
        else:
            st.success(f"✅ Likely Legitimate Message! (SAFE)\nConfidence: {confidence_pct:.2f}%")

        if result["signals"]:
            st.write(f"**Detected signals:** {', '.join(result['signals'])}")
        st.caption(result["explanation"])