import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from attendance import mark_attendance, remove_attendance, download_excel
from face_recognition_utils import load_known_faces, recognize_faces
import os
import shutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variable to store selected class
selected_class = None

# Function to handle instructor login and interface
def show_instructor_interface():
    username = simpledialog.askstring("Login", "Enter Instructor Username:")
    password = simpledialog.askstring("Password", "Enter Instructor Password:", show="*")
    
    if username == "instructor" and password == "1234":
        show_instructor_dashboard()
    else:
        messagebox.showerror("Error", "Invalid login credentials.")

# Function to handle instructor actions
def show_instructor_dashboard():
    global selected_class
    
    for widget in root.winfo_children():
        widget.pack_forget()

    class_label = tk.Label(root, text="Select the Class to Manage", font=("Helvetica", 20, "bold"))
    class_label.pack(pady=20)

    # Frame for Class Selection
    class_frame = tk.Frame(root)
    class_frame.pack(pady=20)

    # Buttons for Class Selection
    cyber_button = tk.Button(class_frame, text="Cyber Security", command=lambda: select_class_for_instructor("Cyber Security"), font=("Helvetica", 14), width=20)
    cyber_button.grid(row=0, column=0, padx=10, pady=10)

    data_button = tk.Button(class_frame, text="Data Analytics", command=lambda: select_class_for_instructor("Data Analytics"), font=("Helvetica", 14), width=20)
    data_button.grid(row=0, column=1, padx=10, pady=10)

    back_button = tk.Button(root, text="Back to Main Menu", command=show_main_menu, font=("Helvetica", 12), bg="lightgray")
    back_button.pack(pady=20)

def select_class_for_instructor(class_type):
    global selected_class
    selected_class = class_type
    for widget in root.winfo_children():
        widget.pack_forget()

    class_label = tk.Label(root, text=f"Instructor Interface for {class_type}", font=("Helvetica", 20, "bold"))
    class_label.pack(pady=20)

    # Frame for Instructor Actions
    action_frame = tk.Frame(root)
    action_frame.pack(pady=20)

    # Button to add attendance manually
    add_button = tk.Button(action_frame, text="Add Attendance Manually", command=add_attendance, font=("Helvetica", 14), bg="#4CAF50", fg="white", width=25)
    add_button.grid(row=0, column=0, padx=10, pady=10)

    # Button to remove attendance manually
    remove_button = tk.Button(action_frame, text="Remove Attendance", command=remove_attendance_manual, font=("Helvetica", 14), bg="#f44336", fg="white", width=25)
    remove_button.grid(row=1, column=0, padx=10, pady=10)

    # Button to download attendance Excel file
    download_button = tk.Button(action_frame, text="Download Attendance Sheet", command=lambda: download_attendance(class_type), font=("Helvetica", 14), bg="#2196F3", fg="white", width=25)
    download_button.grid(row=2, column=0, padx=10, pady=10)

    back_button = tk.Button(root, text="Back", command=show_instructor_dashboard, font=("Helvetica", 12), bg="lightgray")
    back_button.pack(pady=20)

# Function to manually add attendance
def add_attendance():
    global selected_class
    name = simpledialog.askstring("Input", "Enter student name:")
    if name:
        message = mark_attendance(name, selected_class)
        messagebox.showinfo("Attendance", message)

# Function to remove attendance manually
def remove_attendance_manual():
    global selected_class
    name = simpledialog.askstring("Input", "Enter student name to remove:")
    if name:
        message = remove_attendance(name, selected_class)
        messagebox.showinfo("Remove Attendance", message)

# Function to download the attendance sheet
def download_attendance(class_type):
    file_name = download_excel(class_type)
    if file_name and os.path.exists(file_name):
        save_location = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=file_name)
        if save_location:
            shutil.copy(file_name, save_location)
            messagebox.showinfo("Success", f"Attendance file saved to {save_location}")
    else:
        messagebox.showerror("Error", "Attendance file not found.")

# Function to handle admin login and interface
def show_admin_interface():
    username = simpledialog.askstring("Login", "Enter Admin Username:")
    password = simpledialog.askstring("Password", "Enter Admin Password:", show="*")
    
    if username == "admin" and password == "admin123":
        show_admin_dashboard()
    else:
        messagebox.showerror("Error", "Invalid admin credentials.")

