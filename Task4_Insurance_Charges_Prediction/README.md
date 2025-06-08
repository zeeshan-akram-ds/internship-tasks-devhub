# Task 4: Predicting Insurance Claim Amounts

## Objective
Estimate the medical insurance claim amount based on personal data.
This task was conducted as part of the DevelopersHub Corporation - Data Science & Analytics Internship.

## Dataset Overview
- Dataset: Widely used public dataset - Medical Cost Personal Dataset
- Features:
  - age
  - sex
  - bmi
  - children
  - smoker
  - region
  - charges (Target)

## Approach

### 1. Exploratory Data Analysis (EDA)
- Verified there were no missing values.
- Performed detailed EDA with distribution plots and boxplots.
- Identified right-skewed distribution of charges.

### 2. Preprocessing
- Applied RobustScaler to scale numeric features and handle outliers.
- Encoded categorical variables appropriately.
- Conducted feature engineering trials (PolynomialFeatures tested but final model used base features).

### 3. Modeling
- Tried:
  - Linear Regression
  - Ridge Regression
  - Polynomial Features with Linear Models
- After comparison and tuning, Linear Regression performed best and was selected as the final model.

### 4. Model Tuning
- Performed tuning and cross-validation to compare models and scalers.

## Evaluation

### Metrics Used:
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

### Interpretability:
- SHAP Summary Plot revealed:
  - Smoking status was the most influential factor.
  - Age and BMI had strong impacts on charges.
  - Number of children, region, and sex showed smaller effects.

### Visualizations:
- Actual vs. Predicted plot
- Residuals plot
- SHAP Summary Plot

## Key Insights from EDA

- Insurance charges exhibit a right-skewed distribution.
- Smokers pay significantly higher insurance charges — often 3–4 times more than non-smokers.
- Age is positively correlated with charges.
- BMI also increases charges, especially at high BMI levels.
- Region, sex, and number of children have smaller but notable effects.

## Deployment

The model was deployed via Streamlit:
https://insurance-charges-model-hnnjayxdtcuqhpke6tl6hb.streamlit.app/

## Summary

This task demonstrates a full workflow for predicting insurance claim amounts, including:
- Exploratory Data Analysis
- Preprocessing & Feature Engineering
- Model Training & Tuning
- Evaluation & Interpretability
- Deployment via Streamlit
