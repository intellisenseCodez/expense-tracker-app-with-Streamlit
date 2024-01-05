from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import streamlit as st

from models import Base, Expense
import views as vw

import os


engine  = create_engine('sqlite:///expense_db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

# set page configuration
st.set_page_config(
  page_title="Home - Expense Tracker App",
  page_icon="🧊",
  layout="wide",
  initial_sidebar_state="expanded",
  menu_items={
      'About': "# Developed by: Olar."
  }
)

st.title("Expense Tracker App 🔍")
st.markdown("Manage your Expenses with Ease.")


# ========== Visualization =========




# add actions button to navigate pages
option = st.sidebar.selectbox(label="Choose Operation", options=['Choose ...',
                                                        'Add Expense', 
                                                        'View Expense',
                                                        'Edit Expense',
                                                        'Delete Expense'], index=0, key='option')


if st.session_state['option'] == "Add Expense":
  vw.add_view()    
elif st.session_state['option'] == "View Expense":
  vw.list_view()
elif st.session_state['option'] == "Edit Expense":
  vw.edit_view()
elif st.session_state['option'] == "Delete Expense":
  vw.delete_view()
else:
  col1, col2 = st.columns(2)

  with col1:
    st.markdown("##### Count of Expenses")
    all_expenses = session.query(Expense).all()
    st.markdown(f"### {len(all_expenses)}")

  with col2: 
    st.markdown("##### Total Expenses")
    all_expenses = session.query(Expense).all()
    total = 0
    for expense in all_expenses:
      total += expense.amount
      
    st.markdown(f"### {total}")

  
  
if __name__ == "__main__":
    # create an engine
    engine  = create_engine('sqlite:///expense_db.sqlite3')
    Base.metadata.create_all(engine) 

