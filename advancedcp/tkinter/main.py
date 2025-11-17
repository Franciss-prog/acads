import tkinter as tk
from tkinter import messagebox

# Dictionary to store user accounts temporarily
users = {}


# Function to switch to Register window
def open_register():
    login_window.destroy()
    register_window()


# Function to switch to Login window
def open_login():
    reg_window.destroy()
    login_page()


# ---------------------- LOGIN PAGE ----------------------
def login_page():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login Form")
    login_window.geometry("350x250")
    login_window.config(bg="gray")

    tk.Label(
        login_window,
        text="User Login",
        font=("Arial", 18, "bold"),
    ).pack(pady=10)
    tk.Label(login_window, text="Username:", font=("Arial", 12)).pack()
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", font=("Arial", 12)).pack()
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        elif username == "" or password == "":
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(
        login_window, text="Login", command=login, bg="black", fg="white", width=10
    ).pack(pady=10)
    tk.Button(
        login_window,
        text="Register",
        command=open_register,
        bg="black",
        fg="white",
        width=10,
    ).pack()
    tk.Button(
        login_window,
        text="Exit",
        command=login_window.destroy,
        bg="red",
        fg="white",
        width=10,
    ).pack(pady=5)

    login_window.mainloop()


# ---------------------- REGISTER PAGE ----------------------
def register_window():
    global reg_window
    reg_window = tk.Tk()
    reg_window.title("Register Account")
    reg_window.geometry("350x250")
    reg_window.config(bg="gray")

    tk.Label(
        reg_window,
        text="Register New User",
        font=("Arial", 18, "bold"),
    ).pack(pady=10)
    tk.Label(
        reg_window, text="New Username:", bg="lightyellow", font=("Arial", 12)
    ).pack()
    new_user_entry = tk.Entry(reg_window, width=30)
    new_user_entry.pack(pady=5)

    tk.Label(
        reg_window, text="New Password:", bg="lightyellow", font=("Arial", 12)
    ).pack()
    new_pass_entry = tk.Entry(reg_window, show="*", width=30)
    new_pass_entry.pack(pady=5)

    def register():
        new_user = new_user_entry.get()
        new_pass = new_pass_entry.get()

        if new_user == "" or new_pass == "":
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        elif new_user in users:
            messagebox.showerror("Error", "Username already exists!")
        else:
            users[new_user] = new_pass
            messagebox.showinfo("Success", "Account created successfully!")
            reg_window.destroy()
            login_page()

    tk.Button(
        reg_window, text="Register", command=register, bg="green", fg="white", width=10
    ).pack(pady=10)
    tk.Button(
        reg_window,
        text="Back to Login",
        command=open_login,
        bg="blue",
        fg="white",
        width=12,
    ).pack()
    tk.Button(
        reg_window,
        text="Exit",
        command=reg_window.destroy,
        bg="red",
        fg="white",
        width=10,
    ).pack(pady=5)

    reg_window.mainloop()


# ---------------------- RUN THE APP ----------------------
login_page()
tk.tk
