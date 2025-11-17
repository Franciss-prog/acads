import tkinter as tk
from tkinter import messagebox, ttk

# Create main window
window = tk.Tk()
window.title("Personal Information Form")
window.geometry("400x500")
window.config(bg="lightblue")


# ---------- Functions ----------
def submit_form():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    country = country_cb.get()
    comment = text_comment.get("1.0", "end-1c")

    hobbies = []
    if hobby_reading.get():
        hobbies.append("Reading")
    if hobby_sports.get():
        hobbies.append("Sports")
    if hobby_music.get():
        hobbies.append("Music")

    if name == "" or age == "" or gender == "" or country == "":
        messagebox.showwarning(
            "Incomplete Data", "Please fill out all required fields!"
        )
    else:
        info = (
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Hobbies: {', '.join(hobbies)}\n"
            f"Country: {country}\n"
            f"Comment: {comment}"
        )
        messagebox.showinfo("Form Submitted", info)


# ---------- Widgets ----------
tk.Label(
    window, text="Personal Information Form", font=("Arial", 16, "bold"), bg="lightblue"
).pack(pady=10)

# Frame for inputs
frame = tk.Frame(window, bg="lightblue")
frame.pack(pady=5)

# Entry (Name)
tk.Label(frame, text="Full Name:", bg="lightblue", font=("Arial", 12)).grid(
    row=0, column=0, sticky="w"
)
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, pady=3)

# Entry (Age)
tk.Label(frame, text="Age:", bg="lightblue", font=("Arial", 12)).grid(
    row=1, column=0, sticky="w"
)
entry_age = tk.Entry(frame, width=30)
entry_age.grid(row=1, column=1, pady=3)

# Radiobutton (Gender)
tk.Label(frame, text="Gender:", bg="lightblue", font=("Arial", 12)).grid(
    row=2, column=0, sticky="w"
)
gender_var = tk.StringVar()
tk.Radiobutton(
    frame, text="Male", variable=gender_var, value="Male", bg="lightblue"
).grid(row=2, column=1, sticky="w")
tk.Radiobutton(
    frame, text="Female", variable=gender_var, value="Female", bg="lightblue"
).grid(row=2, column=1, sticky="e")

# Checkbutton (Hobbies)
tk.Label(frame, text="Hobbies:", bg="lightblue", font=("Arial", 12)).grid(
    row=3, column=0, sticky="w"
)
hobby_reading = tk.BooleanVar()
hobby_sports = tk.BooleanVar()
hobby_music = tk.BooleanVar()
tk.Checkbutton(frame, text="Reading", variable=hobby_reading, bg="lightblue").grid(
    row=3, column=1, sticky="w"
)
tk.Checkbutton(frame, text="Sports", variable=hobby_sports, bg="lightblue").grid(
    row=4, column=1, sticky="w"
)
tk.Checkbutton(frame, text="Music", variable=hobby_music, bg="lightblue").grid(
    row=5, column=1, sticky="w"
)

# Combobox (Country)
tk.Label(frame, text="Country:", bg="lightblue", font=("Arial", 12)).grid(
    row=6, column=0, sticky="w"
)
country_cb = ttk.Combobox(
    frame, values=["Philippines", "Japan", "USA", "Canada", "Australia"], width=27
)
country_cb.grid(row=6, column=1, pady=5)

# Text (Comment)
tk.Label(window, text="Comments:", bg="lightblue", font=("Arial", 12)).pack(pady=5)
text_comment = tk.Text(window, width=35, height=4)
text_comment.pack()

# Submit Button
tk.Button(
    window,
    text="Submit",
    command=submit_form,
    bg="green",
    fg="white",
    font=("Arial", 12),
    width=10,
).pack(pady=10)

# Exit Button
tk.Button(
    window,
    text="Exit",
    command=window.destroy,
    bg="red",
    fg="white",
    font=("Arial", 12),
    width=10,
).pack()

window.mainloop()
