"""
join.py — Step 2 of the pipeline: bring the roster onto the timesheet.

The timesheet knows *who worked and how long*. The roster knows *what each
person is paid*. Neither file can produce a paycheck on its own, so the pipeline
has to combine them — and the two files have different **grains**: one row per
week-of-work versus one row per person. That is exactly what `pd.merge` is for.
"""

import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return the timesheet with every roster column added to each row.

    Given the (already cleaned) timesheet and the (already cleaned) roster,
    return one row **per timesheet row** with that employee's roster columns —
    `first_name`, `last_name`, `department`, `hourly_rate`, `hourly_rate_usd` —
    filled in beside the timesheet columns.

    Every timesheet row survives, even one whose employee_id is not on the
    roster (NaN for the roster columns). Rostered people who did not work this
    week do not appear.
    """
    return pd.merge(timesheet, employees, on="employee_id", how="left")


if __name__ == "__main__":
    from extract import load_employees, load_timesheet
    import os

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
    timesheet = load_timesheet(os.path.join(data_dir, "timesheet_test.csv"))
    employees = load_employees()
    merged = merge_employees(timesheet, employees)
    print(merged)
    