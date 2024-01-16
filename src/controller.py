import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import Expense, Base
from main import session

import os


def add_expense():
        
    st.subheader("Add New Expense 📝")    
    # add expenses form
    with st.form(key="add_expense", clear_on_submit=True):
        title = st.text_input(label="Expense Title:")
        amount = st.number_input(label="Expense Amount:")
        paid_to = st.text_input(label="Paid To:")
        category = st.selectbox(label="Expense Category:", options=['Don\'t Specify', 'Feeding','Transportation','Others'])
        date_added = st.date_input(label="Date: ")
        description = st.text_area(label="Description (Optional):", placeholder="Enter a comment here ...")
        
        submit_button = st.form_submit_button(label="Submit Expense Details")
        
        if submit_button:
            # check if all mandatory field has been filled
            if not title:
                st.warning("Field Cannot be Empty.")
                st.stop()
                
            
            try:
                expense = Expense(
                              title=title, 
                              amount=amount, 
                              paid_to=paid_to, 
                              category=category,
                              date_added=date_added, 
                              description=description)
                
                # add to database
                session.add(expense)
                session.commit()
                st.success("Data Added Successfully.")
            except Exception as e:
                st.error(f"Some error occured {e}")


def delete_expense():
    st.markdown(" ### Delete Expense 📝")    
    # delete expenses form
    with st.form(key="delete_expense", clear_on_submit=True):
        expense_id = st.text_input(label="Enter Expense ID:")
        submit_button = st.form_submit_button(label="Delete Expense")
        
        if submit_button:
            # search for expense id
            expense = session.query(Expense).get(expense_id)
            
            if expense != None:
                session.delete(expense)
                session.commit()
                st.success("Record Deleted Successfully.")
            else:
                st.error("No Record Found!")
        
        

def edit_expense():
    st.markdown(" ### Edit Expense 📝")    
    # edit expenses form
    expense_id = st.text_input(label="Enter Expense ID:")
    search_btn = st.button(label="Search ID")
        
    if search_btn:
        try:
            # search for expense id
            expense = session.query(Expense).get(expense_id)
            
            if expense != None:
                # display form
                with st.form(key="update_expense", clear_on_submit=True):
                    title = st.text_input(label="Expense Title:", value=expense.title)
                    amount = st.number_input(label="Expense Amount:",value=expense.amount)
                    paid_to = st.text_input(label="Paid To:", value=expense.paid_to)
                    category = st.selectbox(label="Expense Category:", 
                                            options=['Don\'t Specify', 'Feeding','Transportation','Others'],
                                            placeholder =expense.category)
                    description = st.text_area(label="Description (Optional):", value=expense.description)
                    
                    submit_button = st.form_submit_button(label="Update Expense")
                    
                    if submit_button:
                        # check if all mandatory field has been filled
                        if not title:
                            st.warning("Field Cannot be Empty.")
                            st.stop()
                        
                        expense.title = title
                        expense.amount = amount
                        expense.paid_to = paid_to
                        expense.category = category,
                        expense.description = description
                        expense.updated_at = datetime.utcnow()
                        
                        session.commit()
                        st.success("Data Updated Successfully.")
            else:
                st.error("No Record Found!")
        except Exception as e:
            st.error(f"Some error occured {e}")
        
                
        

def list_expenses():
    """
    Display all expenses in a dataframe
    """

    st.subheader("Expenses Dataframe 📝")  
    all_expenses = session.query(Expense).all()
    
    df = pd.DataFrame({
                "ID": [expense.id for expense in all_expenses],
                "Title": [expense.title for expense in all_expenses],
                "Amount": [expense.amount for expense in all_expenses],
                "Paid To": [expense.paid_to for expense in all_expenses],
                "Category": [expense.category for expense in all_expenses],
                "Date": [expense.date_added for expense in all_expenses],
                "Description": [expense.description for expense in all_expenses],
                "Created At": [expense.created_at for expense in all_expenses],
                "Updated At": [expense.updated_at for expense in all_expenses],
            })
            
    st.dataframe(df, hide_index=True, use_container_width=True)


