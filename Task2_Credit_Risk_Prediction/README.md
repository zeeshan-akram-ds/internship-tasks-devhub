# Task 2: Credit Risk Prediction

## Objective
The objective of this project is to build a robust machine learning model that predicts whether a loan applicant is likely to default on a loan, enabling better risk management and informed lending decisions.

## Dataset
I'm using a public **Loan Risk Prediction** dataset, which contains both numerical and categorical information about loan applicants.

**Key Features:**
- **Age**
- **Gender**
- **Home**
- **Emp_length** (Employment length)
- **Intent** (Purpose of the loan)
- **Amount** (Loan amount)
- **Rate** (Interest rate)
- **Status**
- **Percent_income** (Loan amount as a % of income)
- **Cred_length** (Length of credit history)

**Target Variable:**  
`Default` (Yes / No)

## Approach

### Data Preprocessing
- **Outlier Handling:** Applied IQR-based method and Winsorization to mitigate the impact of extreme values.
- **Encoding & Scaling:** Categorical features were encoded appropriately; numerical features were scaled for optimal model performance.
- **Class Imbalance Handling:** Instead of applying SMOTE, used `scale_pos_weight` parameter of XGBoost to address the imbalance.

### Modeling
- Experimented with multiple models including **Logistic Regression**, **Random Forest**, and other ensemble methods.
- Selected **XGBoost Classifier** as the final model due to its superior performance.

### Hyperparameter Tuning
- Performed extensive tuning of XGBoost parameters using **Optuna** for automated optimization.

### Evaluation Metrics
- **Confusion Matrix**
- **ROC Curve**
- **Classification Report** (Precision, Recall, F1-score)
- Focused on both **accuracy** and **business interpretability** of the model.

## Results & Insights
- The model demonstrated strong predictive performance on unseen data.
- Visualizations such as **Feature Importance**, **Confusion Matrix**, and **ROC Curve** were used to explain model behavior.
- Performed comprehensive **Exploratory Data Analysis (EDA)** to uncover valuable patterns and relationships within the data.

## Deployment
The model is deployed as an interactive **Streamlit web app**, allowing users to input applicant data and receive real-time risk predictions.

**Live App:** [Credit Risk Prediction App](https://internship-tasks-devapp-g39hkbw3oyeo6myr6ggpfg.streamlit.app/)
