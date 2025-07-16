import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SORL Salary Calculator", layout="centered")
st.title("SORL Salary Calculator")

# Input layout
col1, col2 = st.columns(2)

with col1:
    basic_salary = st.number_input("Enter basic salary:", min_value=0)
    work_days = st.number_input("Enter number of work days:", min_value=0, max_value=31)
    overtime_days = st.number_input("Enter number of overtime days:", min_value=0, max_value=31)
    night_shifts = st.number_input("Enter number of night shifts:", min_value=0, max_value=31)

with col2:
    leave_days = st.number_input("Enter number of contract leave days:", min_value=0, max_value=31)
    overtime_hours = st.number_input("Enter number of overtime hours:", min_value=0)

if st.button("Calculate Salary"):
    daily_wage = float(basic_salary / 22)
    monthly_basic = work_days * daily_wage
    total_days_worked = work_days + overtime_days
    leave_allowance = daily_wage * leave_days
    risk_allowance = 10 * total_days_worked
    night_allowance = 10 * night_shifts

    attendance_bonus = 100 if total_days_worked >= 19 else 0

    allowance = risk_allowance + night_allowance + attendance_bonus + leave_allowance
    taxable_income = 0.945 * monthly_basic + allowance
    k = 730
    income_tax = 0.175 * (taxable_income - k) + 18.5

    overtime_per_hour = 1.5 * (basic_salary / 216)
    overtime = overtime_hours * overtime_per_hour
    half_basic = monthly_basic / 2

    if overtime <= half_basic:
        overtime_tax = 0.05 * overtime
    else:
        overtime_tax = 0.05 * half_basic + 0.10 * (overtime - half_basic)

    total_tax = income_tax + overtime_tax
    net_salary = taxable_income + overtime - total_tax

    # Display key metrics
    st.subheader("Salary Breakdown")
    col1, col2 = st.columns(2)
    col1.metric("Total Allowance", f"GHS {round(allowance, 2)}")
    col2.metric("Net Salary", f"GHS {round(net_salary, 2)}")
    col1.metric("Income Tax", f"GHS {round(income_tax, 2)}")
    col2.metric("Overtime Tax", f"GHS {round(overtime_tax, 2)}")

    # Prepare CSV content
    report = pd.DataFrame({
        "Item": [
            "Basic Salary", "Daily Wage", "Work Days", "Total Days Worked",
            "Leave Allowance", "Risk Allowance", "Night Allowance", "Attendance Bonus",
            "Total Allowance", "Monthly Basic (after deduction)",
            "Taxable Income", "Income Tax", "Overtime", "Overtime Tax", "Total Tax", "Net Salary"
        ],
        "Amount (GHS)": [
            basic_salary, round(daily_wage, 2), work_days, total_days_worked,
            round(leave_allowance, 2), round(risk_allowance, 2), round(night_allowance, 2), attendance_bonus,
            round(allowance, 2), round(0.945 * monthly_basic, 2),
            round(taxable_income, 2), round(income_tax, 2), round(overtime, 2),
            round(overtime_tax, 2), round(total_tax, 2), round(net_salary, 2)
        ]
    })

    csv_buffer = io.StringIO()
    report.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Salary Report",
        data=csv_buffer.getvalue(),
        file_name="salary_report.csv",
        mime="text/csv"
    )
