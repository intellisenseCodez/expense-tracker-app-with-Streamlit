from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

from model import Expense, Base
import controller


# set page configuration
st.set_page_config(
  page_title="Home - Expense Tracker App",
  page_icon="📈",
  layout="wide",
  initial_sidebar_state="auto",
  menu_items={
      'About': "# Developed by: Olar."
  }
)

# create an engine
engine  = create_engine('sqlite:///expense.db')

# create a session
Session = sessionmaker(bind=engine)
session = Session()

# create database
Base.metadata.create_all(engine) 






st.markdown("# Expense Tracker App 🔍")
st.markdown("Manage your Expenses with Ease.")



# add actions button to navigate pages
operation = st.sidebar.selectbox(label="Choose Operation", options=['🏠 Home',
                                                        '📕 Add Expense', 
                                                        '📖 View Expense',
                                                        '📝 Edit Expense',
                                                        '🗑️ Delete Expense'], index=0)


if operation == "📕 Add Expense":
  controller.add_expense()   
elif operation == "📖 View Expense":
  controller.list_expenses()
elif operation == "📝 Edit Expense":
  controller.edit_expense()
elif operation == "🗑️ Delete Expense":
  controller.delete_expense()
else:
  col1, col2 = st.columns(2)
  expense_df = pd.read_sql_table('expenses', engine)

  with col1:
    st.markdown("##### Count of Expenses")
    st.markdown(f"### {expense_df.shape[0]}")

  with col2: 
    st.markdown("##### Total Expenses")

    total = expense_df['amount'].sum()
    st.markdown(f"### # {total}")
    
  st.divider()
  
  
  st.bar_chart(expense_df.groupby("category")['amount'].sum())
  
  # year = pd.DatetimeIndex(expense_df['date_added']).month
  by_date = expense_df.groupby('date_added')['amount'].sum().reset_index()
  st.line_chart(data =by_date, x='date_added', y='amount')
