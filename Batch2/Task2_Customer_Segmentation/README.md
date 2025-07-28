
# Task 2 – Customer Segmentation Using Unsupervised Learning

> Built by **Zeeshan Akram** — Data Analyst | BI Enthusiast | Machine Learning Developer  
> This project combines business strategy with machine learning to unlock valuable customer insights from mall data.

---

## Project Overview

This project clusters mall customers using their **Age**, **Annual Income**, and **Spending Score** using **K-Means clustering**. The goal is to identify **actionable customer segments** for more effective marketing and business strategy.

 **Business Objective:**  
Segment customers into meaningful groups so that the mall can:
- Target each group with personalized marketing
- Improve sales and customer satisfaction
- Allocate budgets more efficiently

---

## Why This Project Matters (For Stakeholders)

This project is built to reflect **real-world business needs**, not just algorithm output.

 It answers:
- Who are our highest spenders?
- Are young shoppers more loyal?
- Which customer group is underperforming in spending?
- How can we personalize promotions?

📄 The project includes a **PDF report generator** for easy sharing with managers, clients, or decision-makers — ideal for boardrooms or client handovers.

---

## Key Features

- ✅ Clean and structured **Exploratory Data Analysis**
- ✅ Intelligent clustering using **K-Means**
- ✅ **t-SNE** dimensionality reduction for clear cluster separation
- ✅ Business-friendly **segment naming** (e.g., "Premium Spenders", "Cautious Elites")
- ✅ **PDF report generation** per segment or for all segments
- ✅ **Interactive Streamlit App** with filtering, strategy tips, and visual exploration

---

## Dataset Used

- Dataset: `Mall_Customers.csv`  
- Shape: `200 rows × 5 columns`
- Features:
  - `CustomerID`
  - `Gender`
  - `Age`
  - `Annual Income (k$)`
  - `Spending Score (1–100)`

---

## Machine Learning Workflow

| Step | Description |
|------|-------------|
| **1. Preprocessing** | One-hot encoding for gender, scaling of numeric features, dropping ID |
| **2. Clustering**   | K-Means with optimal `k=5` via Elbow Method |
| **3. Segment Profiling** | Each cluster named & profiled with business logic |
| **4. Dimensionality Reduction** | t-SNE used to project customer groups into 2D |
| **5. Insights & Strategy** | Clear, non-technical marketing takeaways |
| **6. PDF Reporting** | Segment reports downloadable with stats & strategy |

---

## File Structure

 Task2_Customer_Segmentation/

├── app.py                     ← Streamlit app

├── pdf_generator.py          ← PDF creation module

├── mall_customers_original.csv   ← Original dataset with clusters/segments

├── mall_customers_scaled.csv     ← Scaled version for ML

├── requirements.txt          ← Dependencies for deployment

├── README.md                 ← This file

└── /images                   ← Screenshots or t-SNE plots


---

## Customer Segments Defined

| Segment Name         | Description |
|----------------------|-------------|
| Premium Spenders     | Young, high-income, high-spending customers |
| Budget Enthusiasts   | Low-income but high-spending youth |
| Mature Moderates     | Older customers with moderate income & spending |
| Cautious Elites      | High-income customers who spend very little |
| Young Averages       | Average age and behavior, large middle group |

These segments are not arbitrary — they are carefully named to reflect real-world marketing personas.

---

## Streamlit App Highlights

-  Sidebar segment selection
-  Dynamic t-SNE and scatter plots
-  PDF download button (based on selected filter)
-  Segment-level statistics shown live
-  Marketing tips and insight block for each cluster

 Use the app to explore segments, then generate a **sharable report** for management.

**Live App**: [Customer Segmentation Dashboard](https://internship-tasks-devapp-juqrcrzfphz8a3ihfmwwdj.streamlit.app/)

---

## Sample Use Case (Business Scenario)

> The mall wants to run a promotional campaign. Instead of a generic discount for all, the marketing team can now:
- Send luxury promotions to **Premium Spenders**
- Engage **Budget Enthusiasts** with bundle deals
- Improve offers for **Cautious Elites** to boost spending
- Reward **Young Averages** to build long-term loyalty

 This is real **data-driven marketing** in action.

---

## Technologies Used

- **Python**
- **Pandas, NumPy, Scikit-learn**
- **Seaborn, Matplotlib, Plotly**
- **Streamlit** for interactive frontend
- **FPDF** for PDF report generation
- **t-SNE** for dimensionality reduction

---

## How to Run

1. Clone the repo:
```bash
git clone https://github.com/zeeshan-akram-ds/internship-tasks-devhub/tree/main/Batch2/Task2_Customer_Segmentation
cd Task2_Customer_Segmentation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run Streamlit app:
```bash
streamlit run app.py
```

---
## About Me
Zeeshan Akram

BS Software Engineering | Data Science Enthusiast

I love solving real-world business problem using data & intelligent model.

LinkedIn | GitHub

---
### License
This project is for educational and demonstration purpose. You may reuse it with attribution. For commercial use, please contact me.
