from datetime import datetime, timedelta, date
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from models import Attendance, BorrowBookPayload
from database import get_db_connection
from utils import calculate_return_date, clean_isbn

import jwt
from zoneinfo import ZoneInfo
import pymysql

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
                "INSERT INTO student (srcode, fullname, type, attendance_count) VALUES (%s, %s, %s, %s)",
                (srcode, fullname, type_, 0),
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
async def get_borrowed_books(token: str):
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
            return {"borrowed": False, "message": "No borrowed book found."}

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


from fastapi import Request


@app.delete("/borrow")
async def delete_borrow_book(request: Request):
    data = await request.json()
    token = data.get("token")
    isbn = data.get("isbn")

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
