import streamlit as st
import joblib
import pandas as pd
import numpy as np
from PIL import Image

# Load the trained model
model_pipeline = joblib.load('task3_churn_modeling.pkl')

# Streamlit App
st.set_page_config(page_title="Bank Customer Churn Prediction", layout="wide")

# Tabs
tabs = st.tabs(["Customer Churn Prediction", "Feature Guide"])

# ========== Tab 1: Prediction ==========
with tabs[0]:
    st.title("Bank Customer Churn Prediction")
    st.markdown("Predict whether a bank customer is likely to leave the bank.")

    # User Inputs
    st.header("Enter Customer Details")

    # Categorical Inputs
    geography = st.selectbox("Geography", options=['France', 'Germany', 'Spain'], help="Country where the customer resides.")
    gender = st.selectbox("Gender", options=['Male', 'Female'], help="Customer's gender.")

    # Numeric Inputs
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650, help="A creditworthiness score (higher is better).")
    age = st.number_input("Age", min_value=18, max_value=100, value=35, help="Customer's age.")
    tenure = st.number_input("Tenure (Years with Bank)", min_value=0, max_value=10, value=5, help="Number of years the customer has been with the bank.")
    balance = st.number_input("Balance", min_value=0.0, max_value=300000.0, value=50000.0, help="Account balance in USD.")
    estimated_salary = st.number_input("Estimated Salary", min_value=0.0, max_value=300000.0, value=70000.0, help="Estimated annual salary in USD.")

    # Passthrough Inputs
    num_of_products = st.selectbox("Number of Products", options=[1, 2, 3, 4], help="Number of bank products the customer holds.")
    has_crcard = st.selectbox("Has Credit Card", options=[0, 1], help="1 = Customer has a credit card; 0 = No credit card.")
    is_active_member = st.selectbox("Is Active Member", options=[0, 1], help="1 = Actively using bank services; 0 = Not active.")

    # Predict button
    if st.button("Predict Churn"):
        # Prepare data
        input_data = pd.DataFrame({
            'Geography': [geography],
            'Gender': [gender],
            'CreditScore': [credit_score],
            'Age': [age],
            'Tenure': [tenure],
            'Balance': [balance],
            'EstimatedSalary': [estimated_salary],
            'NumOfProducts': [num_of_products],
            'HasCrCard': [has_crcard],
            'IsActiveMember': [is_active_member]
        })

        # Predict probability and class
        prob = model_pipeline.predict_proba(input_data)[0][1]
        pred_class = model_pipeline.predict(input_data)[0]

        # Result
        st.subheader("Prediction Result:")
        if pred_class == 1:
            st.error(f"⚠️ The customer is LIKELY to CHURN. Probability: {prob:.2f}")
        else:
            st.success(f"The customer is NOT LIKELY to CHURN. Probability: {prob:.2f}")

# ========== Sidebar: Visualizations ==========
st.sidebar.title("Model Visualizations")
viz_choice = st.sidebar.selectbox("Select Visualization", 
    options=[
        "None",
        "SHAP Summary Plot",
        "Feature Importance",
        "Confusion Matrix",
        "ROC Curve"
    ])

if viz_choice != "None":
    st.sidebar.info(f"Displaying: {viz_choice}")

    image_map = {
        "SHAP Summary Plot": "shap_summary_plot_task3.png",
        "Feature Importance": "feature_imp_task3.png",
        "Confusion Matrix": "cm_task3.png",
        "ROC Curve": "roc_curve_task3.png"
    }

    try:
        image_path = image_map[viz_choice]
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"{viz_choice} image not found. Please add '{image_path}' to the directory.")
with st.expander("Classification Report"):
    st.markdown("""
    **Final Tuned Model - Classification Report:**

    ```
                  precision    recall  f1-score   support

               0       0.91      0.89      0.90      1593
               1       0.61      0.65      0.63       407

        accuracy                           0.84      2000
       macro avg       0.76      0.77      0.76      2000
    weighted avg       0.85      0.84      0.85      2000
    ```
    """)
# ========== Tab 2: Feature Guide ==========
with tabs[1]:
    st.title("Feature Guide")
    st.markdown("""
    **Feature Descriptions:**

    - **Geography**: Country where the customer lives (`France`, `Germany`, or `Spain`).
    - **Gender**: Customer's gender (`Male` or `Female`).
    - **CreditScore**: Customer's creditworthiness score (300 to 850).
    - **Age**: Customer's age in years.
    - **Tenure**: Number of years the customer has stayed with the bank.
    - **Balance**: Bank account balance.
    - **EstimatedSalary**: Estimated yearly salary of the customer.
    - **NumOfProducts**: Number of bank products the customer uses (1 to 4).
    - **HasCrCard**: Whether the customer holds a credit card (1 = Yes, 0 = No).
    - **IsActiveMember**: Whether the customer is actively using bank services (1 = Yes, 0 = No).
    - **Target (Exited)**: 1 = Customer left the bank (churned); 0 = Customer stayed.

    The model predicts whether the customer will **EXIT** the bank based on these features.
    """)
