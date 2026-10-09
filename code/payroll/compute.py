"""compute.py - Step 3 of the pipeline: pay, labels, and the provider export."""

import pandas as pd

from .clean import add_hourly_rate, add_hours_worked
from .join import merge_employees

OVERTIME_THRESHOLD = 40.0
OVERTIME_MULTIPLIER = 1.5


def calc_gross_pay(hours, rate):
    """Gross pay for one employee-week, rounded to cents."""
    if pd.isna(rate):
        return 0.0
    if hours <= OVERTIME_THRESHOLD:
        return round(hours * rate, 2)
    regular_pay = OVERTIME_THRESHOLD * rate
    overtime_hours = hours - OVERTIME_THRESHOLD
    overtime_pay = overtime_hours * rate * OVERTIME_MULTIPLIER
    return round(regular_pay + overtime_pay, 2)


def classify_pay(hours, rate):
    """Return unmatched, overtime, or regular for one employee-week."""
    if pd.isna(rate):
        return "unmatched"
    if hours > OVERTIME_THRESHOLD:
        return "overtime"
    return "regular"


def add_gross_pay(payroll):
    """Return a copy with one new column, gross_pay, via row apply."""
    out = payroll.copy()
    out["gross_pay"] = out.apply(
        lambda row: calc_gross_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1,
    )
    return out


def add_pay_type(payroll):
    """Return a copy with one new column, pay_type, via row apply."""
    out = payroll.copy()
    out["pay_type"] = out.apply(
        lambda row: classify_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1,
    )
    return out


def build_payroll(timesheet, employees):
    """Raw timesheet and roster in, full payroll table out."""
    cleaned_timesheet = add_hours_worked(timesheet)
    cleaned_employees = add_hourly_rate(employees)
    merged = merge_employees(cleaned_timesheet, cleaned_employees)
    with_pay = add_gross_pay(merged)
    with_type = add_pay_type(with_pay)
    return with_type


def payroll_export(payroll):
    """A new frame shaped for the payroll provider: payable rows only."""
    payable = payroll[payroll["pay_type"] != "unmatched"]
    return pd.DataFrame({
        "payrolldate": payable["payroll_date"],
        "employeeid": payable["employee_id"],
        "hours": payable["hours_worked"],
        "rate": payable["hourly_rate_usd"],
        "total": payable["gross_pay"],
    })
