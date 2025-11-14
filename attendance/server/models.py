from pydantic import BaseModel


# Attendance model for incoming requests
class Attendance(BaseModel):
    token: str
    hours: int


class BorrowBookPayload(BaseModel):
    token: str
    isbn: str
    bookname: str
    bookauthor: str
    returndays: int


class ReturnBookPayload(BaseModel):
    token: str
    isbn: str
