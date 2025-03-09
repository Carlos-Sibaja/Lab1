#pip install streamlit
#  streamlit run 0_Benchmark_CSV_Parquet.py to run de app
#  streamlit run app.py --server.port 8501 to run de app in a different port
# IP Address: https://spltopics4260lab1.streamlit.app/

# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate 

# Streamlit Page Configuration
st.set_page_config(page_title="Lab1", page_icon=":chart_with_upwards_trend:", layout="wide")

# Sidebar Menu
st.sidebar.title("Menu")
st.sidebar.subheader("Select the page to navigate")

#Header
# Create two columns
col1, col2 = st.columns(2)
col1.image("logo.jpg", width=200)
col2.markdown("<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>", unsafe_allow_html=True)

st.markdown("<h2 style='color: orange; font-weight: bold;'>Part1 A: Benchmark CSV vs Parquet</h2>", unsafe_allow_html=True)

# Load Data
df_part1 = pd.read_csv('benchmark_csv_parquet.csv')

# Indicator Selection
st.markdown("<h3 style='color:blue; font-weight: bold; text-align: left;'>Dynamic Visualization</h3>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        /* Centering the radio button container */
        div[data-testid="stRadio"] {
            display: flex;
            justify-content: center;
            background-color: orange;
            padding: 10px;
            border-radius: 20px;
            width: 60%;
            margin: auto;
        }

        /* Make buttons bigger */
        div[data-testid="stRadio"] label {
            font-size: 20px !important;
            padding: 10px 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

choices = ["Size", "Read Time", "Write Time"]
variable = st.radio("Select to start the Benchmark:", choices, horizontal=True)

# Column mappings
column_mapping = {
    "Size": ("CSV_Size_MB", "Parquet_Size_MB"),
    "Read Time": ("CSV_Read_Time_s", "Parquet_Read_Time_s"),
    "Write Time": ("CSV_Write_Time_s", "Parquet_Write_Time_s")
}
csv_col, parquet_col = column_mapping[variable]

# Function to plot graphs
def plot_graphs(csv_col, parquet_col):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    scales = [1, 10, 100]
    titles = ["Scale 1X", "Scale 10X", "Scale 100X"]
    compression_types = ["None", "snappy", "gzip", "brotli"]
    colors = ["blue", "green"]

    for i, scale in enumerate(scales):
        df_scale = df_part1[df_part1["Scale"] == scale]

        values, labels = [], []

        for comp in compression_types:
            df_filtered = df_scale[df_scale["Compression"].fillna("None") == comp]

            if df_filtered.empty:
                continue  # Skip if no data for this compression type

            csv_value = df_filtered[csv_col].values[0]
            parquet_value = df_filtered[parquet_col].values[0]

            values.extend([csv_value, parquet_value])
            labels.extend([f"CSV-{comp}", f"Parquet-{comp}"])

        # Ensure data is present before plotting
        if len(values) == 0:
            st.warning(f"⚠️ No valid data for Scale {scale}")
            continue  

        ylabel = "Compression Technique"
        xlabel = "MB" if variable == "Size" else "Seconds"

        sns.barplot(x=values, y=labels, ax=axes[i], palette=colors * (len(values) // 2), orient='h')

        for index, value in enumerate(values):
            axes[i].text(value, index, f"{value:.1f}", va='center', ha='right', fontsize=9, color='white', weight='bold')

        axes[i].set_title(titles[i], fontsize=10, fontweight="bold", color="green")
        axes[i].set_ylabel(ylabel if i == 0 else "", fontsize=9)
        axes[i].set_xlabel(xlabel, fontsize=10, fontweight="bold")
        axes[i].tick_params(axis='x', labelsize=9)
        axes[i].grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

# Call function with correct column names
plot_graphs(csv_col, parquet_col)

# Display dataset in Streamlit
st.markdown("<h3 style='color:blue; font-weight: bold; text-align: left;'>Summary Table of Size of Files and Processing Time in Seconds</h3>", unsafe_allow_html=True)
st.markdown('<div class="center-table">' + df_part1.to_html(index=False) + '</div>', unsafe_allow_html=True)
