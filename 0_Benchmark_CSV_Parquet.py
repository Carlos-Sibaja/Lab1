#pip install streamlit
#  streamlit run 0_Benchmark_CSV_Parquet.py to run de app
#  streamlit run app.py --server.port 8501 to run de app in a different port
# IP Address: https://spltopics4260lab1.streamlit.app/

# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit Page Configuration
st.set_page_config(page_title="Lab1", page_icon=":chart_with_upwards_trend:", layout="wide")

# Sidebar Menu
st.sidebar.title("Menu")
st.sidebar.subheader("Select the page to navigate")
st.sidebar.markdown("[Watch the video](https://www.youtube.com/watch?v=D0D4Pa22iG0)")

# Load and display the logo
st.image("logo.jpg", width=200)

# Title and Subtitle
st.markdown("<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='color: orange; font-weight: bold;'>Part1 A: Benchmark CSV vs Parquet</h2>", unsafe_allow_html=True)

# Load Data
df_part1 = pd.read_csv('benchmark_csv_parquet.csv')

# Indicator Selection
st.markdown("<h3 style='color:blue; font-weight: bold; text-align: left;'>Select Indicator for Visualization</h3>", unsafe_allow_html=True)
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
            width: 40%;
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
variable = st.radio("Choose the variable to visualize:", choices, horizontal=True)

# Function to Plot Graphs (CSV vs Parquet)
st.write("\n" * 3)

# Function to Plot Graphs (Compression Comparison)
def plot_graphs(variable):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    scales = [1, 10, 100]
    titles = ["Scale 1X", "Scale 10X", "Scale 100X"]
    compression_types = ["None", "gzip", "snappy", "brotli"]  # Compression methods
    colors = ["blue", "green", "blue", "green", "blue", "green", "blue", "green"]  # Blue for CSV, Green for Parquet

    for i, scale in enumerate(scales):
        df_scale = df_part1[df_part1["Scale"] == scale]

        # Extract values for CSV and Parquet with different compressions
        values = []
        labels = []
        for comp in compression_types:
            csv_value = df_scale[df_scale["Compression"] == comp]["CSV_Size_MB"].values
            parquet_value = df_scale[df_scale["Compression"] == comp]["Parquet_Size_MB"].values

            if len(csv_value) > 0:
                values.append(csv_value[0])
                labels.append(f"CSV-{comp}")
            if len(parquet_value) > 0:
                values.append(parquet_value[0])
                labels.append(f"Parquet-{comp}")

        ylabel = "Size (MB)" if variable == "Size" else ("Read Time (s)" if variable == "Read Time" else "Write Time (s)")
        
        # Improved graph styling
        sns.barplot(x=labels, y=values, ax=axes[i], palette=colors[:len(values)])

        # Display values on bars
        for index, value in enumerate(values):
            axes[i].text(index, value + (value * 0.02), f"{value:.1f}", ha='center', fontsize=8, color='black')

        axes[i].set_title(titles[i], fontsize=10, fontweight="bold", color="green")
        axes[i].set_ylabel(ylabel, fontsize=9)
        axes[i].set_xlabel("Compression Type", fontsize=9)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

# Plot Second Set of Graphs
plot_graphs(variable)

# ******************Part1 A: Benchmark CSV vs Parquet
st.write("Comparison of the performance of CSV and Parquet formats for 1X, 10X, 100X.")
st.write("\n")
st.write(df_part1.set_index("Scale"))
st.write("\n")
