import tkinter as tk
from tkinter import messagebox, simpledialog
from face_recognition_utils import recognize_faces, load_known_faces
from attendance import mark_attendance

# Global variable to store selected class
selected_class = None

# Function to start face recognition after class selection
def start_recognition():
    global selected_class
    if selected_class:
        known_faces, known_names = load_known_faces(selected_class)
        recognized_name = recognize_faces(known_faces, known_names)
        if recognized_name:
            # Capture the message from mark_attendance
            message = mark_attendance(recognized_name, selected_class)
            recognized_label.config(text=message)
            attendance_log.insert(tk.END, f"{message}\n")
        else:
            recognized_label.config(text="No face recognized.")
    else:
        messagebox.showwarning("No Class Selected", "Please select a class first!")

# Function to manually add attendance
def add_attendance():
    global selected_class
    name = simpledialog.askstring("Input", "Enter name to add:")
    if name:
        # Capture the message from mark_attendance
        message = mark_attendance(name, selected_class)
        attendance_log.insert(tk.END, f"{message}\n")
        messagebox.showinfo("Attendance", message)

# Function to handle class selection and go to attendance page
def select_class(selected):
    global selected_class
    selected_class = selected
    class_label.config(text=f"Selected Class: {selected_class}")
    show_attendance_page()

# Function to show the class selection page
def show_class_selection_page():
    for widget in root.winfo_children():
        widget.pack_forget()
    
    title_label = tk.Label(root, text="Select Your Class", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=20)
    
    cyber_button = tk.Button(root, text="Cyber Security", command=lambda: select_class("Cyber Security"), font=("Helvetica", 12))
    cyber_button.pack(pady=10)
    
    data_button = tk.Button(root, text="Data Analytics", command=lambda: select_class("Data Analytics"), font=("Helvetica", 12))
    data_button.pack(pady=10)

    instructor_button = tk.Button(root, text="Instructor", command=lambda: select_class("Instructor"), font=("Helvetica", 12))
    instructor_button.pack(pady=10)

# Function to show the attendance page after class selection
def show_attendance_page():
    for widget in root.winfo_children():
        widget.pack_forget()

    # Display selected class
    class_label.pack(pady=10)

    # Face recognition start button
    start_button.pack(pady=10)

    # Manual attendance marking button
    add_button.pack(pady=5)

    # Label for recognized names
    recognized_label.pack(pady=10)

    # Attendance log area
    attendance_log.pack(pady=10)

    # Button to go back to class selection
    back_button.pack(pady=10)

# Main window setup
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Aesthetic improvements
root.geometry("500x400")
root.configure(bg="#f0f0f0")

# Widgets for attendance page
class_label = tk.Label(root, text="Selected Class: None", font=("Helvetica", 14, "italic"))

start_button = tk.Button(root, text="Start Face Recognition", command=start_recognition, font=("Helvetica", 12))
add_button = tk.Button(root, text="Add Attendance Manually", command=add_attendance, font=("Helvetica", 12))
recognized_label = tk.Label(root, text="Recognized: None", font=("Helvetica", 12))

attendance_log = tk.Text(root, height=10, width=50, font=("Helvetica", 10))

back_button = tk.Button(root, text="Back to Class Selection", command=show_class_selection_page, font=("Helvetica", 12))

# Start the GUI with class selection page
show_class_selection_page()

# Start the main loop
root.mainloop()
