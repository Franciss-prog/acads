grade = int(input("Enter your grade: "))


if grade >= 8 or grade <= 10:
    print("A")
elif grade >= 5 or grade <= 7:
    print("B")
elif grade >= 2 or grade <= 4:
    print("C")
elif grade >= 0 or grade <= 1:
    print("D")
else:
    pass
