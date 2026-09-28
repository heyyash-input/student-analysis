# STEP 3: Store the clean data in a SQL database and ask questions with SQL
# SQLite is a small database that lives in a single file (students.db).
# It comes built into Python, so no extra installation is needed.

import sqlite3
import pandas as pd

df = pd.read_csv("students_clean.csv")

# Connect to the database file (it is created if it doesn't exist)
conn = sqlite3.connect("students.db")

# Save the table into the database. "replace" = overwrite if it already exists
df.to_sql("students", conn, if_exists="replace", index=False)
print("Saved", len(df), "students into students.db (table: students)\n")

# Our business questions, answered with SQL
questions = {
    "Q1. How many students passed and failed?": """
        SELECT result, COUNT(*) AS total_students
        FROM students
        GROUP BY result
    """,

    "Q2. What is the average final marks in each department?": """
        SELECT department, ROUND(AVG(final_marks), 1) AS avg_marks
        FROM students
        GROUP BY department
        ORDER BY avg_marks DESC
    """,

    "Q3. Who are the top 5 students?": """
        SELECT student_id, department, final_marks
        FROM students
        ORDER BY final_marks DESC
        LIMIT 5
    """,

    "Q4. Does attendance matter? (75% or more = High)": """
        SELECT
            CASE WHEN attendance >= 75 THEN 'High' ELSE 'Low' END AS attendance_level,
            COUNT(*) AS total_students,
            ROUND(AVG(final_marks), 1) AS avg_marks
        FROM students
        GROUP BY attendance_level
    """,

    "Q5. How many students study more than 7 hours, and how many of them passed?": """
        SELECT result, COUNT(*) AS total_students
        FROM students
        WHERE study_hours > 7
        GROUP BY result
    """,
}

for question, query in questions.items():
    print(question)
    answer = pd.read_sql_query(query, conn)
    print(answer.to_string(index=False))
    print()

conn.close()
