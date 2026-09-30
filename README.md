# Student Result Predictor – A Mini Data Pipeline

A small Data Science project that takes raw student data, cleans it, stores it in a
SQL database, analyses it with SQL, and trains a Machine Learning model to predict
whether a student will **Pass** or **Fail**.

## The Pipeline

```
Step 1: Generate data  ->  Step 2: Clean (pandas)  ->  Step 3: Store + analyse (SQL)  ->  Step 4: Predict (ML)
   students_raw.csv          students_clean.csv            students.db                     accuracy + prediction
```

| File | What it does |
|---|---|
| `step1_generate_data.py` | Creates 300 students with some messy data (missing values, duplicates) |
| `step2_clean_data.py` | Removes duplicates, fills missing attendance with the median |
| `step3_sql_analysis.py` | Saves data into SQLite and answers 5 questions using SQL |
| `step4_train_model.py` | Trains a Logistic Regression model and tests its accuracy |

| `app.py` | **Frontend** – a web dashboard that shows the results and lets you predict live |

**Tools used:** Python, pandas, SQL (SQLite), scikit-learn, Streamlit

## How to Run (VS Code)

1. Open VS Code -> **File -> Open Folder** -> choose `V4C.ai`
2. Press `Ctrl+Shift+P` -> type **Python: Select Interpreter** -> choose the one with `.venv`
3. Open each file in order (step1 -> step4) and click the **Run ▶** button at the top right

Or run from the VS Code terminal:
```
.venv\Scripts\python.exe step1_generate_data.py
.venv\Scripts\python.exe step2_clean_data.py
.venv\Scripts\python.exe step3_sql_analysis.py
.venv\Scripts\python.exe step4_train_model.py
```

## Run the Frontend (Dashboard)

Run steps 1–3 first (they create `students.db`). Then in the VS Code terminal:
```
.venv\Scripts\streamlit.exe run app.py
```
Open **http://localhost:8501** in your browser. Press `Ctrl+C` in the terminal to stop it.

The dashboard has 4 parts:
1. **Summary numbers** – total students, pass rate, model accuracy
2. **Charts** – average marks by attendance, pass vs fail (each chart's data comes from a SQL query – click "See the SQL")
3. **Predict** – move 3 sliders, the model predicts Pass/Fail instantly with a confidence %
4. **Data table** – see all 300 students

Settings are in `.streamlit/config.toml` – the app only runs on this computer (`localhost`) and sends no usage data.

## Results

- Cleaning: 305 rows -> 300 rows (5 duplicates removed, 10 missing values filled)
- SQL finding: students with High attendance (75%+) scored **60.7** on average vs **53.2** for Low attendance
- SQL finding: 84 out of 88 students who study more than 7 hours passed
- ML model accuracy: **85%** on test data
