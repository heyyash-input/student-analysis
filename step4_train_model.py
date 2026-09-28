# STEP 4: Train a Machine Learning model to predict Pass / Fail
# Model used: Logistic Regression (a simple and popular model for Yes/No type answers)

import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Read the data from our database (output of Step 3)
conn = sqlite3.connect("students.db")
df = pd.read_sql_query("SELECT * FROM students", conn)
conn.close()

# Inputs (features) = what we know BEFORE the final exam
# We do NOT use final_marks, because Pass/Fail comes directly from it.
# Using it would be like giving the model the answer sheet.
X = df[["study_hours", "attendance", "previous_marks"]]

# Output (target) = what we want to predict
y = df["result"]

# Split: 80% data to train the model, 20% kept aside to test it
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Test the model on data it has never seen
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("\nModel accuracy on test data:", round(accuracy * 100, 1), "%")

# Show a few predictions next to the real answers
comparison = X_test.copy()
comparison["actual"] = y_test
comparison["predicted"] = predictions
print("\nSample predictions:")
print(comparison.head(5).to_string(index=False))

# Try the model on a brand new student
new_student = pd.DataFrame({
    "study_hours": [2.0],
    "attendance": [60],
    "previous_marks": [45],
})
print("\nNew student:", new_student.to_dict("records")[0])
print("Prediction:", model.predict(new_student)[0])