# Function for the admin dashboard where they can download attendance
# Function to show the admin dashboard with report and download options
def show_admin_dashboard():
    for widget in root.winfo_children():
        widget.pack_forget()

    dashboard_label = tk.Label(root, text="Admin Dashboard", font=("Helvetica", 20, "bold"), bg="#3F51B5", fg="white")
    dashboard_label.pack(pady=20, fill=tk.X)

    # Frame for reports and downloads
    report_frame = tk.Frame(root, padx=20, pady=20)
    report_frame.pack(pady=20)

    # Section label for Downloads
    downloads_label = tk.Label(report_frame, text="Download Attendance", font=("Helvetica", 16, "bold"))
    downloads_label.pack(pady=10)

    # Button to download attendance for Cyber Security
    cyber_button = tk.Button(report_frame, text="Download Cyber Security Attendance", command=lambda: download_attendance("Cyber Security"), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=30)
    cyber_button.pack(pady=5)

    # Button to download attendance for Data Analytics
    data_button = tk.Button(report_frame, text="Download Data Analytics Attendance", command=lambda: download_attendance("Data Analytics"), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=30)
    data_button.pack(pady=5)

    # Section label for Reports
    reports_label = tk.Label(report_frame, text="Reports", font=("Helvetica", 16, "bold"))
    reports_label.pack(pady=10)

    # Button to view attendance chart
    view_chart_button = tk.Button(report_frame, text="View Attendance Chart", command=show_attendance_chart, font=("Helvetica", 14), bg="#FF9800", fg="white", width=30)
    view_chart_button.pack(pady=5)

    # Back button
    back_button = tk.Button(root, text="Back to Main Menu", command=show_main_menu, font=("Helvetica", 12), bg="#F44336", fg="white", width=20)
    back_button.pack(pady=20)

# Function to show attendance chart using Matplotlib
def show_attendance_chart():
    # Sample data for demonstration purposes
    classes = ['Cyber Security', 'Data Analytics']
    attendance_counts = [30, 25]  # You should replace this with actual data from your attendance records

    plt.figure(figsize=(8, 5))
    plt.bar(classes, attendance_counts, color=['blue', 'orange'])
    plt.title('Attendance Counts by Class')
    plt.xlabel('Classes')
    plt.ylabel('Number of Students Attended')
    plt.grid(axis='y')
    plt.show()

def view_full_report():
    # Placeholder for viewing reports logic
    messagebox.showinfo("Report", "This feature will display the full attendance report.")

# Function to show the student mode interface
def show_student_mode():
    global selected_class
    for widget in root.winfo_children():
        widget.pack_forget()

    class_label = tk.Label(root, text="Select Your Class", font=("Helvetica", 16, "bold"))
    class_label.pack(pady=20)

    cyber_button = tk.Button(root, text="Cyber Security", command=lambda: select_class_for_student("Cyber Security"), font=("Helvetica", 12))
    cyber_button.pack(pady=10)

    data_button = tk.Button(root, text="Data Analytics", command=lambda: select_class_for_student("Data Analytics"), font=("Helvetica", 12))
    data_button.pack(pady=10)

    back_button = tk.Button(root, text="Back to Main Menu", command=show_main_menu, font=("Helvetica", 12))
    back_button.pack(pady=20)

# Enhanced function for the student to select a class and scan face
def select_class_for_student(class_type):
    global selected_class
    selected_class = class_type
    for widget in root.winfo_children():
        widget.pack_forget()

    class_label = tk.Label(root, text=f"Face Scan for {class_type}", font=("Helvetica", 16, "bold"))
    class_label.pack(pady=20)

    scan_button = tk.Button(root, text="Scan Face", command=lambda: enhance_scan_face_interface(class_type), font=("Helvetica", 12))
    scan_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=show_student_mode, font=("Helvetica", 12))
    back_button.pack(pady=20)

def enhance_scan_face_interface(class_type):
    global selected_class
    selected_class = class_type
    faces_encoded, known_face_names = load_known_faces()  # Load known faces and names from your database
    recognized_name = recognize_faces(faces_encoded, known_face_names)

    if recognized_name:
        message = mark_attendance(recognized_name, selected_class)
        messagebox.showinfo("Attendance", message)
    else:
        messagebox.showwarning("Warning", "Face not recognized. Attendance not marked.")

# Function to show the main menu
def show_main_menu():
    for widget in root.winfo_children():
        widget.pack_forget()

    title_label = tk.Label(root, text="Attendance Management System", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=20)

    student_button = tk.Button(root, text="Student Mode", command=show_student_mode, font=("Helvetica", 14), bg="#4CAF50", fg="white", width=25)
    student_button.pack(pady=10)

    instructor_button = tk.Button(root, text="Instructor Login", command=show_instructor_interface, font=("Helvetica", 14), bg="#2196F3", fg="white", width=25)
    instructor_button.pack(pady=10)

    admin_button = tk.Button(root, text="Admin Login", command=show_admin_interface, font=("Helvetica", 14), bg="#F44336", fg="white", width=25)
    admin_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Helvetica", 12), bg="lightgray")
    quit_button.pack(pady=20)

# Main GUI setup
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("600x500")

show_main_menu()

root.mainloop()
