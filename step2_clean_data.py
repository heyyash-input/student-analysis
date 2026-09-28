# STEP 2: Clean the messy data using pandas
# Real-world data is never perfect. Here we fix two common problems:
#   1) Duplicate rows   -> remove them
#   2) Missing values   -> fill them with a sensible value

import pandas as pd

df = pd.read_csv("students_raw.csv")

print("BEFORE cleaning")
print("Rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())
print("Missing attendance values:", df["attendance"].isnull().sum())

# 1) Remove duplicate rows
df = df.drop_duplicates()

# 2) Fill missing attendance with the median (middle value)
#    We use median instead of average because it is not affected by extreme values
median_attendance = df["attendance"].median()
df["attendance"] = df["attendance"].fillna(median_attendance)
df["attendance"] = df["attendance"].astype(int)  # back to whole numbers

print("\nAFTER cleaning")
print("Rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())
print("Missing attendance values:", df["attendance"].isnull().sum())
print("Filled missing attendance with median:", median_attendance)

df.to_csv("students_clean.csv", index=False)
print("\nSaved students_clean.csv")
