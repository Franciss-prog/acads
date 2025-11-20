from datetime import datetime, timedelta, date
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from models import Attendance, BorrowBookPayload, RenderBorrowedBook, ReturnBookPayload, AdminLoginPayload
from database import get_db_connection
from utils import calculate_return_date, clean_isbn

import jwt
from zoneinfo import ZoneInfo
import pymysql
import hashlib
import secrets

app = FastAPI()

# === CORS configuration ===
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # change to specific origins later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/attendance")
async def post_attendance(data: Attendance):
    if not data.token or data.hours <= 0:
        raise HTTPException(status_code=400, detail="Missing or invalid fields")

    db = None
    cursor = None
    try:
        # Decode token (skip signature verification only for dev)
        payload = jwt.decode(data.token, options={"verify_signature": False})
        srcode = payload.get("srcode")
        fullname = payload.get("fullname", "")
        type_ = payload.get("type", "student")

        if not srcode:
            raise HTTPException(
                status_code=400, detail="Malformed token: missing srcode"
            )

        # timezone
        timezone = ZoneInfo("Asia/Manila")
        now = datetime.now(timezone)
        timeout = now + timedelta(hours=data.hours)
        today = now.date()

        db = get_db_connection()
        cursor = db.cursor()

        # Check if student exists
        cursor.execute("SELECT * FROM student WHERE srcode = %s", (srcode,))
        student = cursor.fetchone()
        # if th student doesn't exist, create a new one
        if not student and type_.lower() == "student":
            cursor.execute(
                "INSERT INTO student (srcode, fullname, type, attendance_count) VALUES (%s, %s, %s, %s)",
                (srcode, fullname, type_, 0),
            )

        cursor.execute(
            "SELECT id FROM attendance WHERE srcode = %s AND DATE(time_in) = %s",
            (srcode, today),
        )
        existing_attendance = cursor.fetchone()

        if existing_attendance:
            raise HTTPException(
                status_code=409, detail="Attendance already recorded for today"
            )

        # Insert attendance
        cursor.execute(
            "INSERT INTO attendance (srcode, time_in, time_out) VALUES (%s, %s, %s)",
            (srcode, now, timeout),
        )

        # Increment attendance count
        cursor.execute(
            "UPDATE student SET attendance_count = attendance_count + 1 WHERE srcode = %s",
            (srcode,),
        )

        db.commit()
        return {"message": f"Attendance recorded successfully for {fullname}."}

    except pymysql.MySQLError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# for borrow book
@app.post("/borrow")
async def post_borrow(data: BorrowBookPayload):
    # validate the incoming data
    if not data.token or not data.isbn or not data.bookname or not data.bookauthor:
        raise HTTPException(status_code=400, detail="Missing or invalid fields")

    db = None
    cursor = None

    try:
        # clean the isbn just to make sure the isbn is no dash format and spaces format
        isbn = clean_isbn(data.isbn)

        # Decode token (skip signature verification only for dev)
        payload = jwt.decode(data.token, options={"verify_signature": False})
        fullname = payload.get("fullname", "")
        type_ = payload.get("type", "student")
        srcode = payload.get("srcode")

        if not fullname or not type_ or not srcode:
            raise HTTPException(
                status_code=400, detail="Malformed token: missing srcode"
            )

        # connect to the database
        db = get_db_connection()
        cursor = db.cursor()
        db.begin()  # start transaction

        # check if student exists
        cursor.execute("SELECT * FROM student WHERE srcode = %s", (srcode,))
        student = cursor.fetchone()

        # if the student doesn't exist, create a new one
        if not student:
            cursor.execute(
                "INSERT INTO student (srcode, fullname, type, attendance_count, book_count) VALUES (%s, %s, %s, %s,%s)",
                (srcode, fullname, type_, 0, 0),
            )

        # check if book exists
        cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
        book = cursor.fetchone()

        # if the book doesn't exist, create it
        if not book:
            cursor.execute(
                "INSERT INTO books (isbn, bookname, bookauthor) VALUES (%s, %s, %s)",
                (isbn, data.bookname, data.bookauthor),
            )
        # then update the book_count to student table
        cursor.execute(
            "UPDATE student SET book_count = book_count + 1 WHERE srcode = %s",
            (srcode,),
        )

        # prevent duplicate borrow (student already borrowed this book and not yet returned)
        cursor.execute(
            "SELECT * FROM borrow WHERE srcode = %s AND isbn = %s AND return_date >= CURDATE()",
            (srcode, isbn),
        )
        existing_borrow = cursor.fetchone()
        if existing_borrow:
            raise HTTPException(
                status_code=400, detail="Book already borrowed and not yet returned."
            )

        # calculate borrow and return dates
        borrow_date = date.today()
        return_date = calculate_return_date(borrow_date, data.returndays)

        # insert the borrowed book into the database
        cursor.execute(
            "INSERT INTO borrow (srcode, isbn, bookname,bookauthor,   borrow_date, return_date) VALUES (%s, %s, %s, %s, %s, %s)",
            (srcode, isbn, data.bookname, data.bookauthor, borrow_date, return_date),
        )

        db.commit()  # commit transaction
        return {"message": f"{fullname} borrowed '{data.bookname}' successfully."}

    except pymysql.MySQLError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# render for borrowed books
