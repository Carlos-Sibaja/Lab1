# Import the Streamlit library
import streamlit as st
import pandas as pd
import numpy as np

# Load the logo and display it at the top-left
st.image("logo.jpg", width=200)  

# Set the sidebar menu
st.sidebar.title("Menu")
st.sidebar.subheader("Select the page to navigate")

# ********************Title and subtitle of the app
st.markdown(
    "<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>",
    unsafe_allow_html=True)
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