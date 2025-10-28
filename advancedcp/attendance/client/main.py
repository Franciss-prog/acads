import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

# ----------------------
# Data
# ----------------------
AttendanceList = []


class Attendance:
    def __init__(self, srcode, name, time_in, time_out):
        self.srcode = srcode
        self.name = name
        self.time_in = time_in
        self.time_out = time_out


# ----------------------
# Utility Functions
# ----------------------
def get_current_time():
    return datetime.now().strftime("%I:%M %p")


def is_valid_srcode(srcode):
    return bool(re.match(r"^\d{2}-\d{5}$", srcode))


def is_valid_time(time_str):
    try:
        input_time = datetime.strptime(time_str, "%I:%M %p")
        if input_time < datetime.now():
            return False
        return True
    except ValueError:
        return False


# ----------------------
# Tkinter App
# ----------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Attendance System")
        self.geometry("450x350")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MenuPage, AddAttendancePage, AttendanceListPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "AttendanceListPage":
            frame.refresh_list()


# ----------------------
# Pages
# ----------------------
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Student Attendance Menu", font=("Arial", 16)).pack(pady=20)

        tk.Button(
            self,
            text="Show Attendance List",
            width=25,
            command=lambda: controller.show_frame("AttendanceListPage"),
        ).pack(pady=5)

        tk.Button(
            self,
            text="Add New Attendance",
            width=25,
            command=lambda: controller.show_frame("AddAttendancePage"),
        ).pack(pady=5)

        tk.Button(self, text="Exit", width=25, command=self.quit).pack(pady=20)


class AddAttendancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Add Student Attendance", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Name:").pack()
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack()

        tk.Label(self, text="SR-CODE (e.g., 24-45678):").pack()
        self.srcode_entry = tk.Entry(self, width=30)
        self.srcode_entry.pack()

        tk.Label(self, text="Time Out (HH:MM AM/PM):").pack()
        self.timeout_entry = tk.Entry(self, width=30)
        self.timeout_entry.pack()

        self.timein_label = tk.Label(self, text=f"Time In: {get_current_time()}")
        self.timein_label.pack(pady=5)

        tk.Button(self, text="Submit Attendance", command=self.submit).pack(pady=10)
        tk.Button(
            self, text="Back to Menu", command=lambda: controller.show_frame("MenuPage")
        ).pack()

    def submit(self):
        name = self.name_entry.get().strip()
        srcode = self.srcode_entry.get().strip()
        timeout = self.timeout_entry.get().strip()
        timein = get_current_time()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not is_valid_srcode(srcode):
            messagebox.showerror("Error", "Invalid SR-CODE format.")
            return
        if not is_valid_time(timeout):
            messagebox.showerror("Error", "Invalid or past time. Use HH:MM AM/PM.")
            return

        AttendanceList.append(Attendance(srcode, name, timein, timeout))
        messagebox.showinfo("Success", "Attendance Recorded!")
        self.name_entry.delete(0, tk.END)
        self.srcode_entry.delete(0, tk.END)
        self.timeout_entry.delete(0, tk.END)
        self.timein_label.config(text=f"Time In: {get_current_time()}")
        self.controller.show_frame("AttendanceListPage")


class AttendanceListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Attendance List", font=("Arial", 16)).pack(pady=10)
        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack(pady=5)
        tk.Button(
            self, text="Back to Menu", command=lambda: controller.show_frame("MenuPage")
        ).pack(pady=10)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        if not AttendanceList:
            self.listbox.insert(tk.END, "No records found.")
        for idx, att in enumerate(AttendanceList, start=1):
            self.listbox.insert(
                tk.END,
                f"{idx}. {att.srcode} | {att.name} | {att.time_in} -> {att.time_out}",
            )


# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
