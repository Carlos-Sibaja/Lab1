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
import streamlit



# Header
# Create two columns
col1, col2 = st.columns(2)
col1.image("logo.jpg", width=200)
col2.markdown("<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>", 
              unsafe_allow_html=True)
st.markdown("<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenz Id: 300384848</h3>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Menu")

# Load S&P 500 company tickers
sp500_companies = pd.read_csv("sp500_companies.csv")
sp500_companies["Ticker"] = sp500_companies["Ticker"].str.upper()

# Load dataset
df = pd.read_csv("all_stocks_5yr.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Get unique stock tickers
tickers = df["name"].unique()

# User input for stock ticker
col1, col2, col3 = st.columns(3)

# Create an input field to filter tickers
search_term = col1.text_input("### Search for a ticker (Start typing):", "")

# Dynamically filter tickers
filtered_tickers = [ticker for ticker in tickers if ticker.upper().startswith(search_term.upper())]

# Display a selectbox with the filtered options
userInput = col2.selectbox("Choose a company ticker:", filtered_tickers if filtered_tickers else tickers)

# Get company name
companyName = sp500_companies.loc[sp500_companies["Ticker"] == userInput, "Name"]
companyName = companyName.values[0] if not companyName.empty else "Company Not Found"
col3.text_input("Company Name", companyName, disabled=True)

# Load dataset
df = pd.read_csv("all_stocks_5yr.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Filter data for selected company
df_selected = df[df["name"].str.upper() == userInput.upper()]

if df_selected.empty:
    st.error(f"No data found for {userInput}. Please enter a valid ticker.")
    st.stop()

# Feature engineering
df_selected["SMA_10"] = df_selected["close"].rolling(window=10).mean()
df_selected["Volatility"] = df_selected["close"].rolling(window=10).std()
df_selected["prev_close"] = df_selected["close"].shift(1)
df_selected["prev_volume"] = df_selected["volume"].shift(1)
df_selected = df_selected.dropna()

# Define features and target
X = df_selected[["prev_close", "prev_volume", "SMA_10", "Volatility"]]
y = df_selected["close"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
lin_reg = LinearRegression().fit(X_train, y_train)
rf_reg = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_split=5, random_state=42).fit(X_train, y_train)

# Evaluate models
lin_reg_r2 = r2_score(y_test, lin_reg.predict(X_test))
rf_reg_r2 = r2_score(y_test, rf_reg.predict(X_test))

# *******************Predict 90 days into the future**************
future_dates = pd.date_range(df_selected["date"].iloc[-1], periods=16, freq='B')[1:]
future_predictions = []
last_row = pd.DataFrame([X.iloc[-1]], columns=X.columns)

for i in range(15):
    pred_price = rf_reg.predict(last_row)[0]
    future_predictions.append(pred_price)
    last_row = pd.DataFrame([[pred_price] + last_row.iloc[0, 1:].tolist()], columns=X.columns)

# Create table for predictions
st.markdown(f"<h2 style='text-align: center; font-size: 24px; color: orange'>Predicted Next Day Closing Price for {companyName}</h2>", unsafe_allow_html=True)

# Load the CSV file
df_part3 = pd.read_csv('Predictions.csv')

# Display the table centered using st.markdown
st.markdown(
    """
   <style>
      th, td {
        text-align: center !important;
        vertical-align: bottom !important;
    }
  
   .dataframe {
        display: block;
        margin-left: 20%;
        margin-right: auto;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the table centered using st.markdown
st.markdown('<div class="center-table">' + df_part3.to_html(index=False) + '</div>', unsafe_allow_html=True)

# Display R² values
st.write("\n")
st.markdown(f"<h2 style='text-align: center; font-size: 24px; color: orange;'>R² Comparison for {companyName} / {userInput} </h2>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)
col1.metric("Linear Regression R²", f"{lin_reg_r2:.4f}")
col2.metric("Random Forest R²", f"{rf_reg_r2:.4f}")

# Plot actual prices
plt.figure(figsize=(9, 5))
plt.plot(df_selected["date"], df_selected["close"], label=f"{userInput}/{companyName} Actual", linestyle="-")
plt.plot(future_dates, future_predictions, marker="o", markersize=3, linestyle="dashed", label=f"{userInput}/{companyName} Predicted")
plt.xlabel("Year")
plt.ylabel("Closing Price")
plt.title(f"Stock Price Prediction for {companyName} ({userInput}) -Next 15 Days-")
plt.legend()
plt.grid(True)

# Show plot in Streamlit
st.pyplot(plt)