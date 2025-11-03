def categorize_transactions(df):
    categories = {
        'Rent': ['rent', 'lease'],
        'Food': ['grocery', 'restaurant', 'food', 'cafe'],
        'Transport': ['bus', 'train', 'fuel', 'taxi', 'uber'],
        'Utilities': ['electricity', 'water', 'gas', 'internet', 'wifi', 'bill'],
        'Entertainment': ['movie', 'concert', 'subscription'],
        'Income': ['salary', 'income']
    }
    def get_category(description):
        description = str(description).lower()
        for cat, keywords in categories.items():
            if any(kw in description for kw in keywords):
                return cat
        return 'Other'
    df['Category'] = df['Description'].apply(get_category)
    return df

def summary_report(df):
    summary = df.groupby('Category')['Amount'].sum()
    mean_expense = df['Amount'].mean()
    savings_ratio = None
    if 'Income' in summary.index and 'Food' in summary.index:
        savings_ratio = summary['Income'] / abs(summary['Food']) if summary['Food'] != 0 else None
    return summary, mean_expense, savings_ratio
