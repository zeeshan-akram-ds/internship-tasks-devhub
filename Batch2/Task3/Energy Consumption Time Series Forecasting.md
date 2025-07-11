# Energy Consumption Time Series Forecasting

## Project Overview

This project focuses on forecasting short-term household energy consumption using historical time-based patterns. Accurate energy forecasting is vital for effective energy management, optimizing resource allocation, and implementing demand-side response strategies. By analyzing historical data, this project aims to identify and leverage underlying patterns, seasonality, and trends to predict future energy demands.

## Objective

The primary objective of this project is to build, evaluate, and compare various time series forecasting models to predict household energy consumption. The project also aims to provide actionable insights into consumption patterns and identify the most effective model for this specific forecasting task.

## Dataset

The dataset utilized in this analysis is the **"Household Power Consumption Dataset"** sourced from the UCI Machine Learning Repository. This dataset comprises measurements of electric power consumption in a single household, recorded at a one-minute sampling rate over a period of nearly four years (December 2006 to November 2010). It includes various electrical quantities such as global active power, global reactive power, voltage, global intensity, and sub-metering values.

**Data Source:** [UCI Machine Learning Repository - Individual Household Electric Power Consumption](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption)

## Methodology

The forecasting process involves several key stages:

1.  **Data Acquisition and Loading:** The dataset is automatically fetched and loaded into a pandas DataFrame.
2.  **Data Cleaning and Preprocessing:**
    *   Handling of missing values through imputation.
    *   Conversion of date and time columns into a unified datetime format.
    *   Resampling of data to hourly and daily intervals for practical and computational efficiency.
3.  **Feature Engineering:** Extraction of time-based features from the datetime index, including hour of the day, day of the week, day of the year, month, quarter, year, week of year, and weekday/weekend flags. These features help capture cyclical patterns and temporal dependencies.
4.  **Exploratory Data Analysis (EDA):** In-depth visualization of energy consumption patterns to understand trends, seasonality (daily, weekly, monthly, yearly), and other significant characteristics that influence energy usage.
5.  **Model Building and Evaluation:** Three distinct time series forecasting models are built and compared:
    *   **ARIMA (AutoRegressive Integrated Moving Average):** A traditional statistical method for time series forecasting.
    *   **Facebook Prophet:** A robust forecasting tool optimized for business forecasts, capable of handling seasonality, holidays, and trends automatically.
    *   **XGBoost (eXtreme Gradient Boosting):** A powerful machine learning algorithm applied to time series data by incorporating lag features and engineered time-based features.
    The models are evaluated using standard metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE).
6.  **Visualization of Forecasts:** Plots comparing actual versus predicted values for each model are generated to visually assess performance and identify discrepancies.

## Key Findings and Conclusion

The analysis reveals strong daily, weekly, and yearly seasonal patterns in household energy consumption, emphasizing the importance of models capable of capturing these complex temporal dynamics. Both XGBoost and Facebook Prophet models generally demonstrate superior performance compared to the traditional ARIMA model, primarily due to their ability to handle non-linear relationships and complex seasonalities more effectively. XGBoost benefits from its robust handling of engineered features, while Prophet excels in its automated approach to seasonality and trend detection.

For practical applications, a hybrid modeling approach or ensemble methods could further enhance forecasting accuracy by combining the strengths of different techniques.

## How to Run the Notebook

To run this Jupyter Notebook and reproduce the analysis, follow these steps:

1.  **Clone the Repository (if applicable) or Download Files:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```
    (If you downloaded the files directly, navigate to the project directory.)

2.  **Install Dependencies:** Ensure you have Python 3.8+ installed. Install the required libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the Dataset:** The notebook is designed to automatically download the `household_power_consumption.txt` file. However, if there are issues, you can manually download it from:
    [https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip](https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip)
    Unzip the file and place `household_power_consumption.txt` in the same directory as the notebook.

4.  **Run Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```

5.  **Open and Execute:** Open `energy_forecasting.ipynb` in your browser and run all cells sequentially.

