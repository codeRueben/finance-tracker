import streamlit as st
import plotly.express as px

def plot_expense_distribution(df):
    cat_sum = df.groupby('Category')['Amount'].sum().reset_index()
    fig = px.pie(
        cat_sum,
        names='Category',
        values='Amount',
        title='Expense Distribution',
        color_discrete_sequence=px.colors.qualitative.Vivid,
        hole=0.4
    )
    fig.update_traces(
        textinfo='percent+label+value',
        pull=[0.02 for _ in cat_sum['Category']]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend_font_color='white',
        title_font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_trends(df):
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_expense = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_expense['Month'] = monthly_expense['Month'].astype(str)
    fig = px.line(
        monthly_expense,
        x='Month',
        y='Amount',
        title='Monthly Expense Trend',
        markers=True,
        line_shape='linear',
        text='Amount'
    )
    fig.update_traces(textposition="top center", line=dict(color='#00E5FF', width=4))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend_font_color='white',
        title_font_color='white',
        xaxis_title_font=dict(color="white"),
        yaxis_title_font=dict(color="white"),
        xaxis=dict(showgrid=True, gridcolor='gray', tickfont=dict(color='white')),
        yaxis=dict(showgrid=True, gridcolor='gray', tickfont=dict(color='white'))
    )
    st.plotly_chart(fig, use_container_width=True)
