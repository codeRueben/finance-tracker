from data_import_and_preprocessing import load_data, clean_data
from categorization_and_analysis import categorize_transactions, summary_report
from visualization_plotly import plot_expense_distribution, plot_monthly_trends
import streamlit as st

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

def main():
    st.title("Personal Finance Tracker")
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Select Page", ["Upload Data", "Summary & Analytics", "Visualize", "About"])

    if menu == "Upload Data":
        uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                df = load_data(uploaded_file)
                df = clean_data(df)
                df = categorize_transactions(df)
                st.session_state['df'] = df
                st.success("Data uploaded and processed successfully!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error processing file: {e}")
                st.stop()

    elif menu == "Summary & Analytics":
        df = st.session_state.get('df', None)
        if df is not None:
            summary, mean_expense, savings_ratio = summary_report(df)
            st.write("Expense Summary:", summary)
            st.write("Mean Monthly Expense:", mean_expense)
            if savings_ratio:
                st.write("Savings Ratio:", savings_ratio)
        else:
            st.info("Please upload data first in the Upload Data tab.")

    elif menu == "Visualize":
        df = st.session_state.get('df', None)
        if df is not None:
            plot_expense_distribution(df)
            plot_monthly_trends(df)
        else:
            st.info("Please upload data first in the Upload Data tab.")

    elif menu == "About":
        st.markdown("""
        ### About This Project
        Built by Your Name.
        This dashboard allows you to upload your financial transactions and explore your spending, savings, and trends interactively!
        """)

if __name__ == "__main__":
    main()
