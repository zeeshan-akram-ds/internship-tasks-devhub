from fpdf import FPDF
import plotly.io as pio
import os
import pandas as pd
from datetime import datetime
import pytz

# ----------------------------------------------
# PDF Report Generator for Superstore Dashboard
# ----------------------------------------------

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "Superstore Sales Dashboard", ln=True, align="C")
        self.ln(4)
        self.set_font("Arial", "", 12)
        self.set_text_color(90, 90, 90)
        self.cell(0, 10, "Comprehensive BI Report", ln=True, align="C")
        self.ln(5)

        # Pakistan timestamp
        pakistan_time = datetime.now(pytz.timezone('Asia/Karachi')).strftime("%B %d, %Y %I:%M %p")
        self.set_font("Arial", "I", 10)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Generated on: {pakistan_time}", ln=True, align="C")

        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100)
    
        self.cell(0, 5, f"Page {self.page_no()}", ln=True, align="C")
        self.set_y(-10)
        self.cell(0, 5, "Developed by Zeeshan Akram | GitHub: github.com/zeeshan-akram-ds | LinkedIn: linkedin.com/in/zeeshan-akram-572bbb34a", align="C")
        
    def add_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(20, 20, 20)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def add_kpi(self, label, value):
        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, f"{label}: {value}", ln=True)

    def add_insight_list(self, insights):
        self.set_font("Helvetica", "", 11)
        for item in insights:
            self.multi_cell(0, 8, f"- {item}")
        self.ln(5)

    def add_image(self, image_path, w=180):
        if os.path.exists(image_path):
            self.image(image_path, w=w)
            self.ln(10)

# ----------------------------------------------
# Main Function to Generate PDF Report
# ----------------------------------------------

def generate_pdf_report(df, kpis: dict, insights: list, chart_paths: list, output_path="superstore_report.pdf", alerts: list = None):
    """
    Generates a clean, fast business PDF report without heavy charts.
    
    Parameters:
    - df: Filtered DataFrame
    - kpis: Dictionary of key performance indicators
    - insights: Business insights
    - chart_paths: (Ignored) previously used for images
    - output_path: Filename to save PDF
    - alerts: List of business alert strings (losses, drops, etc.)
    """
    pdf = PDFReport()
    pdf.add_page()

    # Section: KPIs
    pdf.add_title("Key Performance Indicators")
    for label, value in kpis.items():
        pdf.add_kpi(label, value)

    # Section: Insights
    pdf.add_title("Business Insights")
    pdf.add_insight_list(insights)

    # Section: Alerts
    if alerts:
        pdf.add_title("Business Alerts")
        pdf.add_insight_list(alerts)

    # Optional: remove charts to improve speed/performance
    # Previously used chart_paths, now excluded for performance
    # pdf.add_title("Visual Charts")
    # for chart in chart_paths:
    #     pdf.add_image(chart)

    # Save PDF
    pdf.output(output_path)
    print(f"PDF Report saved as: {output_path}")
def generate_alerts(filtered_df: pd.DataFrame) -> list:
    """
    Analyze monthly sales and profit from the filtered dataframe
    and return a list of natural business alerts (losses, outliers, sharp drops).
    """
    alerts = []

    if filtered_df.empty:
        alerts.append("No data available for alert generation.")
        return alerts

    df = filtered_df.copy()
    df["Month_Year"] = df["Order Date"].dt.to_period("M").astype(str)

    # Monthly aggregation
    monthly = (
        df.groupby("Month_Year")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Month_Year")
    )

    # Detect Loss Months
    loss_months = monthly[monthly["Profit"] < 0]
    for _, row in loss_months.iterrows():
        alerts.append(f"Loss recorded in {row['Month_Year']} -> Profit: ${row['Profit']:,.0f}")

    # Sharp Profit Drops
    monthly["Profit_Change"] = monthly["Profit"].diff()
    sharp_drops = monthly[monthly["Profit_Change"] < -5000]
    for _, row in sharp_drops.iterrows():
        alerts.append(f"Sharp profit decline in {row['Month_Year']} -> Drop: ${abs(row['Profit_Change']):,.0f}")

    # Sales Outliers using IQR
    q1 = monthly["Sales"].quantile(0.25)
    q3 = monthly["Sales"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr
    outliers = monthly[(monthly["Sales"] > upper) | (monthly["Sales"] < lower)]
    for _, row in outliers.iterrows():
        alerts.append(f"Unusual sales in {row['Month_Year']} -> Sales: ${row['Sales']:,.0f}")

    # Clean streak (optional)
    if (monthly["Profit"] > 0).all() and len(monthly) > 0:
        alerts.append("No negative profit months detected during the selected period.")

    return alerts
# ----------------------------------------------
# Utility: Save Plotly Figure as PNG (for PDF use)
# ----------------------------------------------

def save_chart_image(fig, filename="chart.png", path="charts"):
    """
    Saves a Plotly figure to disk as PNG.
    Requires kaleido backend (auto used by Plotly).
    """
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, filename)
    pio.write_image(fig, file_path, format="png", width=1000, height=600, scale=1)
    return file_path

