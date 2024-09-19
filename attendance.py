import pandas as pd
import os
from datetime import datetime


def mark_attendance(name):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    
    if os.path.exists("attendance.xlsx"):
               df = pd.read_excel("attendance.xlsx")
    else:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    # Check if the name is already in the attendance list for today
    if not any((df["Name"] == name) & (df["Date"] == date_string)):
        # Append the new attendance record
        df = df.append({"Name": name, "Date": date_string, "Time": time_string}, ignore_index=True)

    # Save the updated DataFrame to the Excel file
    df.to_excel("attendance.xlsx", index=False)

