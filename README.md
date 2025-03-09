# Lab Work: Data Analytics with Streamlit

## Overview
This project is part of the CSIS 4260 – Special Topics in Data Analytics course. The application is built using Streamlit and focuses on benchmarking different data processing techniques and predicting stock prices.

## Approach
The initial approach was to develop the entire scope using Anaconda/Jupyter Notebook. However, I encountered many challenges managing the installation of Polars. It was recommended to move the Jupyter Notebook to Visual Studio Code (VSC) to gain more resources.

The Jupyter Notebook (`Lab1_Spl.ipynb`) remained as the main source for the calculations of the benchmarks and predictions. Several `.py` files were used to manage the Streamlit code to create the dashboard.

The outputs of the file `Lab1_Spl.ipynb` were saved as individual CSV files to be used as input for the dashboard. During the development of the dashboard, part of the code for the calculations was moved inside the `.py` files.

As a result, the code for the calculations of the benchmarks is located in `Lab1_Spl.ipynb`, and the regressions are inside the `.py` files.

Finally, the application was published using Streamlit Cloud.

## Features
- **Benchmark CSV vs Parquet**: Compare the performance of CSV and Parquet file formats in terms of size and processing time.
- **Benchmark Pandas vs Polars**: Evaluate the performance of Pandas and Polars libraries for data manipulation and analysis.
- **Stock Price Prediction**: Predict future stock prices using machine learning models such as Linear Regression and Random Forest.

## Main File
The main file for running the application is `0_Benchmark_CSV_Parquet.py`. To run the application, use the following command:
```bash
streamlit run 0_Benchmark_CSV_Parquet.py
```

You can also run the application on a different port using:


streamlit run app.py --server.port 8501
The application is also publicly available on Streamlit Cloud at the following link: https://stockprice-lab1.streamlit.app/

## GitHub
The files for this project can be accessed on https://github.com/Carlos-Sibaja/Lab1.git

## Installation
To install the necessary dependencies, create a requirements.txt file with the following content:
```
streamlit
pandas
seaborn
matplotlib
scikit-learn
```

## Contact
For any questions or issues, please contact Carlos Sibaja
