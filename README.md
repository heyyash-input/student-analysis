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

## How to Explain It (30 seconds)

> "I built a small data pipeline in Python. First I generated a student dataset with
> some messy data on purpose. Then I cleaned it using pandas – removed duplicates and
> filled missing values with the median. Next I stored it in a SQLite database and used
> SQL queries like GROUP BY and CASE WHEN to find insights, for example that students with
> high attendance score about 7 marks more. Finally I trained a Logistic Regression model
> using study hours, attendance and previous marks to predict Pass or Fail, and it got
> 85% accuracy on test data."

## Questions You May Be Asked

**Q: Why did you fill missing values with the median and not the average?**
The median is the middle value, so a few very high or very low numbers don't pull it up or down.

**Q: Why didn't you use `final_marks` as an input to the model?**
Pass/Fail is decided directly from final marks. Using it would be like giving the model the
answer sheet – it would look perfect but be useless in real life. This problem is called **data leakage**.

**Q: Why Logistic Regression?**
It is a simple model made for Yes/No (two-class) predictions, and it is easy to explain.

**Q: Why split the data into train and test?**
To check the model on data it has never seen. Testing on the same data it learned from
would be like giving students the exact exam questions beforehand.

**Q: Is 85% accuracy good?**
About 69% of students passed, so a "dumb" model that always says "Pass" would get 69%.
Our model gets 85%, so it has clearly learned something useful.

**Q: Is this real data?**
No – I generated it myself to practise the full pipeline end to end. The next step would
be to apply the same steps to a real dataset.

**Q: How would you improve it?**
Use real data, add more features, try other models like a Decision Tree, and add a
GenAI feature where you can ask questions in plain English and an LLM writes the SQL.

## Frontend Questions You May Be Asked

**Q: Why Streamlit and not HTML/Flask?**
Streamlit lets me build a web page using only Python, so I could focus on the data and the model
instead of HTML, CSS and JavaScript. It is widely used in Data Science to share results quickly.

**Q: How does Streamlit work?**
Every time the user moves a slider, Streamlit runs the whole Python file again from top to bottom
and redraws the page with the new values.

**Q: Then does the model train again every time a slider moves?**
No. I used `@st.cache_resource`, which trains the model once and remembers it. Without it, the
app would retrain on every slider move and feel slow.

**Q: What does "87% confident" mean?**
Logistic Regression gives a probability for each answer. I show the probability of the predicted
answer. Close to 50% means the model is unsure; close to 100% means it is very sure.
