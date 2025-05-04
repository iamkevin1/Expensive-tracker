import streamlit as st
import pandas as pd
from datetime import datetime

# Load or initialize data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("expenses.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Member", "Category", "Amount", "Notes"])

def save_data(df):
    df.to_csv("expenses.csv", index=False)

st.title("👨‍👩‍👧‍👦 Family Expense Tracker")

# Add Expense Form
st.header("➕ Add New Expense")
with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    member = st.selectbox("Family Member", ["Dad", "Mom", "Kid1", "Kid2"])
    category = st.selectbox("Category", ["Food", "Transport", "School", "Utilities", "Entertainment", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    notes = st.text_input("Notes (optional)")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_data = pd.DataFrame([{
        "Date": date,
        "Member": member,
        "Category": category,
        "Amount": amount,
        "Notes": notes
    }])
    df = load_data()
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.success("Expense added successfully!")

# Expense Table
st.header("📄 All Expenses")
df = load_data()
st.dataframe(df)

# Summary
st.header("📊 Summary")
if not df.empty:
    total = df["Amount"].sum()
    per_member = df.groupby("Member")["Amount"].sum()
    per_category = df.groupby("Category")["Amount"].sum()

    st.metric("Total Expenses", f"${total:.2f}")
    st.bar_chart(per_member)
    st.bar_chart(per_category)
else:
    st.info("No expenses yet. Add some using the form above!")

