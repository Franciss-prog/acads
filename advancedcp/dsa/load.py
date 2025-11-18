# CREATE A PROGRAM IN A DICTIONARY FORMAT

import os
import pprint

students = {
    1: {"name": "John", "age": 19, "srCode": "24-43298"},
    2: {"name": "Jane", "age": 20, "srCode": "24-43299"},
    3: {"name": "Jack", "age": 21, "srCode": "24-43331"},
    4: {"name": "Jack", "age": 21, "srCode": "24-43332"},
    5: {"name": "Jack", "age": 21, "srCode": "24-43324"},
}


def add_student(id):
    studentName = input("Enter student name: ")
    studentAge = input("Enter student age: ")
    studentCode = input("Enter student code: ")

    students[id] = {
        "name": studentName,
        "age": studentAge,
        "srCode": studentCode,
    }
    print("Student added successfully")
    os.system("clear")


def display_students():
    pprint.pprint(students)


def saveStudentData():
    # convert dictionary to array
    content = str(students)
    # save the data to a file named studentData.json
    with open("studentData.txt", "w") as file:
        file.write(content)
        print("Data saved successfully")


while True:
    print("1: Add Student")
    print("2: display Studends")
    print("3: Save Student Data")
    print("4: Exit")

    choice = int(input("Enter your choice:  "))

    if choice == 1:
        add_student(len(students) + 1)
        os.system("clear")

    elif choice == 2:
        display_students()

    elif choice == 3:
        saveStudentData()
    elif choice == 4:
        break
    else:
        print("Invalid choice")
        continue
