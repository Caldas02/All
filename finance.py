import streamlit as st
import pandas as pd
import plotly.express as px

# Title and description
st.title('Finance Manager')
st.write('Welcome to the Finance Manager app! This tool helps you manage your finances by tracking your income and expenses.')

# Sidebar options
st.sidebar.header('Options')
selected_option = st.sidebar.radio('Select an option:', ('Income', 'Expenses', 'Summary'))

# Load data
@st.cache_data()
def load_data():
    return pd.DataFrame(columns=['Category', 'Amount'])

data = load_data()

# Function to add income or expenses
def add_transaction():
    category = st.text_input('Enter category:')
    amount = st.number_input('Enter amount:', step=0.01)
    if st.button('Add Transaction'):
        data.loc[len(data)] = [category, amount]

# Function to show income
def show_income():
    income_data = data[data['Amount'] > 0]
    if not income_data.empty:
        fig = px.pie(income_data, values='Amount', names='Category', title='Income Breakdown')
        st.plotly_chart(fig)
    else:
        st.write('No income recorded yet.')

# Function to show expenses
def show_expenses():
    expenses_data = data[data['Amount'] < 0]
    if not expenses_data.empty:
        fig = px.pie(expenses_data, values='Amount', names='Category', title='Expenses Breakdown')
        st.plotly_chart(fig)
    else:
        st.write('No expenses recorded yet.')

# Function to show summary
def show_summary():
    total_income = data[data['Amount'] > 0]['Amount'].sum()
    total_expenses = abs(data[data['Amount'] < 0]['Amount'].sum())
    net_balance = total_income - total_expenses

    st.write(f'Total Income: ${total_income:.2f}')
    st.write(f'Total Expenses: ${total_expenses:.2f}')
    st.write(f'Net Balance: ${net_balance:.2f}')

# Main app logic
if selected_option == 'Income':
    st.header('Add Income')
    add_transaction()

elif selected_option == 'Expenses':
    st.header('Add Expenses')
    add_transaction()

elif selected_option == 'Summary':
    st.header('Summary')
    show_summary()
    st.subheader('Income Breakdown')
    show_income()
    st.subheader('Expenses Breakdown')
    show_expenses()
