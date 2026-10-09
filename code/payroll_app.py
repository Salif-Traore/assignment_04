"""payroll_app.py - the weekly payroll, for someone who has never opened a terminal."""

import streamlit as st

from payroll.compute import build_payroll, payroll_export
from payroll.extract import load_employees, load_timesheet

st.title("Salt City Coffee - Weekly Payroll")
st.write("Upload the week's timesheet to see totals and download the payroll file.")

roster = load_employees()

uploaded_file = st.file_uploader(
    "Upload timesheet CSV:",
    key="timesheet",
)

if uploaded_file:
    timesheet = load_timesheet(uploaded_file)
    payroll = build_payroll(timesheet, roster)

    payroll_date = payroll["payroll_date"].iloc[0]
    st.subheader(f"Pay period: {payroll_date}")

    paid = payroll[payroll["pay_type"] != "unmatched"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees paid", len(paid))
    col2.metric("Total hours", payroll["hours_worked"].sum())
    col3.metric("Total gross pay", f"${payroll['gross_pay'].sum():,.2f}")
    col4.metric("Overtime weeks", len(payroll[payroll["pay_type"] == "overtime"]))

    unmatched = payroll[payroll["pay_type"] == "unmatched"]
    if len(unmatched) > 0:
        ids = ", ".join(unmatched["employee_id"])
        st.warning(f"Unmatched employee IDs (not on the roster): {ids}")
    else:
        st.success("Every row matched an employee on the roster.")

    st.dataframe(payroll)

    export = payroll_export(payroll)
    st.download_button(
        "Download payroll CSV for the provider",
        data=export.to_csv(index=False),
        file_name=f"payroll_{payroll_date}.csv",
        mime="text/csv",
        key="download",
    )
