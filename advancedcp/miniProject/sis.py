# create a dictionary to store student information
import os
import time


students = {
    1: {"name": "John", "age": 19, "srCode": "24-43298"},
    2: {"name": "Jane", "age": 20, "srCode": "24-43299"},
    3: {"name": "Jack", "age": 21, "srCode": "24-43331"},
}


# function to view all students
def view_students():
    print("<----------All students---------->")
    print(students)


def timer(n):
    if n == 0:
        print("Timer completed")
        return 1
    print("countdown to exit: ", n)
    time.sleep(1)
    os.system("clear")
    timer(n - 1)


# function to add Student
def add_student():
    os.system("clear")
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))  # type casting
    sr_code = input("Enter student code: ")

    # validate else
    if not name:
        name = "N/A"
    elif not age:
        age = "N/A"
    elif not sr_code:
        sr_code = "N/A"

    # add the tudent to the dictionary
    students[len(students) + 1] = {"name": name, "age": age, "srCode": sr_code}

    # print all the students
    view_students()


def delete_student():
    os.system("clear")
    # print all the students
    view_students()

    # ask the user to enter the id of the student to
    id = int(input("Enter the id of the student to delete: "))

    # delete the student from the dictionary
    del students[id]

    # print all the students
    print("<----------Updated students---------->")
    view_students()
    timer(10)


# function to search student by name
def search_student():
    os.system("clear")
    name = input("Enter the name of the student to search: ")
    # check if the student exists
    if name in students:
        print(students[name])
    else:
        print("Student not found")


# main porgram
while True:
    os.system("clear")
    print("Welcome to the student information system")
    print("1. Add a student")
    print("2. View all students")
    print("3. Delete student")
    print("4. Search student by name")
    print("5. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        add_student()
    if choice == "2":
        view_students()
    if choice == "3":
        delete_student()
    if choice == "4":
        search_student()
    if choice == "5":
        break
