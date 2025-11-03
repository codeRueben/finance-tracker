from data_import_and_preprocessing import load_data, clean_data
from categorization_and_analysis import categorize_transactions, summary_report
from visualization_plotly import plot_expense_distribution, plot_monthly_trends

def main():
    file_path = input("Enter path to CSV/XLSX file: ")
    df = load_data(file_path)
    df = clean_data(df)
    df = categorize_transactions(df)
    summary, mean_expense, savings_ratio = summary_report(df)
    print("Expense Summary:\n", summary)
    print("Mean Expense:", mean_expense)
    if savings_ratio is not None:
        print("Savings Ratio:", savings_ratio)
    plot_expense_distribution(df)    # In CLI, make sure this uses fig.show()
    plot_monthly_trends(df)          # In CLI, make sure this uses fig.show()

if __name__ == "__main__":
    main()
