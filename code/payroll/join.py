"""join.py - Step 2 of the pipeline: bring the roster onto the timesheet."""

import os

import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return the timesheet with every roster column added to each row.

    Every timesheet row survives, even one whose employee_id is not on the
    roster (NaN for the roster columns). Rostered people who did not work this
    week do not appear.
    """
    return pd.merge(timesheet, employees, on="employee_id", how="left")


if __name__ == "__main__":
    from extract import load_employees, load_timesheet

    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "..", "..", "data")
    timesheet = load_timesheet(os.path.join(data_dir, "timesheet_test.csv"))
    employees = load_employees()
    merged = merge_employees(timesheet, employees)
    print(merged)
