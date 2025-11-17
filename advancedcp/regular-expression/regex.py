import re


#  format email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

while True:
    confirm_email = input("Enter your email: ")

    if re.fullmatch(regex, confirm_email):
        print("Valid Email")
        break
    else:
        print("Invalid Email, Please Try Again!")
        continue
