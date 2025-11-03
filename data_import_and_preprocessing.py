import pandas as pd
import numpy as np

def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV or XLSX files are supported.")

def clean_data(df):
    df = df.dropna(subset=['Date', 'Amount', 'Description'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.drop_duplicates()
    return df
