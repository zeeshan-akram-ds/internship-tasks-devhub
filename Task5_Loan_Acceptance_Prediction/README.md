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

