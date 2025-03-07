#pip install streamlit
#  streamlit run 0_Benchmark_CSV_Parquet.py to run de app
#  streamlit run app.py --server.port 8501 to run de app in a different port
# IP Address: https://spltopics4260lab1.streamlit.app/

# Import the Streamlit library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Page name
st.set_page_config(page_title="Lab1", page_icon=":chart_with_upwards_trend:", layout="wide")

# Set the sidebar menu
st.sidebar.title("Menu")
st.sidebar.subheader("Select the page to navigate")
st.sidebar.write("Great Video on Streamlit")
st.sidebar.link_button("Watch the video", "https://www.youtube.com/watch?v=D0D4Pa22iG0")


# Load the logo and display it at the top-left
st.image("logo.jpg", width=200)  # Adjust width if needed

# ********************Title and subtitle of the app
st.markdown(
    "<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>",
    unsafe_allow_html=True
)

# Part1 A: Benchmark CSV vs Parquet
st.markdown(
    "<h2 style='color: orange; font-weight: bold;'>Part1 A: Benchmark CSV vs Parquet</h2>",
    unsafe_allow_html=True
)

# Content for Part1 A
st.write("Comparison of the performance of CSV and Parquet formats for 1X, 10X, 100X.")

df_part1 = pd.read_csv('benchmark_csv_parquet.csv')
st.write(df_part1.set_index("Scale"))

st.write("\n")


# ****  Graph for Part1 A
st.write("Graph for Part1 A")
# Load the original dataset
df= pd.read_csv('benchmark_csv_parquet.csv')

# Function to plot graphs
def plot_graphs(variable):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    scales = [1, 10, 100]
    titles = ["Scale 1X", "Scale 10X", "Scale 100X"]

    for i, scale in enumerate(scales):
        df_scale = df[df["Scale"] == scale]
        x_labels = ["CSV", "Parquet"]

        if variable == "Size":
            values = [df_scale["CSV_Size_MB"].mean(), df_scale["Parquet_Size_MB"].mean()]
            ylabel = "Size (MB)"
        elif variable == "Read Time":
            values = [df_scale["CSV_Read_Time_s"].mean(), df_scale["Parquet_Read_Time_s"].mean()]
            ylabel = "Read Time (s)"
        elif variable == "Write Time":
            values = [df_scale["CSV_Write_Time_s"].mean(), df_scale["Parquet_Write_Time_s"].mean()]
            ylabel = "Write Time (s)"
        else:
            raise ValueError("Invalid variable. Choose 'Size', 'Read Time', or 'Write Time'.")

        axes[i].bar(x_labels, values, color=["blue", "green"])
        axes[i].set_title(titles[i])
        axes[i].set_ylabel(ylabel)
        axes[i].set_xlabel("Format")
        axes[i].grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()
#  esta malo,  necesito que escoga la compresion y hacer el input para escoger la variable. 
 = col1.text_input("### Search for a ticker (Start typing):", "")

# Example usage: Choose the variable to visualize
plot_graphs("Size")  # Change to "Read Time" or "Write Time" to see different metrics

