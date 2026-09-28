# FRONTEND: One-page dashboard for the Student Result Predictor
# Streamlit turns a normal Python script into a web page.
# Important idea: every time you move a slider, Streamlit runs this whole file again from top to bottom.
#
# Run it with:  .venv\Scripts\streamlit.exe run app.py
# Then open:    http://localhost:8501

import os
import sqlite3
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Student Result Predictor", layout="wide")


# ---------- 1. Load the data from our database (made in Step 3) ----------
if not os.path.exists("students.db"):
    st.error("students.db not found. Please run step1, step2 and step3 first.")
    st.stop()


def run_sql(query):
    conn = sqlite3.connect("students.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


df = run_sql("SELECT * FROM students")


# ---------- 2. Train the model (same as Step 4) ----------
# @st.cache_resource = train only once and remember the model,
# instead of training again every time a slider moves
@st.cache_resource
def train_model(df):
    X = df[["study_hours", "attendance", "previous_marks"]]
    y = df["result"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return model, accuracy


model, accuracy = train_model(df)


# ---------- 3. Title ----------
st.title("Student Result Predictor")
st.caption("Raw data → pandas cleaning → SQLite database → SQL insights → ML prediction")


# ---------- 4. Summary numbers ----------
total_students = len(df)
pass_rate = (df["result"] == "Pass").mean() * 100

col1, col2, col3 = st.columns(3)
col1.metric("Students", total_students)
col2.metric("Pass rate", f"{pass_rate:.0f}%")
col3.metric("Model accuracy", f"{accuracy * 100:.0f}%")


# ---------- 5. Charts (the data for each chart comes from a SQL query) ----------
attendance_query = """
SELECT
    CASE WHEN attendance >= 75 THEN 'High (75%+)' ELSE 'Low (below 75%)' END AS attendance_level,
    ROUND(AVG(final_marks), 1) AS avg_marks
FROM students
GROUP BY attendance_level
"""

result_query = """
SELECT result, COUNT(*) AS total_students
FROM students
GROUP BY result
"""

left, right = st.columns(2)

with left:
    st.subheader("Average marks by attendance")
    st.bar_chart(run_sql(attendance_query), x="attendance_level", y="avg_marks",
                 x_label="Attendance", y_label="Average final marks")

with right:
    st.subheader("Pass vs fail")
    st.bar_chart(run_sql(result_query), x="result", y="total_students",
                 x_label="Result", y_label="Number of students", color="result")

with st.expander("See the SQL behind these charts"):
    st.code(attendance_query, language="sql")
    st.code(result_query, language="sql")


# ---------- 6. Predict for a new student ----------
st.divider()
st.subheader("Predict for a new student")
st.write("Move the sliders. The prediction updates instantly.")

c1, c2, c3 = st.columns(3)
study_hours = c1.slider("Study hours per day", 0.0, 10.0, 5.0, step=0.5)
attendance = c2.slider("Attendance (%)", 40, 100, 75)
previous_marks = c3.slider("Previous exam marks", 30, 100, 65)

new_student = pd.DataFrame({
    "study_hours": [study_hours],
    "attendance": [attendance],
    "previous_marks": [previous_marks],
})

prediction = model.predict(new_student)[0]
confidence = model.predict_proba(new_student).max() * 100  # how sure the model is

if prediction == "Pass":
    st.success(f"Prediction: PASS  ({confidence:.0f}% confident)")
else:
    st.error(f"Prediction: FAIL  ({confidence:.0f}% confident)")


# ---------- 7. Show the data ----------
with st.expander("See all student data"):
    st.dataframe(df)
