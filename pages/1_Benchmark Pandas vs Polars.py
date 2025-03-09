# Import necessary libraries
import streamlit as st
import pandas as pd

# Header
# Create two columns
col1, col2 = st.columns(2)
col1.image("logo.jpg", width=200)
col2.markdown("<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>", unsafe_allow_html=True)

# Set the sidebar menu
st.sidebar.title("Menu")
st.sidebar.subheader("Select the page to navigate")

st.markdown(
    "<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='color: orange; font-weight: bold;'>Part1 B: Pandas vs Polars</h2>",
    unsafe_allow_html=True
)

# Content for Part2 A
st.markdown(
    "<div style='text-align: center;'>Performance of Pandas and Polars Libraries Execution.</div>",
    unsafe_allow_html=True
)

# Load the CSV file
df_part1 = pd.read_csv('Benchmark_Pandas_Polars.csv')

# Apply CSS to center the table
st.markdown(
    """
    <style>
    .center-table {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the table centered using st.markdown
st.markdown('<div class="center-table">' + df_part1.to_html(index=False) + '</div>', unsafe_allow_html=True)