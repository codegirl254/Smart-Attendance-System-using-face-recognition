import tkinter as tk
from tkinter import messagebox, simpledialog
from  face_recognition_utils import recognize_faces  # Import your face recognition function
from face_recognition_utils import load_known_faces
from attendance import mark_attendance  # Import your attendance function

# Function to start face recognition
def start_recognition():
    known_faces, known_names = load_known_faces()  # Load the known faces and names
    recognized_name = recognize_faces(known_faces, known_names)  # Pass the loaded data
    if recognized_name:
        mark_attendance(recognized_name)
        recognized_label.config(text=f"Recognized: {recognized_name}")
        attendance_log.insert(tk.END, f"Attendance marked for {recognized_name}\n")
    else:
        recognized_label.config(text="No face recognized.")

# Function to manually add attendance
def add_attendance():
    name = simpledialog.askstring("Input", "Enter name to add:")
    if name:
        mark_attendance(name)
        attendance_log.insert(tk.END, f"Attendance manually marked for {name}\n")
        messagebox.showinfo("Attendance", f"Attendance marked for {name}")

# Function to remove attendance (this is a placeholder; implement as needed)
def remove_attendance():
    name = simpledialog.askstring("Input", "Enter name to remove:")
    if name:
        # Implement logic to remove attendance from your records
        attendance_log.insert(tk.END, f"Attendance removed for {name}\n")
        messagebox.showinfo("Attendance", f"Attendance removed for {name}")

# Create the main window
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Create a button to start recognition
start_button = tk.Button(root, text="Start Face Recognition", command=start_recognition)
start_button.pack(pady=20)

# Label to display recognized names
recognized_label = tk.Label(root, text="Recognized: None")
recognized_label.pack(pady=10)

# Text area to log attendance records
attendance_log = tk.Text(root, height=10, width=50)
attendance_log.pack(pady=10)

# Button to manually
add_button = tk.Button(root, text="Add Attendance Manually", command=add_attendance)
add_button.pack(pady=5)

# Button to manually add attendance
remove_button = tk.Button(root, text="Remove Attendance", command=remove_attendance)
remove_button.pack(pady=5)

# Start the main loop
root.mainloop()