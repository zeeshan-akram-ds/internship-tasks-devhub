from pathlib import Path

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "Task2_xgb_credit_risk_prediction.pkl"
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image

# Load the trained pipeline
pipeline = joblib.load('Task2_xgb_credit_risk_prediction.pkl')

# Set page configuration
st.set_page_config(page_title="Loan Risk Prediction", layout="wide")

# Sidebar to enable/disable visualizations
st.sidebar.header("Visualization Options")
show_viz = st.sidebar.checkbox("Show Model Visualizations", value=False)

# If user enables visualization section
if show_viz:
    st.header("Model Visualizations")
    
    viz_option = st.radio("Select Visualization:", ("ROC Curve", "Confusion Matrix"))

    if viz_option == "ROC Curve":
        try:
            roc_image = Image.open("roc_curve_task2.png")
            st.image(roc_image, use_container_width=True, caption="ROC Curve - Tuned XGBoost")
        except FileNotFoundError:
            st.warning("ROC Curve image not found. Please add 'roc_curve.png' to the directory.")

    elif viz_option == "Confusion Matrix":
        try:
            cm_image = Image.open("confusion_matrix_task2.png")
            st.image(cm_image, use_container_width=True, caption="Confusion Matrix - Tuned XGBoost")
        except FileNotFoundError:
            st.warning("Confusion Matrix image not found. Please add 'confusion_matrix.png' to the directory.")
# Main title
st.title("Loan Risk Prediction App")
st.markdown("Predict whether a loan applicant is likely to default based on their financial and personal information.")

# Input fields with tooltips
st.header("Applicant Information")

age = st.number_input(
    label="Age",
    min_value=18,
    max_value=100,
    value=30,
    help="Applicant's age in years."
)

income = st.number_input(
    label="Annual Income ($)",
    min_value=1000,
    max_value=1000000,
    value=50000,
    step=1000,
    help="Total annual income of the applicant."
)

home = st.selectbox(
    label="Home Ownership",
    options=['OWN', 'RENT', 'MORTGAGE', 'OTHER'],
    help="Type of home ownership."
)

emp_length = st.number_input(
    label="Employment Length (years)",
    min_value=0,
    max_value=50,
    value=5,
    help="Number of years the applicant has been employed."
)

intent = st.selectbox(
    label="Loan Purpose",
    options=['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'],
    help="Purpose of the loan."
)

amount = st.number_input(
    label="Loan Amount ($)",
    min_value=500,
    max_value=50000,
    value=10000,
    step=500,
    help="Total loan amount requested."
)

rate = st.number_input(
    label="Interest Rate (%)",
    min_value=1.0,
    max_value=40.0,
    value=12.5,
    step=0.1,
    help="Interest rate applicable to the loan."
)

status = st.selectbox(
    label="Current Loan Status",
    options=[0, 1],
    help="0: No late payment, 1: Late payment or delinquent."
)

percent_income = st.number_input(
    label="Percent of Income (%)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=0.1,
    help="Percentage of income that goes towards loan repayment."
)

cred_length = st.number_input(
    label="Credit History Length (years)",
    min_value=1,
    max_value=50,
    value=10,
    help="Number of years since the applicant's first credit line."
)

# Prepare input data
input_data = pd.DataFrame({
    'Age': [age],
    'Income': [income],
    'Home': [home],
    'Emp_length': [emp_length],
    'Intent': [intent],
    'Amount': [amount],
    'Rate': [rate],
    'Status': [status],
    'Percent_income': [percent_income],
    'Cred_length': [cred_length]
})

# Prediction
if st.button("Predict Loan Default Risk"):
    prediction = pipeline.predict(input_data)
    prediction_proba = pipeline.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result:")
    if prediction[0] == 1:
        st.error(f"High risk of default! Probability: {prediction_proba:.2f}")
    else:
        st.success(f"Low risk of default. Probability: {prediction_proba:.2f}")

# Classification Report
with st.expander("Classification Report"):
    st.markdown("""
    ```
                  precision    recall  f1-score   support

           0       0.99      0.79      0.88      1216
           1       0.49      0.95      0.64       261

    accuracy                           0.82      1477
   macro avg       0.74      0.87      0.76      1477
weighted avg       0.90      0.82      0.83      1477
    ```
    """)
