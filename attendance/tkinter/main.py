import base64
import json
import threading
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, Optional

import time

try:
    import cv2  # type: ignore[import]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "OpenCV (cv2) is required. Install with `pip install opencv-python`."
    ) from exc

try:
    from pyzbar import pyzbar  # type: ignore[import]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "pyzbar is required. Install with `pip install pyzbar` and ensure zbar is installed."
    ) from exc

import requests
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore[import]
    from matplotlib.figure import Figure  # type: ignore[import]

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    FigureCanvasTkAgg = None  # type: ignore[assignment]
    Figure = None  # type: ignore[assignment]
    MATPLOTLIB_AVAILABLE = False

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
BACKEND_BASE_URL = "http://localhost:8000"


def sanitize_isbn(isbn: str) -> str:
    return isbn.replace("-", "").replace(" ", "").upper()


def is_valid_isbn(isbn: str) -> bool:
    return bool(__import__("re").match(r"^(97[89]\d{10}|\d{9}[\dX])$", isbn))


def to_isbn13(isbn: str) -> str:
    isbn = sanitize_isbn(isbn)
    if len(isbn) == 13:
        return isbn
    core = "978" + isbn[:-1]
    total = 0
    for idx, char in enumerate(core):
        total += int(char) * (1 if idx % 2 == 0 else 3)
    check_digit = (10 - (total % 10)) % 10
    return core + str(check_digit)