@app.post("/borrowed")
async def get_borrowed_books(data: RenderBorrowedBook):
    # GET THE data
    token = data.token
    if not token:
        raise HTTPException(status_code=400, detail="Missing token.")

    db = None
    cursor = None

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        srcode = payload.get("srcode")

        if not srcode:
            raise HTTPException(
                status_code=400, detail="Malformed token: missing srcode"
            )

        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Fetch only this student's borrowed book
        cursor.execute(
            "SELECT * FROM borrow WHERE srcode = %s LIMIT 1",
            (srcode,),
        )
        borrowed_book = cursor.fetchone()

        if not borrowed_book:
            return {"borrowed": False}

        return {
            "borrowed": True,
            "books": borrowed_book,
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# return book
@app.post("/returnbook")
async def delete_borrow_book(data: ReturnBookPayload):
    token = data.token
    isbn = clean_isbn(data.isbn)

    if not token or not isbn:
        raise HTTPException(status_code=400, detail="Missing token or ISBN.")

    db = None
    cursor = None

    try:
        # Decode token (skip signature verification only for dev)
        payload = jwt.decode(token, options={"verify_signature": False})
        srcode = payload.get("srcode")
        fullname = payload.get("fullname", "")

        if not srcode:
            raise HTTPException(
                status_code=400, detail="Malformed token: missing srcode"
            )

        db = get_db_connection()
        cursor = db.cursor()
        db.begin()

        # Check if the user actually borrowed this book
        cursor.execute(
            "SELECT * FROM borrow WHERE srcode = %s AND isbn = %s",
            (srcode, isbn),
        )
        borrowed_book = cursor.fetchone()

        if not borrowed_book:
            raise HTTPException(
                status_code=404,
                detail="You have no record of borrowing this book.",
            )

        # Delete the borrow record
        cursor.execute(
            "DELETE FROM borrow WHERE srcode = %s AND isbn = %s",
            (srcode, isbn),
        )

        db.commit()
        return {"message": f"{fullname} returned the book successfully."}

    except pymysql.MySQLError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# Admin login endpoint
@app.post("/admin/login")
async def admin_login(data: AdminLoginPayload):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Missing username or password")

    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Check if admin table exists, if not create it with default admin
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

        # Check if any admin exists
        cursor.execute("SELECT COUNT(*) as count FROM admin")
        admin_count = cursor.fetchone()["count"]
        
        # If no admin exists at all, create default admin (username: admin, password: admin123)
        if admin_count == 0:
            default_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO admin (username, password_hash) VALUES (%s, %s)",
                ("admin", default_password_hash)
            )
            db.commit()

        # Check if the provided username exists
        cursor.execute("SELECT * FROM admin WHERE username = %s", (data.username,))
        admin = cursor.fetchone()

        if not admin:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Hash the provided password and compare
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        if password_hash != admin["password_hash"]:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Generate a simple admin token (in production, use proper JWT)
        admin_token = secrets.token_urlsafe(32)
        
        return {
            "message": "Login successful",
            "token": admin_token,
            "username": admin["username"]
        }

    except pymysql.MySQLError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# Get top attendance (ranked by total hours)
@app.get("/admin/top-attendance")
async def get_top_attendance():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Calculate total hours for each student
        # Total hours = SUM of TIMESTAMPDIFF(HOUR, time_in, time_out) from attendance table
        cursor.execute("""
            SELECT 
                s.srcode,
                s.fullname as name,
                COALESCE(SUM(TIMESTAMPDIFF(HOUR, a.time_in, a.time_out)), 0) as total_hours
            FROM student s
            LEFT JOIN attendance a ON s.srcode = a.srcode
            WHERE s.type = 'student'
            GROUP BY s.srcode, s.fullname
            ORDER BY total_hours DESC
            LIMIT 100
        """)
        
        students = cursor.fetchall()
        
        # Format the response
        result = []
        for student in students:
            result.append({
                "name": student["name"] or "Unknown",
                "total_hours": int(student["total_hours"]) if student["total_hours"] else 0
            })

        return {"students": result}

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# Get most borrowed books (ranked by book_count)
@app.get("/admin/most-borrowed-books")
async def get_most_borrowed_books():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Get students ranked by book_count
        cursor.execute("""
            SELECT 
                srcode,
                fullname as name,
                COALESCE(book_count, 0) as books_borrowed
            FROM student
            WHERE type = 'student'
            ORDER BY books_borrowed DESC
            LIMIT 100
        """)
        
        students = cursor.fetchall()
        
        # Format the response
        result = []
        for student in students:
            result.append({
                "name": student["name"] or "Unknown",
                "books_borrowed": int(student["books_borrowed"]) if student["books_borrowed"] else 0
            })

        return {"students": result}

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# Get today's attendance
@app.get("/admin/today-attendance")
async def get_today_attendance():
    db = None
    cursor = None
    try:
        timezone = ZoneInfo("Asia/Manila")
        today = datetime.now(timezone).date()

        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Get today's attendance records
        cursor.execute("""
            SELECT 
                s.fullname as name,
                TIMESTAMPDIFF(HOUR, a.time_in, a.time_out) as hours,
                DATE_FORMAT(a.time_in, '%%Y-%%m-%%d %%H:%%i:%%s') as time
            FROM attendance a
            JOIN student s ON a.srcode = s.srcode
            WHERE DATE(a.time_in) = %s
            ORDER BY a.time_in DESC
        """, (today,))
        
        records = cursor.fetchall()
        
        # Format the response
        result = []
        for record in records:
            result.append({
                "name": record["name"] or "Unknown",
                "hours": int(record["hours"]) if record["hours"] else 0,
                "time": record["time"] or "N/A"
            })

        return {"attendance": result}

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
