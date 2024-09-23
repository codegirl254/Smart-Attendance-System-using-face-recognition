import pandas as pd
import os
from datetime import datetime

def mark_attendance(name, class_type):
    # Select the correct file based on the class type
    if class_type == "Cyber Security":
        file_name = "cyber_security_attendance.xlsx"
    elif class_type == "Data Analytics":
        file_name = "data_analytics_attendance.xlsx"
    else:
        file_name = "instructors_attendance.xlsx"

    # Load existing attendance if file exists
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
    else:
        df = pd.DataFrame(columns=["Name"])  # Initial empty DataFrame with "Name" as the only column

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    # If the date column for today doesn't exist, add it
    if date_string not in df.columns:
        df[date_string] = None

    # Check if the name already exists in the DataFrame
    if name in df["Name"].values:
        # Check if the attendance for today has already been marked
        existing_time = df.loc[df["Name"] == name, date_string].values[0]
        if pd.notna(existing_time):
            return f"Attendance for {name} has already been marked today at {existing_time}."
        else:
            # Update the existing row with the time for the current date
            df.loc[df["Name"] == name, date_string] = time_string
            return f"Attendance for {name} has been updated for today."
    else:
        # Add a new row for the new attendee and mark attendance
        new_row = pd.DataFrame({"Name": [name], date_string: [time_string]})
        df = pd.concat([df, new_row], ignore_index=True)  # Replacing append with pd.concat

    # Save the updated DataFrame to the Excel file
    df.to_excel(file_name, index=False)
    return f"Attendance marked for {name}."
