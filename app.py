"""Job Application Tracker

A Streamlit app for logging job applications, tracking a weekly target
and seeing how many applications get a response.
"""

import sqlite3
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# Settings in one place so they're easy to change later
DB_PATH = "jobs.db"
WEEKLY_TARGET = 10
STATUSES = ["Applied", "Interview", "Offer", "Rejected"]


# Database functions

def get_connection():
    """Open a connection to the SQLite database file."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the applications table the first time the app runs."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                date_applied TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied'
            )
            """
        )


def add_application(company, role, date_applied):
    """Save a new application. The ? placeholders stop SQL injection."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO applications (company, role, date_applied, status) "
            "VALUES (?, ?, ?, 'Applied')",
            (company, role, date_applied.isoformat()),
        )


def update_status(app_id, new_status):
    """Change the status of one application."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (new_status, app_id),
        )


def load_applications():
    """Read every application into a pandas DataFrame, newest first."""
    with get_connection() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM applications ORDER BY date_applied DESC, id DESC",
            conn,
        )
    df["date_applied"] = pd.to_datetime(df["date_applied"])
    return df


# The page itself

st.set_page_config(page_title="Job Tracker")
init_db()

st.title("Job Application Tracker")

# Form to log a new application
with st.form("add_form", clear_on_submit=True):
    st.subheader("Log an application")
    company = st.text_input("Company")
    role = st.text_input("Role")
    date_applied = st.date_input("Date applied", value=date.today())
    submitted = st.form_submit_button("Add application")

    if submitted:
        if company.strip() and role.strip():
            add_application(company.strip(), role.strip(), date_applied)
            st.success(f"Added {role} at {company}")
        else:
            st.error("Fill in both company and role.")

df = load_applications()

# Stats: this week's count, total, and response rate
today = date.today()
week_start = today - timedelta(days=today.weekday())  # Monday of this week
this_week = df[df["date_applied"].dt.date >= week_start]

total = len(df)
responses = len(df[df["status"] != "Applied"])
response_rate = (responses / total * 100) if total else 0

col1, col2, col3 = st.columns(3)
col1.metric("This week", f"{len(this_week)} / {WEEKLY_TARGET}")
col2.metric("Total applications", total)
col3.metric("Response rate", f"{response_rate:.0f}%")
st.progress(min(len(this_week) / WEEKLY_TARGET, 1.0))

# Update a status
if total:
    st.subheader("Update a status")
    labels = {f"#{row.id} {row.company}, {row.role}": row.id for row in df.itertuples()}
    chosen = st.selectbox("Application", list(labels.keys()))
    new_status = st.selectbox("New status", STATUSES)
    if st.button("Update"):
        update_status(labels[chosen], new_status)
        st.rerun()

    # Full list
    st.subheader("All applications")
    display = df.copy()
    display["date_applied"] = display["date_applied"].dt.strftime("%d %b %Y")
    st.dataframe(display.drop(columns="id"), hide_index=True, width="stretch")
else:
    st.info("No applications yet. Add your first one above.")
