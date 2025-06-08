from pathlib import Path

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "task5_loan_acceptance_pred.pkl"
roc_path = BASE_DIR / "roc_curve_task5.png"
cm_path = BASE_DIR / "cm_task5.png"
fi_path = BASE_DIR / "feature_importance_task5.png"
pr_path = BASE_DIR / "pr_curve_task5.png"
import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Load the trained pipeline
model_pipeline = joblib.load(MODEL_PATH)

# Sidebar About section (Always visible)
with st.sidebar:
    st.title("About This App")
    st.write("""
    This app predicts whether a bank customer is likely to **accept a loan offer** based on their profile.
    
    **Model:** Tuned XGBoost Classifier  
    **Dataset:** Public Bank Marketing Dataset (Kaggle)  
    **Developer:** Zeeshan Akram  
    
    **GitHub:** [github.com/zeeshan-akram-ds](https://github.com/zeeshan-akram-ds)
    """)

# App layout - Tabs
tab1, tab2, tab3 = st.tabs(["Prediction App", "Visualizations", "Feature Guide"])

# ---- TAB 1: Prediction App ----
with tab1:
    st.title("Bank Marketing - Loan Offer Acceptance Prediction")
    st.write("""
    This app predicts whether a customer is likely to accept a loan offer based on their profile.
    The model was trained on the **Bank Marketing Dataset**.
    """)

    st.header("Enter Customer Information")

    # Numeric skewed features
    balance = st.number_input("Account Balance (€)", value=0,
                              help="Current balance in the customer's bank account.")
    duration = st.number_input("Call Duration (sec)", value=0,
                               help="Duration of the last marketing call in seconds.")
    campaign = st.number_input("Number of Contacts During Campaign", value=0,
                               help="Number of times the customer was contacted during this campaign.")
    pdays = st.number_input("Days Since Last Contact (-1 means never contacted)", value=-1,
                            help="Number of days passed since the customer was last contacted. -1 means never contacted.")
    previous = st.number_input("Number of Previous Contacts", value=0,
                               help="Number of contacts performed before this campaign.")

    # Numeric normal features
    age = st.number_input("Customer Age", value=30,
                          help="Age of the customer.")
    day = st.number_input("Day of Month Contacted", value=15,
                          help="Day of the month when the customer was contacted.")

    # Categorical nominal features
    job = st.selectbox("Job", ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management',
                               'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed'],
                       help="Type of job the customer has.")

    marital = st.selectbox("Marital Status", ['married', 'single', 'divorced'],
                           help="Marital status of the customer.")

    education = st.selectbox("Education Level", ['primary', 'secondary', 'tertiary', 'unknown'],
                             help="Education level of the customer.")

    contact = st.selectbox("Contact Communication Type", ['cellular', 'telephone', 'unknown'],
                           help="Communication type used to contact the customer.")

    month = st.selectbox("Month of Last Contact", ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
                         help="Last contact month of year.")

    poutcome = st.selectbox("Outcome of Previous Marketing Campaign", ['failure', 'unknown', 'success', 'other'],
                            help="Outcome of the previous marketing campaign.")

    # Binary features
    default = st.selectbox("Credit in Default?", ['no', 'yes'],
                           help="Whether the customer has credit in default.")
    housing = st.selectbox("Housing Loan?", ['no', 'yes'],
                           help="Whether the customer has a housing loan.")
    loan = st.selectbox("Personal Loan?", ['no', 'yes'],
                        help="Whether the customer has a personal loan.")

    # Prepare input DataFrame
    input_data = pd.DataFrame({
        'balance': [balance],
        'duration': [duration],
        'campaign': [campaign],
        'pdays': [pdays],
        'previous': [previous],
        'age': [age],
        'day': [day],
        'job': [job],
        'marital': [marital],
        'education': [education],
        'contact': [contact],
        'month': [month],
        'poutcome': [poutcome],
        'default': [default],
        'housing': [housing],
        'loan': [loan]
    })
    for col in ['default', 'housing', 'loan']:
        input_data[col] = input_data[col].map({'no': 0, 'yes': 1})

    # Predict button
    if st.button("Predict Offer Acceptance"):
        prediction = model_pipeline.predict(input_data)[0]
        prob = model_pipeline.predict_proba(input_data)[0][1]  # probability of class 1

        if prediction == 1:
            st.success(f"The customer is LIKELY to ACCEPT the loan offer. Probability: {prob:.2f}")
        else:
            st.warning(f"The customer is NOT LIKELY to ACCEPT the loan offer. Probability: {prob:.2f}")

    # Classification report in expander
    with st.expander("Classification Report"):
        st.markdown("""
        **Final Tuned Model - Classification Report:**

        | Class | Precision | Recall | F1-score | Support |
        |-------|-----------|--------|----------|---------|
        | 0     | 0.97      | 0.88   | 0.92     | 801     |
        | 1     | 0.45      | 0.80   | 0.58     | 104     |

        **Accuracy:** 0.87  
        **Macro Avg:** Precision 0.71, Recall 0.84, F1-score 0.75  
        **Weighted Avg:** Precision 0.91, Recall 0.87, F1-score 0.88  
        """)

# ---- TAB 2: Visualizations ----
with tab2:
    st.header("Model Visualizations")

    viz_option = st.selectbox("Select Visualization:", 
                              ("", "Feature Importance", "Confusion Matrix", "ROC Curve", "Precision-Recall Curve"))

    if viz_option == "Feature Importance":
        try:
            img = Image.open(fi_path)
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.warning("Feature Importance image not found. Please add 'feature_importance_task5.png' to the directory.")

    elif viz_option == "Confusion Matrix":
        try:
            img = Image.open(cm_path)
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.warning("Confusion Matrix image not found. Please add 'cm_task5.png' to the directory.")

    elif viz_option == "ROC Curve":
        try:
            img = Image.open(roc_path)
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.warning("ROC Curve image not found. Please add 'roc_curve_task5.png' to the directory.")

    elif viz_option == "Precision-Recall Curve":
        try:
            img = Image.open(pr_path)
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.warning("Precision-Recall Curve image not found. Please add 'pr_curve_task5.png' to the directory.")

# ---- TAB 3: Feature Guide ----
with tab3:
    st.header("Feature Guide - Bank Marketing Dataset")

    st.markdown("""
    - **balance:** Current balance in customer's bank account (€).
    - **duration:** Duration of the last marketing call in seconds.
    - **campaign:** Number of times the customer was contacted during this campaign.
    - **pdays:** Number of days since last contact (-1 means never contacted).
    - **previous:** Number of contacts performed before this campaign.
    - **age:** Customer's age.
    - **day:** Day of the month when the customer was contacted.
    - **job:** Customer's job type (admin., technician, services, etc.).
    - **marital:** Marital status of the customer.
    - **education:** Customer's education level.
    - **contact:** Communication type used (cellular, telephone, unknown).
    - **month:** Month of the year when the customer was last contacted.
    - **poutcome:** Outcome of the previous marketing campaign.
    - **default:** Whether the customer has credit in default.
    - **housing:** Whether the customer has a housing loan.
    - **loan:** Whether the customer has a personal loan.
    """)
