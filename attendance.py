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
        return "Invalid class type."

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

    # Ensure case-insensitive matching of names
    df['Name'] = df['Name'].str.lower()  # Convert all names in the DataFrame to lowercase
    name_lower = name.lower()  # Convert input name to lowercase

    # Check if the name already exists in the DataFrame
    if name_lower in df["Name"].values:
        # Check if the attendance for today has already been marked
        existing_time = df.loc[df["Name"] == name_lower, date_string].values[0]
        if pd.notna(existing_time):
            return f"Attendance for {name} has already been marked today at {existing_time}."
        else:
            # Update the existing row with the time for the current date
            df.loc[df["Name"] == name_lower, date_string] = time_string
            df.to_excel(file_name, index=False)  # Save the updated DataFrame
            return f"Attendance for {name} has been updated for today."
    else:
        # Add a new row for the new attendee and mark attendance
        new_row = pd.DataFrame({"Name": [name_lower], date_string: [time_string]})
        df = pd.concat([df, new_row], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    df.to_excel(file_name, index=False)
    return f"Attendance marked for {name}."

def remove_attendance(name, class_type):
    # Select the correct file based on the class type
    if class_type == "Cyber Security":
        file_name = "cyber_security_attendance.xlsx"
    elif class_type == "Data Analytics":
        file_name = "data_analytics_attendance.xlsx"
    else:
        return "Invalid class type."

    # Check if file exists
    if not os.path.exists(file_name):
        return "Attendance file not found."

    # Load the attendance data
    df = pd.read_excel(file_name)

    # Ensure case-insensitive matching of names
    df['Name'] = df['Name'].str.lower()  # Convert all names in the DataFrame to lowercase
    name_lower = name.lower()  # Convert input name to lowercase

    # Check if the name exists in the attendance
    if name_lower in df['Name'].values:
        # Remove the attendance entry
        df = df[df['Name'] != name_lower]
        df.to_excel(file_name, index=False)
        return f"Removed attendance for {name} from {class_type}."
    else:
        return f"{name} not found in {class_type} attendance."

def download_excel(class_type):
    # Select the correct file based on the class type
    if class_type == "Cyber Security":
        file_name = "cyber_security_attendance.xlsx"
    elif class_type == "Data Analytics":
        file_name = "data_analytics_attendance.xlsx"
    else:
        return None

    return file_name
