## Task 3: Bank Customer Churn Prediction

### Objective
**Identify bank customers who are likely to leave the bank** so that proactive retention strategies can be designed to improve customer loyalty.

---

### Dataset Overview
A popular **ChurnModeling** dataset widely used for customer churn prediction projects.

**Features included:**

- `RowNumber`  
- `CustomerId`  
- `Surname`  
- `CreditScore`  
- `Geography`  
- `Gender`  
- `Age`  
- `Tenure`  
- `Balance`  
- `NumOfProducts`  
- `HasCrCard`  
- `IsActiveMember`  
- `EstimatedSalary`  
- `Exited` (Target variable: 0 = No churn, 1 = Churn)

---

### Approach

- Performed detailed **Exploratory Data Analysis (EDA)** to understand feature distributions and relationships with churn.
- Dataset contained no missing values.
- Applied **RobustScaler** to prevent outlier influence on numeric features.
- Encoded categorical features (`Geography`, `Gender`).
- Applied **SMOTE** to handle class imbalance and improve recall on minority class (Churned customers).

---

### Modeling

- Trained and compared multiple models including base classifiers and ensemble methods.
- The final selected model: **Gradient Boosting Classifier**, tuned with **Optuna** to optimize performance.
- SMOTE + Gradient Boosting provided the best balance of precision, recall, and F1-score.

---

### Evaluation

- Evaluated with:
  - **Confusion Matrix**
  - **ROC Curve**
  - **Classification Report**
  - **SHAP Summary Plot** to analyze feature contributions and improve model interpretability.

---

### Key Insights from EDA

- **Churn rates** were significantly higher among customers in **Germany**, indicating a strong geographical influence.
- **Inactive members** and customers with **only one product** exhibited a much higher risk of churn — engagement and product diversity matter.
- **Age** and **Gender** had secondary effects on churn.
- Financial factors such as **Balance** and **EstimatedSalary** were less predictive — behavioral factors outweighed purely financial ones in predicting churn.

---

### Deployment

✅ Deployed on Streamlit Cloud:  
[Bank Customer Churn Prediction App](https://internship-tasks-devapp-kern5bvbnbpf7qscyzqdkd.streamlit.app/)

---

### Additional Notes

- A strong emphasis was placed on producing **interpretable and business-friendly visualizations**, helping decision-makers understand why customers churn.
- The app is **fully interactive** and allows users to input customer attributes and get real-time churn predictions.

---


