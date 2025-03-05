# Import the Streamlit library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from tabulate import tabulate  # To display results in table format

# Load the logo and display it at the top-left
st.image("logo.jpg", width=250)  # Adjust width if needed

# ********************Title and subtitle of the app
st.markdown(
    "<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>",
    unsafe_allow_html=True
)

# ------------------Section B: Price Prediction Models
st.markdown(
    "<h2 style='color: orange; font-weight: bold;'>Part B: Price Prediction Models</h2>",
    unsafe_allow_html=True
)
# Placeholder content for Part B
# Load the S&P 500 companies dataset
sp500_companies = pd.read_csv("sp500_companies.csv")
# Convert tickers to uppercase for consistency
sp500_companies["Ticker"] = sp500_companies["Ticker"].str.upper()

st.write("This section will display stock price predictions using different algorithms.")

col1, col2 = st.columns(2)
userInput = col1.text_input(f"### Choose the company to predict the stock price: ","AAPL")

#Search for the company name in the CSV
companyName = sp500_companies.loc[sp500_companies["Ticker"] == userInput, "Name"]

# If the ticker is found, retrieve the company name; otherwise, show an error message
if not companyName.empty:
    companyName = companyName.values[0]
else:
    companyName = "Company Not Found"

# Display the company name in the second column
col2.text_input("Company Name", companyName, disabled=True)

# Load dataset
csv_file = "all_stocks_5yr.csv"
df = pd.read_csv(csv_file)

# Convert date column to datetime and sort values
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Select Company
selected_company = [userInput]  # ["AAPL", "GOOGL", "AMZN"]
df_selected = df[df["name"].str.upper() == userInput.upper()]

if df_selected.empty:
    st.error(f"No data found for {userInput}. Please enter a valid company name.")
    st.stop()

# Initialize storage for results
results = []
r2_scores = []

# Process each company separately
for company in selected_company:
    df_company = df_selected[df_selected["name"] == company].copy()

    # Create additional features
    df_company["SMA_10"] = df_company["close"].rolling(window=10).mean()  # 10-day moving average
    df_company["Volatility"] = df_company["close"].rolling(window=10).std()  # Standard deviation (volatility)

    # Drop NaN values from rolling calculations
    df_company = df_company.dropna()

    # Define features (X) and target (y)
    X = df_company[["close", "volume", "SMA_10", "Volatility"]]
    y = df_company["close"].shift(-1)  # Predict next day's closing price

    # Drop last row because it has NaN in y (shifted row)
    X, y = X[:-1], y[:-1]

    # Split into 80% training and 20% testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    lin_reg_pred = lin_reg.predict(X_test)
    lin_reg_r2 = r2_score(y_test, lin_reg_pred)

    # Train Random Forest model
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_reg.fit(X_train, y_train)
    rf_reg_pred = rf_reg.predict(X_test)
    rf_reg_r2 = r2_score(y_test, rf_reg_pred)

    # Get the last available row for prediction
    last_row = X.iloc[-1].values.reshape(1, -1)
    predicted_lin = lin_reg.predict(last_row)[0]
    predicted_rf = rf_reg.predict(last_row)[0]

    # Store results
    last_date = df_company["date"].iloc[-1]
    actual_last_price = df_company["close"].iloc[-1]
    results.append([company, last_date, actual_last_price, predicted_lin, predicted_rf])
    r2_scores.append([company, lin_reg_r2, rf_reg_r2])

# Convert results to DataFrame
results_df3 = pd.DataFrame(results, columns=["Company", "Previous Date", "Previous Price", "Predicted Linear Regression", "Predicted Random Forest"])

# Save the benchmark results to a CSV file
results_df3.to_csv("Predictions.csv", index=False)

# Content for Part3
st.write(f"### Stock Price Prediction for next day for: {userInput}")

df_part3 = pd.read_csv('Predictions.csv')
st.write(df_part3.set_index("Company"))

# Display the table centered using st.markdown
st.write(f"### R² Comparison for {userInput}")
col1, col2, col3 = st.columns(3)
col1.metric(label="Company", value=userInput)
col2.metric(label="R² Linear Regression", value=f"{lin_reg_r2:.4f}")
col3.metric(label="R² Random Forest", value=f"{rf_reg_r2:.4f}")