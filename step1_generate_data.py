# STEP 1: Create a sample dataset of students
# We make our own data so we don't need to download anything.
# The data is a bit "messy" on purpose (missing values + duplicates)
# so that Step 2 has something real to clean.

import random
import pandas as pd

random.seed(42)  # fixed seed = same data every time we run this file

departments = ["CSE", "IT", "AI"]
rows = []

for student_id in range(1, 301):  # 300 students
    study_hours = round(random.uniform(0, 10), 1)   # hours per day
    attendance = random.randint(40, 100)            # percentage
    previous_marks = random.randint(30, 100)        # last exam marks

    # Final marks depend on the 3 values above, plus a little randomness
    final_marks = (0.4 * previous_marks) + (3 * study_hours) + (0.2 * attendance) + random.randint(-10, 10)
    final_marks = max(0, min(100, round(final_marks)))  # keep between 0 and 100

    result = "Pass" if final_marks >= 50 else "Fail"

    rows.append({
        "student_id": student_id,
        "department": random.choice(departments),
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_marks": previous_marks,
        "final_marks": final_marks,
        "result": result,
    })

df = pd.DataFrame(rows)

# Make the data messy on purpose
# 1) Remove attendance for 10 random students (missing values)
missing_rows = random.sample(range(len(df)), 10)
df.loc[missing_rows, "attendance"] = None

# 2) Copy 5 students again (duplicate rows)
df = pd.concat([df, df.sample(5, random_state=42)])

df.to_csv("students_raw.csv", index=False)

print("Created students_raw.csv")
print("Total rows:", len(df))
print(df.head().to_string())
