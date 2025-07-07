import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pdf_generator import generate_segment_pdf

# Set page title
st.set_page_config(page_title="Customer Segmentation App", layout="wide")

# Load data
main_df = pd.read_csv("mall_customers_original_with_segments.csv", sep=',')
final_df = pd.read_csv("mall_customers_scaled_with_segments.csv", sep=',')
segments = ['All Segments'] + sorted(main_df['Segment'].unique().tolist())
## Sidebar
st.sidebar.title("Customer Segmentation App")
segment_selected = st.sidebar.selectbox('Select a Segment', options=segments, key='segment_select')
if segment_selected != 'All Segments':
    selected_main_df = main_df[main_df['Segment'] == segment_selected].drop(columns=['TSNE-2','TSNE-1','CustomerID'], axis=1)
    selected_final_df = final_df[final_df['Segment'] == segment_selected]
    # Main content
    st.title(f"Customer Segmentation for {segment_selected}")
    ## Showing stats and strategy for selected segment
    st.markdown(f"### Profile Summary: {segment_selected}")
    st.markdown("Below is a statistical overview of the selected segment's key attributes " \
    "including **Age**, **Annual Income**, and **Spending Score**. These values represent " \
    "central tendencies, spread, and customer behavior patterns.")
    st.dataframe(selected_main_df.describe().T, use_container_width=True)
    st.markdown("These scaled values were used to cluster customers via **K-Means**, allowing " \
    "me to position this group meaningfully in the market space.")
    st.markdown("### Cluster Engine Input Preview")
    st.dataframe(selected_final_df.head(), use_container_width=True)
else:
    # Main content for all segments
    st.title("Customer Segmentation Overview")
    st.markdown("### Overall Customer Profile Summary")
    st.markdown("Below is a statistical overview of all segments key attributes " \
    "including **Age**, **Annual Income**, and **Spending Score**. These values represent " \
    "central tendencies, spread, and customer behavior patterns.")
    st.dataframe(main_df.describe().T, use_container_width=True)
    st.markdown("### Scaled Data for Clustering")
    st.dataframe(final_df.head(), use_container_width=True)
show_strategy = st.sidebar.checkbox('Show Marketing Strategy', value=True, key='show_strategy')
if show_strategy:
    st.markdown("""
    ### Project Objective

    This app aims to segment mall customers using key features such as **Age**, **Annual Income**, and **Spending Score**. The primary goals are:

    - **Identify distinct customer groups** within the mall’s audience
    - **Understand the behavioral profile** of each segment
    - **Enable data-driven marketing decisions** for personalized offers and promotions

    By grouping customers based on their habits and demographics, the mall can **maximize marketing ROI**, improve customer satisfaction, and uncover valuable business opportunities.
    """)

st.subheader("Visualizing Customer Segments with t-SNE")

# Filter the data if a specific segment is selected
if segment_selected != 'All Segments':
    st.info(f"You're now viewing the **{segment_selected}** segment in t-SNE space.")

    filtered_df = main_df[main_df['Segment'] == segment_selected]

    fig = px.scatter(
        data_frame=filtered_df,
        x='TSNE-1',
        y='TSNE-2',
        color='Segment',
        hover_data=['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
        title=f't-SNE Projection of {segment_selected}',
        template='plotly_white'
    )
else:
    fig = px.scatter(
        data_frame=main_df,
        x='TSNE-1',
        y='TSNE-2',
        color='Segment',
        hover_data=['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
        title='t-SNE Projection of Customer Segments',
        template='plotly_white'
    )

# Style and display the figure
fig.update_traces(marker=dict(size=9, line=dict(width=1, color='DarkSlateGrey')))
fig.update_layout(legend_title_text='Customer Segment')

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interpretation of t-SNE Clustering

The t-SNE projection clearly separates customer segments into distinct spatial regions. Here's what we observe:

- **Segment: Mature Moderates** -> Positioned top-right, indicating strong cohesion and similarity in their behavior.
- **Segment: Premium Spenders** -> Bottom-right cluster, showing high spending and income.
- **Segment: Young Averages** -> Center-left, moderate behavior on both dimensions.
- **Segment: Cautious Elites** -> Lower-left, high income but minimal spending — a low-engagement group.
- **Segment: Budget Enthusiasts** -> Centered tightly, lower income but high spending behavior.

This separation confirms the effectiveness of clustering and supports targeted strategies.
""")
if segment_selected != 'All Segments':
    st.markdown(f"""
    ### Insight: {segment_selected}
    
    Customers in this segment share closely grouped behavior in the t-SNE space, suggesting a well-defined profile.
    
    Use this segmentation to:
    - Craft targeted marketing messages
    - Launch personalized offers
    - Build customer loyalty programs
    
    This group demonstrates unique shopping behavior, making them ideal for focused strategies.
    """)

# Prepare content for PDF
if st.sidebar.button("Generate PDF Report"):
    
    if segment_selected == "All Segments":
        summary_text = (
            "This report provides a complete breakdown of all customer segments identified through clustering. "
            "Each group is analyzed based on key metrics such as Age, Annual Income, Spending Score, and Gender."
        )

        # Group by Segment
        segment_stats_dict = {}
        for seg in main_df['Segment'].unique():
            sub_df = main_df[main_df['Segment'] == seg]
            stats = sub_df.describe().T

            segment_stats_dict[seg] = {
                "Total Customers": len(sub_df),
                "Mean Age": round(stats.loc["Age"]["mean"], 2),
                "Mean Income ($k)": round(stats.loc["Annual Income (k$)"]["mean"], 2),
                "Mean Spending Score": round(stats.loc["Spending Score (1-100)"]["mean"], 2),
                "Male %": f"{round(final_df['Genre_Male'].mean() * 100, 1)}%",
                "Female %": f"{round((1 - final_df['Genre_Male'].mean()) * 100, 1)}%"
            }

        pdf_file = generate_segment_pdf("All Segments", summary_text, segment_stats_dict)

    else:
        # Single segment report
        sub_df = main_df[main_df['Segment'] == segment_selected]
        stats = sub_df.describe().T

        summary_text = f"""This report focuses on the '{segment_selected}' segment of mall customers. 
It includes a behavioral and demographic summary to support personalized marketing efforts."""

        segment_stats = {
            "Total Customers": len(sub_df),
            "Mean Age": round(stats.loc["Age"]["mean"], 2),
            "Mean Income ($k)": round(stats.loc["Annual Income (k$)"]["mean"], 2),
            "Mean Spending Score": round(stats.loc["Spending Score (1-100)"]["mean"], 2),
            "Male %": f"{round(final_df['Genre_Male'].mean() * 100, 1)}%",
            "Female %": f"{round((1 - final_df['Genre_Male'].mean()) * 100, 1)}%"
        }

        pdf_file = generate_segment_pdf(segment_selected, summary_text, segment_stats)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Download PDF Report",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )