from data_import_and_preprocessing import load_data, clean_data
from categorization_and_analysis import categorize_transactions, summary_report
from visualization_plotly import plot_expense_distribution, plot_monthly_trends
import streamlit as st
import pandas as pd
import numpy as np

# AI
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

st.markdown("# 💸 Personal Finance Tracker")
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.info("Upload your data and explore trends!")

menu = st.sidebar.radio(
    "Select Page",
    ["Upload Data", "Summary & Analytics", "Visualize", "Predict Next Month", "About"],
    format_func=lambda x: "🤖 "+x if "Predict" in x else ("📈 "+x if x == "Visualize" else x)
)

def predict_next_month(df):
    # Suppose df has a "Date" column (month) and "Amount" column
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        st.info("Date or Amount column missing for prediction.")
        return
    df['Date'] = pd.to_datetime(df['Date'])
    monthly = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum().reset_index()
    monthly['DateInt'] = np.arange(len(monthly))
    X = monthly[['DateInt']]
    y = monthly['Amount']
    if len(X) < 2:
        st.info("Need at least two months of data for prediction.")
        return
    model = LinearRegression().fit(X, y)
    pred_next = model.predict([[len(monthly)]])[0]
    st.metric("Predicted Next Month Expense", f"₹{pred_next:.2f}")
    st.line_chart(pd.DataFrame({'Actual': y, 'Predicted': np.append(model.predict(X), pred_next)}, index=monthly['Date'].astype(str).tolist() + ['Next']))


def main():
    if menu == "Upload Data":
        st.markdown("## 📂 Upload Data")
        uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                df = load_data(uploaded_file)
                df = clean_data(df)
                df = categorize_transactions(df)
                st.session_state['df'] = df
                st.success("Data uploaded and processed successfully!")
                with st.expander("Show Full Data Table"):
                    st.dataframe(df)
                csv = df.to_csv(index=False).encode()
                st.download_button("Download Processed Data", csv, "finance_report.csv", "text/csv")
            except Exception as e:
                st.error(f"Error processing file: {e}")
                st.stop()
        else:
            st.warning("Please upload a CSV or Excel file to begin.")

    elif menu == "Summary & Analytics":
        st.markdown("## 📊 Summary & Analytics")
        df = st.session_state.get('df', None)
        if df is not None:
            summary, mean_expense, savings_ratio = summary_report(df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Mean Monthly Expense", f"₹{mean_expense:.2f}")
            if 'Income' in summary.index:
                col2.metric("Total Income", f"₹{summary.get('Income', 0):.2f}")
            col3.metric("Savings Ratio", f"{savings_ratio:.2%}" if savings_ratio else "N/A")
            st.markdown("### Category Expense Breakdown")
            st.table(summary)
        else:
            st.info("Please upload data first in the Upload Data tab.")

    elif menu == "Visualize":
        st.markdown("## 📈 Visualize Trends")
        df = st.session_state.get('df', None)
        if df is not None:
            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown("### Expense Distribution")
                plot_expense_distribution(df)
            with col2:
                st.markdown("### Monthly Expense Trend")
                plot_monthly_trends(df)
        else:
            st.info("Please upload data first in the Upload Data tab.")

    elif menu == "Predict Next Month":
        st.markdown("## 🤖 AI Expense Prediction")
        df = st.session_state.get('df', None)
        if df is not None:
            predict_next_month(df)
        else:
            st.info("Please upload data first in the Upload Data tab.")

    elif menu == "About":
        st.markdown("""
        ## ℹ️ About This Project
        Built by Your Name.  
        Upload your financial transactions and interactively explore your personal spending, savings, trends, and predictions.
        """)

if __name__ == "__main__":
    main()
