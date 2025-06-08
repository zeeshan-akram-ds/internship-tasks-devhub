# Task 5: Personal Loan Acceptance Prediction

## Objective
Predict which customers are likely to accept a personal loan offer.

## Dataset
I used the **Medical Cost Personal Dataset** which is a widely used dataset in the community.  
**Rows, Columns:** (4521 rows, 17 columns)

### Key Features:
- **age:** Age of the customer
- **job:** Type of job (admin, technician, blue-collar, etc.)
- **marital:** Marital status (married, single, divorced)
- **education:** Education level
- **default:** Has credit in default? (yes/no)
- **housing:** Has housing loan? (yes/no)
- **loan:** Has personal loan? (yes/no)
- **contact:** Type of communication contact (cellular, telephone)
- **month:** Last contact month of year
- **day_of_week:** Last contact day of the week
- **duration:** Last contact duration (seconds)
- **campaign:** Number of contacts performed during this campaign
- **pdays:** Number of days since last contact
- **previous:** Number of contacts performed before this campaign
- **poutcome:** Outcome of previous marketing campaign
- **y:** Target variable → has the client subscribed to the term deposit? (yes/no) → Interpreted as **loan acceptance**.

## Data Preprocessing & Feature Engineering
- No missing values in this dataset.
- Applied **RobustScaler** to some numerical features to handle outliers.
- Applied **StandardScaler** to other features for balanced scaling.
- Encoded categorical variables appropriately.
- Addressed class imbalance through:
  - SMOTE  
  - SMOTE + Tomek Links  
  - SMOTEENN  
  - scale_pos_weight parameter in XGBoost
- Ultimately, **SMOTEENN + XGBoost** gave the best results.

## Modeling Approach
- Tried a total of **8 different models**.
- XGBoost (with SMOTEENN) was chosen due to the best overall performance.
- No stacking, voting, or additional ensemble models were used.
- Hyperparameter tuning was performed using **Optuna**:
  - Multiple parameters tuned including learning rate, max_depth, n_estimators, etc.
  - Plotted tuning history and results for interpretability.

## Evaluation
### Final Tuned Model - Classification Report:
          precision    recall  f1-score   support

       0       0.96      0.89      0.93       801
       1       0.47      0.75      0.58       104

accuracy                           0.88       905
macro avg       0.72      0.82      0.75       905
weighted avg    0.91      0.88      0.89       905

### Confusion Matrix:

[[714  87]
 [ 26  78]]

### Other Visualizations:
- **Feature Importance Plot**
- **ROC Curve**
- **Precision-Recall (PR) Curve**
- **Confusion Matrix**

Additionally, an **interactive Streamlit app** was created with:
- User-friendly manual inputs
- Probability-based predictions
- Visual explanations and insights

## Key Insights from EDA & Modeling
- **Previous Campaign Outcome:**  
  Customers with `poutcome = success` are strongly associated with higher acceptance rates. Targeting these customers can improve results significantly.
- **Month of Contact:**  
  Contacts made in **October** and **March** showed higher acceptance rates.
- **Contact Type:**  
  Customers contacted via **cellular** had much higher response rates.
- **Call Duration:**  
  Longer calls correlate with higher acceptance probability. Sales agents should focus on maintaining longer and quality interactions.
- **Housing and Loan Indicators:**  
  Customers **without housing loans** or **without personal loans** tend to have higher acceptance rates.
- **Education and Job:**  
  Certain job categories (**technician, blue-collar, management**) and **higher education** levels were associated with slightly higher acceptance rates.

## Deployment
The project was deployed successfully via **Streamlit Cloud**:

👉 [https://internship-tasks-devapp-4mrc94edtksynutbcdmija.streamlit.app/](https://internship-tasks-devapp-4mrc94edtksynutbcdmija.streamlit.app/)

## Summary
This project provided a comprehensive exercise in:
- Advanced preprocessing
- Feature engineering
- Model tuning and optimization
- Handling class imbalance
- Effective visual communication
- Deployment of a professional-grade ML application.

It was the most advanced and comprehensive project of this internship round, demonstrating my strong capabilities in delivering a real-world data science solution.

---