def jwt_format(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 3 and all(parts)


def jwt_decode(token: str) -> Optional[Dict[str, Any]]:
    if not jwt_format(token):
        return None
    try:
        payload_b64 = token.split(".")[1]
        padding = "=" * (-len(payload_b64) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
        payload = json.loads(payload_bytes.decode("utf-8"))
        return payload
    except (ValueError, json.JSONDecodeError):
        return None


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper


@dataclass
class Book:
    title: str
    authors: str
    isbn: str
    thumbnail_url: Optional[str] = None


class BackendClient:
    def __init__(self, base_url: str = BACKEND_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        response.raise_for_status()
        return response.json()

    def borrow_book(self, token: str, book: Book, return_days: int) -> Dict[str, Any]:
        payload = {
            "token": token,
            "isbn": book.isbn,
            "bookname": book.title,
            "bookauthor": book.authors or "Unknown",
            "returndays": return_days,
        }
        return self._handle_response(
            requests.post(f"{self.base_url}/borrow", json=payload, timeout=10)
        )

    def fetch_borrowed(self, token: str) -> Dict[str, Any]:
        return self._handle_response(
            requests.post(f"{self.base_url}/borrowed", json={"token": token}, timeout=10)
        )

    def return_book(self, token: str, isbn: str) -> Dict[str, Any]:
        payload = {"token": token, "isbn": isbn}
        return self._handle_response(
            requests.post(f"{self.base_url}/returnbook", json=payload, timeout=10)
        )

    def log_attendance(self, token: str, hours: int) -> Dict[str, Any]:
        payload = {"token": token, "hours": hours}
        return self._handle_response(
            requests.post(f"{self.base_url}/attendance", json=payload, timeout=10)
        )

    def admin_login(self, username: str, password: str) -> Dict[str, Any]:
        payload = {"username": username, "password": password}
        return self._handle_response(
            requests.post(f"{self.base_url}/admin/login", json=payload, timeout=10)
        )

    def get_top_attendance(self) -> Dict[str, Any]:
        return self._handle_response(
            requests.get(f"{self.base_url}/admin/top-attendance", timeout=10)
        )

    def get_most_borrowed_books(self) -> Dict[str, Any]:
        return self._handle_response(
            requests.get(f"{self.base_url}/admin/most-borrowed-books", timeout=10)
        )

    def get_today_attendance(self) -> Dict[str, Any]:
        return self._handle_response(
            requests.get(f"{self.base_url}/admin/today-attendance", timeout=10)
        )


class BookService:
    @staticmethod
    def fetch_book_by_isbn(isbn: str) -> Optional[Book]:
        isbn = sanitize_isbn(isbn)
        if not is_valid_isbn(isbn):
            raise ValueError("Invalid ISBN. Must be 10 or 13 characters.")

        isbn13 = to_isbn13(isbn)
        params = {"q": f"isbn:{isbn13}"}
        response = requests.get(GOOGLE_BOOKS_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("items"):
            return None

        volume = data["items"][0]["volumeInfo"]
        authors = ", ".join(volume.get("authors", []))
        identifiers = volume.get("industryIdentifiers", [])
        isbn_value = next(
            (ident["identifier"] for ident in identifiers if ident["type"] == "ISBN_13"),
            isbn13,
        )
        thumbnail = volume.get("imageLinks", {}).get("thumbnail")
        return Book(
            title=volume.get("title", "Unknown Title"),
            authors=authors or "Unknown",
            isbn=isbn_value,
            thumbnail_url=thumbnail,
        )


class AppFrame(tk.Frame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.app = master

    def on_show(self):
        pass

    def on_hide(self):
        pass


class LandingFrame(AppFrame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.configure(bg="#111")

        tk.Label(
            self,
            text="Library Attendance System\n  Batangas State University Mabini Campus",
            font=("Helvetica", 28, "bold"),
            fg="#f8f8f8",
            bg="#111",
        ).pack(pady=(120, 12))
        tk.Label(
            self,
            text="Scan your student QR code to record attendance,\nborrow, or return books.",
            font=("Helvetica", 14),
            fg="#ddd",
            bg="#111",
            justify="center",
        ).pack(pady=8)

        ttk.Button(self, text="Scan QR Code", command=self.goto_scanner).pack(pady=40)

        ttk.Button(self, text="Admin Login", command=self.open_admin_login).pack(pady=10)

        tk.Label(
            self,
            text="© 2025 Library Attendance System",
            font=("Helvetica", 10),
            fg="#777",
            bg="#111",
        ).pack(side=tk.BOTTOM, pady=20)

    def goto_scanner(self):
        self.app.show_frame("scanner")

    def open_admin_login(self):
        AdminLoginDialog(self.app)


class QRScannerFrame(AppFrame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.configure(bg="#111")
        self.capture = None
        self.scan_active = False
        self.image_label = tk.Label(self, bg="#000")
        self.image_label.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        controls = tk.Frame(self, bg="#111")
        controls.pack(pady=10)
        ttk.Button(controls, text="Stop", command=self.stop_camera).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(controls, text="Back", command=self.go_back).pack(
            side=tk.LEFT, padx=5
        )

        self.status_var = tk.StringVar(value="Camera not started")
        tk.Label(
            self,
            textvariable=self.status_var,
            fg="#ccc",
            bg="#111",
            font=("Helvetica", 12),
        ).pack(pady=(0, 20))

    def on_show(self):
        self.start_camera()

    def on_hide(self):
        self.stop_camera()

    def go_back(self):
        self.app.show_frame("landing")

    def start_camera(self):
        if self.capture is not None:
            return
        self.status_var.set("Starting camera...")
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.status_var.set("Cannot access camera.")
            messagebox.showerror("Camera Error", "Cannot access webcam.")
            self.capture = None
            return
        self.scan_active = True
        self.status_var.set("Ready to scan")
        self.after(50, self.update_frame)

    def stop_camera(self):
        self.scan_active = False
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        self.image_label.configure(image="")
        self.image_label.image = None

    def update_frame(self):
        if not self.capture or not self.scan_active:
            return
        ret, frame = self.capture.read()
        if not ret:
            self.status_var.set("Failed to read frame.")
            self.after(100, self.update_frame)
            return
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)
        if decoded:
            data = decoded[0].data.decode("utf-8")
            self.scan_active = False
            self.status_var.set("QR detected. Processing...")
            self.after(100, self.process_token, data)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((640, 480))
        photo = ImageTk.PhotoImage(image=img)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        if self.scan_active:
            self.after(30, self.update_frame)

    def process_token(self, token: str):
        self.stop_camera()
        self.app.handle_token(token)


class BorrowFrame(AppFrame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.backend = BackendClient()
        self.current_token: Optional[str] = None
        self.current_book: Optional[Book] = None
        self.thumbnail_image = None

        self.configure(bg="#111")
        self.title_var = tk.StringVar(value="Borrow a Book")
        tk.Label(
            self, textvariable=self.title_var, font=("Helvetica", 20, "bold"), bg="#111", fg="#fafafa"
        ).pack(pady=20)

        form = tk.Frame(self, bg="#111")
        form.pack(pady=10)

        tk.Label(form, text="ISBN (10 or 13 digits):", fg="#ddd", bg="#111").grid(
            row=0, column=0, sticky="w"
        )
        self.isbn_entry = ttk.Entry(form, width=30)
        self.isbn_entry.grid(row=1, column=0, pady=5)

        ttk.Button(form, text="Find Book", command=self.fetch_book).grid(
            row=1, column=1, padx=10
        )

        self.info_frame = tk.Frame(self, bg="#111", bd=1, relief=tk.GROOVE)
        self.info_frame.pack(pady=20, padx=30, fill=tk.X)
        self.book_label = tk.Label(
            self.info_frame,
            text="Book info will appear here.",
            fg="#ccc",
            bg="#111",
            justify="left",
        )
        self.book_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.thumbnail_label = tk.Label(self.info_frame, bg="#111")
        self.thumbnail_label.pack(side=tk.RIGHT, padx=10)

        control_frame = tk.Frame(self, bg="#111")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Return in (days):", fg="#ddd", bg="#111").grid(
            row=0, column=0, sticky="w"
        )
        self.return_days = tk.IntVar(value=1)
        tk.Spinbox(
            control_frame, from_=1, to=7, width=5, textvariable=self.return_days
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            self, text="Confirm Borrow", command=self.confirm_borrow
        ).pack(pady=20)
        ttk.Button(self, text="Back", command=lambda: self.app.show_frame("landing")).pack(
            pady=(0, 10)
        )

    def set_token(self, token: str, full_name: str):
        self.current_token = token
        self.title_var.set(f"What book do you want to borrow?\n{full_name}")
        self.clear_book_info()

    def clear_book_info(self):
        self.current_book = None
        self.book_label.config(text="Book info will appear here.")
        self.thumbnail_label.config(image="")
        self.thumbnail_label.image = None

    @threaded
    def fetch_book(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showwarning("Missing ISBN", "Please enter an ISBN.")
            return
        try:
            book = BookService.fetch_book_by_isbn(isbn)
            if not book:
                self.after(0, lambda: messagebox.showinfo("Not Found", "Book not found."))
                self.after(0, self.clear_book_info)
                return
            self.current_book = book
            self.after(0, self.display_book_info)
        except ValueError as exc:
            self.after(0, lambda: messagebox.showerror("Invalid ISBN", str(exc)))
        except requests.RequestException as exc:
            self.after(
                0, lambda: messagebox.showerror("Network Error", f"Failed to fetch book info.\n{exc}")
            )

    def display_book_info(self):
        if not self.current_book:
            return
        book = self.current_book
        info = f"Title: {book.title}\nAuthors: {book.authors}\nISBN: {book.isbn}"
        self.book_label.config(text=info)
        if book.thumbnail_url:
            try:
                response = requests.get(book.thumbnail_url, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img = img.resize((120, 180))
                self.thumbnail_image = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=self.thumbnail_image)
                self.thumbnail_label.image = self.thumbnail_image
            except requests.RequestException:
                self.thumbnail_label.config(image="")
                self.thumbnail_label.image = None
        else:
            self.thumbnail_label.config(image="")
            self.thumbnail_label.image = None

    def confirm_borrow(self):
        if not self.current_token:
            messagebox.showerror("Missing Token", "Student token missing. Scan QR first.")
            return
        if not self.current_book:
            messagebox.showerror("No Book", "Please fetch a book first.")
            return
        return_days = int(self.return_days.get())
        try:
            result = self.backend.borrow_book(self.current_token, self.current_book, return_days)
            messagebox.showinfo("Borrowed", result.get("message", "Book borrowed successfully."))
            self.app.show_frame("scanner")
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail") if exc.response is not None else str(exc)
            messagebox.showerror("Borrow Failed", detail or "Request failed.")
        except requests.RequestException as exc:
            messagebox.showerror("Network Error", f"Failed to borrow book.\n{exc}")


class ReturnFrame(AppFrame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.backend = BackendClient()
        self.current_token: Optional[str] = None
        self.book_data: Optional[Book] = None
        self.title_var = tk.StringVar(value="Return borrowed book")

        self.configure(bg="#111")
        tk.Label(
            self, textvariable=self.title_var, font=("Helvetica", 20, "bold"), fg="#fafafa", bg="#111"
        ).pack(pady=20)

        self.info_label = tk.Label(self, text="", fg="#ddd", bg="#111", justify="left")
        self.info_label.pack(pady=20)

        ttk.Button(self, text="Mark as Returned", command=self.confirm_return).pack(
            pady=10
        )
        ttk.Button(self, text="Back", command=lambda: self.app.show_frame("landing")).pack(
            pady=(0, 20)
        )

    def set_token(self, token: str, full_name: str):
        self.current_token = token
        self.title_var.set(f"Return borrowed book\n{full_name}")
        self.info_label.config(text="Fetching borrowed book details...")
        self.load_borrowed_book()

    @threaded
    def load_borrowed_book(self):
        if not self.current_token:
            self.after(0, lambda: messagebox.showerror("Error", "Token missing."))
            return
        try:
            data = self.backend.fetch_borrowed(self.current_token)
            if not data.get("borrowed"):
                self.after(
                    0,
                    lambda: [
                        messagebox.showinfo("No Books", "No borrowed books found."),
                        self.app.show_frame("scanner"),
                    ],
                )
                return
            book_info = data.get("books", {})
            authors = book_info.get("bookauthor", "")
            self.book_data = Book(
                title=book_info.get("bookname", "Unknown"),
                authors=authors,
                isbn=book_info.get("isbn", ""),
                thumbnail_url=book_info.get("thumbnail"),
            )
            borrowed_date = book_info.get("borrowed_date")
            info = f"Title: {self.book_data.title}\nAuthors: {self.book_data.authors}\nISBN: {self.book_data.isbn}"
            if borrowed_date:
                info += f"\nBorrowed on: {borrowed_date}"
            self.after(0, lambda: self.info_label.config(text=info))
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail") if exc.response is not None else str(exc)
            self.after(0, lambda: messagebox.showerror("Error", detail or "Failed to fetch book."))
        except requests.RequestException as exc:
            self.after(
                0, lambda: messagebox.showerror("Network Error", f"Failed to fetch borrowed book.\n{exc}")
            )

    def confirm_return(self):
        if not self.current_token or not self.book_data:
            messagebox.showerror("Error", "No borrowed book to return.")
            return
        try:
            result = self.backend.return_book(self.current_token, self.book_data.isbn)
            messagebox.showinfo("Returned", result.get("message", "Book returned successfully."))
            self.app.show_frame("scanner")
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail") if exc.response is not None else str(exc)
            messagebox.showerror("Return Failed", detail or "Request failed.")
        except requests.RequestException as exc:
            messagebox.showerror("Network Error", f"Failed to return book.\n{exc}")


class AttendanceFrame(AppFrame):
    def __init__(self, master: "LibraryApp"):
        super().__init__(master)
        self.backend = BackendClient()
        self.current_token: Optional[str] = None
        self.configure(bg="#111")
        self.title_var = tk.StringVar(value="Attendance")

        tk.Label(
            self, textvariable=self.title_var, font=("Helvetica", 22, "bold"), fg="#fafafa", bg="#111"
        ).pack(pady=30)

        self.status_var = tk.StringVar(value="Ready to submit attendance.")
        tk.Label(self, textvariable=self.status_var, fg="#ccc", bg="#111").pack(pady=10)

        hours_frame = tk.Frame(self, bg="#111")
        hours_frame.pack(pady=10)
        tk.Label(hours_frame, text="Hours attended (1-8):", fg="#ddd", bg="#111").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.hours_var = tk.IntVar(value=1)
        self.hours_spin = tk.Spinbox(
            hours_frame,
            from_=1,
            to=8,
            width=5,
            textvariable=self.hours_var,
            justify="center",
        )
        self.hours_spin.grid(row=0, column=1, padx=5)

        ttk.Button(self, text="Record Attendance", command=self.submit_attendance).pack(
            pady=10
        )
        ttk.Button(self, text="Back", command=lambda: self.app.show_frame("landing")).pack(
            pady=10
        )

    def set_token(self, token: str, full_name: str):
        self.current_token = token
        self.title_var.set(f"Record Attendance\n{full_name}")
        self.status_var.set("Ready to submit attendance.")
        self.hours_var.set(1)

    def submit_attendance(self):
        if not self.current_token:
            messagebox.showerror("Missing Token", "Student token missing. Scan QR first.")
            return
        try:
            hours = int(self.hours_var.get())
            if hours <= 0:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showwarning("Invalid Hours", "Please select hours between 1 and 8.")
            return
        try:
            result = self.backend.log_attendance(self.current_token, hours)
            messagebox.showinfo(
                "Attendance", result.get("message", "Attendance recorded successfully.")
            )
            self.app.show_frame("scanner")
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail") if exc.response is not None else str(exc)
            messagebox.showerror("Attendance Failed", detail or "Request failed.")
        except requests.RequestException as exc:
            messagebox.showerror("Network Error", f"Failed to record attendance.\n{exc}")


class ChoiceDialog(tk.Toplevel):
    def __init__(self, parent: "LibraryApp", user_name: str, on_choice):
        super().__init__(parent)
        self.title("Select action")
        self.resizable(False, False)
        self.configure(bg="#111")
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self,
            text=f"Hi {user_name}! What would you like to do?",
            fg="#fafafa",
            bg="#111",
            font=("Helvetica", 14, "bold"),
        ).pack(padx=30, pady=(20, 10))
        ttk.Button(
            self, text="Record Attendance", command=lambda: self._choose("attendance")
        ).pack(fill=tk.X, padx=30, pady=5)
        ttk.Button(self, text="Borrow Book", command=lambda: self._choose("borrow")).pack(
            fill=tk.X, padx=30, pady=5
        )
        ttk.Button(self, text="Return Book", command=lambda: self._choose("return")).pack(
            fill=tk.X, padx=30, pady=5
        )
        
        ttk.Button(self, text="Cancel", command=self.destroy).pack(
            fill=tk.X, padx=30, pady=(15, 20)
        )

        self.on_choice = on_choice

    def _choose(self, action: str):
        self.destroy()
        self.on_choice(action)


class AdminLoginDialog(tk.Toplevel):
    def __init__(self, parent: "LibraryApp"):
        super().__init__(parent)
        self.title("Admin Login")
        self.resizable(False, False)
        self.configure(bg="#111")
        self.transient(parent)
        self.grab_set()
        self.parent = parent
        self.backend = BackendClient()

        tk.Label(
            self,
            text="Admin Login",
            fg="#fafafa",
            bg="#111",
            font=("Helvetica", 18, "bold"),
        ).pack(padx=40, pady=(30, 20))

        form_frame = tk.Frame(self, bg="#111")
        form_frame.pack(padx=40, pady=10)

        tk.Label(form_frame, text="Username:", fg="#ddd", bg="#111").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.username_entry = ttk.Entry(form_frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Password:", fg="#ddd", bg="#111").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.password_entry = ttk.Entry(form_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        self.status_var = tk.StringVar(value="")
        tk.Label(
            form_frame, textvariable=self.status_var, fg="#ff6b6b", bg="#111", font=("Helvetica", 10)
        ).grid(row=2, column=0, columnspan=2, pady=5)

        button_frame = tk.Frame(self, bg="#111")
        button_frame.pack(padx=40, pady=(10, 30))

        ttk.Button(button_frame, text="Login", command=self.handle_login).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.username_entry.focus()
        self.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status_var.set("Please enter both username and password.")
            return

        self.status_var.set("Logging in...")
        threading.Thread(target=self._login, args=(username, password), daemon=True).start()

    def _login(self, username: str, password: str):
        try:
            result = self.backend.admin_login(username, password)
            self.after(0, lambda: self._on_login_success(result))
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail") if exc.response is not None else "Login failed."
            self.after(0, lambda: self.status_var.set(detail))
        except requests.RequestException as exc:
            self.after(0, lambda: self.status_var.set(f"Connection error: {exc}"))

    def _on_login_success(self, result: Dict[str, Any]):
        self.destroy()
        AdminDashboardWindow(self.parent)


class AdminDashboardWindow(tk.Toplevel):
    def __init__(self, parent: "LibraryApp"):
        super().__init__(parent)
        self.title("Admin Dashboard - Library Attendance System")
        self.geometry("1200x800")
        self.configure(bg="#111")
        self.backend = BackendClient()
        self._chart_refs = []

        tk.Label(
            self,
            text="Admin Dashboard",
            fg="#fafafa",
            bg="#111",
            font=("Helvetica", 24, "bold"),
        ).pack(pady=20)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        top_attendance_frame = tk.Frame(notebook, bg="#111")
        notebook.add(top_attendance_frame, text="Top Attendance")

        most_borrowed_frame = tk.Frame(notebook, bg="#111")
        notebook.add(most_borrowed_frame, text="Most Borrowed Books")

        today_attendance_frame = tk.Frame(notebook, bg="#111")
        notebook.add(today_attendance_frame, text="Today's Attendance")

        self._setup_top_attendance(top_attendance_frame)
        self._setup_most_borrowed(most_borrowed_frame)
        self._setup_today_attendance(today_attendance_frame)

        button_frame = tk.Frame(self, bg="#111")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Refresh All", command=self.refresh_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.refresh_all()

    def _setup_top_attendance(self, parent: tk.Frame):
        label = tk.Label(
            parent,
            text="Ranked list of students with highest attendance",
            fg="#ddd",
            bg="#111",
            font=("Helvetica", 12),
        )
        label.pack(pady=10)

        tree_frame = tk.Frame(parent, bg="#111")
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        chart_frame = tk.Frame(parent, bg="#111", width=300)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=10)
        self.top_chart_frame = chart_frame

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.top_attendance_tree = ttk.Treeview(
            tree_frame,
            columns=("Rank", "Student", "Total Hours"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        self.top_attendance_tree.heading("Rank", text="Rank")
        self.top_attendance_tree.heading("Student", text="Student Name")
        self.top_attendance_tree.heading("Total Hours", text="Total Hours")
        self.top_attendance_tree.column("Rank", width=80, anchor="center")
        self.top_attendance_tree.column("Student", width=300, anchor="w")
        self.top_attendance_tree.column("Total Hours", width=150, anchor="center")
        self.top_attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.top_attendance_tree.yview)

    def _setup_most_borrowed(self, parent: tk.Frame):
        label = tk.Label(
            parent,
            text="Students who borrowed the most books",
            fg="#ddd",
            bg="#111",
            font=("Helvetica", 12),
        )
        label.pack(pady=10)

        tree_frame = tk.Frame(parent, bg="#111")
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        chart_frame = tk.Frame(parent, bg="#111", width=300)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=10)
        self.most_borrowed_chart_frame = chart_frame

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.most_borrowed_tree = ttk.Treeview(
            tree_frame,
            columns=("Rank", "Student", "Books Borrowed"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        self.most_borrowed_tree.heading("Rank", text="Rank")
        self.most_borrowed_tree.heading("Student", text="Student Name")
        self.most_borrowed_tree.heading("Books Borrowed", text="Books Borrowed")
        self.most_borrowed_tree.column("Rank", width=80, anchor="center")
        self.most_borrowed_tree.column("Student", width=300, anchor="w")
        self.most_borrowed_tree.column("Books Borrowed", width=150, anchor="center")
        self.most_borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.most_borrowed_tree.yview)

    def _setup_today_attendance(self, parent: tk.Frame):
        label = tk.Label(
            parent,
            text="Students who scanned attendance today",
            fg="#ddd",
            bg="#111",
            font=("Helvetica", 12),
        )
        label.pack(pady=10)

        tree_frame = tk.Frame(parent, bg="#111")
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        chart_frame = tk.Frame(parent, bg="#111", width=300)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=10)
        self.today_chart_frame = chart_frame

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.today_attendance_tree = ttk.Treeview(
            tree_frame,
            columns=("Student", "Hours", "Time"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        self.today_attendance_tree.heading("Student", text="Student Name")
        self.today_attendance_tree.heading("Hours", text="Hours Attended")
        self.today_attendance_tree.heading("Time", text="Time")
        self.today_attendance_tree.column("Student", width=300, anchor="w")
        self.today_attendance_tree.column("Hours", width=150, anchor="center")
        self.today_attendance_tree.column("Time", width=200, anchor="center")
        self.today_attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.today_attendance_tree.yview)

    def refresh_all(self):
        threading.Thread(target=self._refresh_top_attendance, daemon=True).start()
        threading.Thread(target=self._refresh_most_borrowed, daemon=True).start()
        threading.Thread(target=self._refresh_today_attendance, daemon=True).start()

    def _render_bar_chart(
        self,
        frame: tk.Frame,
        labels: list[str],
        values: list[float],
        title: str,
        color: str = "#4CAF50",
    ):
        for widget in frame.winfo_children():
            widget.destroy()
        if not labels:
            tk.Label(
                frame,
                text="No data to visualize yet.",
                fg="#888",
                bg="#111",
                font=("Helvetica", 12),
            ).pack(expand=True)
            return
        if not MATPLOTLIB_AVAILABLE:
            tk.Label(
                frame,
                text="Install matplotlib to view charts.",
                fg="#fbc02d",
                bg="#111",
                font=("Helvetica", 12, "bold"),
                justify="center",
                wraplength=240,
            ).pack(expand=True, padx=20)
            return

        fig = Figure(figsize=(4.2, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.barh(labels, values, color=color)
        ax.set_title(title, color="#fafafa", fontsize=12, pad=14)
        ax.set_facecolor("#111")
        fig.patch.set_facecolor("#111")
        ax.tick_params(colors="#ddd")
        for spine in ax.spines.values():
            spine.set_color("#555")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        self._chart_refs.append(canvas)

    def _refresh_top_attendance(self):
        try:
            data = self.backend.get_top_attendance()
            students = data.get("students", [])
            self.after(0, lambda: self._populate_top_attendance(students))
        except requests.RequestException as exc:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch top attendance:\n{exc}"))

    def _populate_top_attendance(self, students: list):
        for item in self.top_attendance_tree.get_children():
            self.top_attendance_tree.delete(item)

        labels = []
        values = []
        for idx, student in enumerate(students, 1):
            name = student.get("name", "Unknown")
            hours = student.get("total_hours", 0)
            self.top_attendance_tree.insert("", tk.END, values=(idx, name, hours))
            labels.append(name)
            values.append(hours)

        self._render_bar_chart(
            self.top_chart_frame,
            labels,
            values,
            "Total Attendance Hours",
            color="#ff9800",
        )

    def _refresh_most_borrowed(self):
        try:
            data = self.backend.get_most_borrowed_books()
            students = data.get("students", [])
            self.after(0, lambda: self._populate_most_borrowed(students))
        except requests.RequestException as exc:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch most borrowed books:\n{exc}"))

    def _populate_most_borrowed(self, students: list):
        for item in self.most_borrowed_tree.get_children():
            self.most_borrowed_tree.delete(item)

        labels = []
        values = []
        for idx, student in enumerate(students, 1):
            name = student.get("name", "Unknown")
            count = student.get("books_borrowed", 0)
            self.most_borrowed_tree.insert("", tk.END, values=(idx, name, count))
            labels.append(name)
            values.append(count)

        self._render_bar_chart(
            self.most_borrowed_chart_frame,
            labels,
            values,
            "Books Borrowed",
            color="#4caf50",
        )

    def _refresh_today_attendance(self):
        try:
            data = self.backend.get_today_attendance()
            records = data.get("attendance", [])
            self.after(0, lambda: self._populate_today_attendance(records))
        except requests.RequestException as exc:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch today's attendance:\n{exc}"))

    def _populate_today_attendance(self, records: list):
        for item in self.today_attendance_tree.get_children():
            self.today_attendance_tree.delete(item)

        labels = []
        values = []
        for record in records:
            name = record.get("name", "Unknown")
            hours = record.get("hours", 0)
            time = record.get("time", "N/A")
            self.today_attendance_tree.insert("", tk.END, values=(name, hours, time))
            labels.append(f"{name} ({time})")
            values.append(hours)

        self._render_bar_chart(
            self.today_chart_frame,
            labels,
            values,
            "Today's Logged Hours",
            color="#2196f3",
        )


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Attendance System")

        self.geometry("900x700")
        self.configure(bg="#111")
        self.resizable(False, False)
        self.frames: Dict[str, AppFrame] = {}
        self.current_token: Optional[str] = None
        self.current_user: Optional[str] = None
        container = tk.Frame(self, bg="#111")
        container.pack(fill=tk.BOTH, expand=True)

        self.frames["landing"] = LandingFrame(self)
        self.frames["scanner"] = QRScannerFrame(self)
        self.frames["attendance"] = AttendanceFrame(self)
        self.frames["borrow"] = BorrowFrame(self)
        self.frames["return"] = ReturnFrame(self)

        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

        self.active_frame: Optional[AppFrame] = None
        self.show_frame("landing")

    def show_frame(self, name: str):
        frame = self.frames[name]
        if self.active_frame is frame:
            return
        if self.active_frame:
            self.active_frame.on_hide()
        frame.tkraise()
        self.active_frame = frame
        frame.on_show()

    def handle_token(self, token: str):
        decoded = jwt_decode(token)
        if not decoded or "fullname" not in decoded:
            messagebox.showwarning("Invalid Token", "Invalid token: missing user info.")
            self.show_frame("scanner")
            return
        full_name = decoded["fullname"]
        user_type = decoded.get("type", "STUDENT")
        if user_type == "TEACHER":
            messagebox.showinfo("Teacher Detected", f"Greetings {full_name}! Opening admin view.")
            self.show_frame("landing")
            return

        self.current_token = token
        self.current_user = full_name

        def on_choice(action: str):
            if action == "borrow":
                self.frames["borrow"].set_token(token, full_name)
                self.show_frame("borrow")
            elif action == "return":
                self.frames["return"].set_token(token, full_name)
                self.show_frame("return")
            elif action == "attendance":
                self.frames["attendance"].set_token(token, full_name)
                self.show_frame("attendance")
            else:
                self.show_frame("scanner")

        ChoiceDialog(self, full_name, on_choice)


def main():
    app = LibraryApp()
    app.mainloop()


if __name__ == "__main__":
    main()

