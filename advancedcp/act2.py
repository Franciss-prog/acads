import math
import os
import statistics
# student info
print("Welcome to customer info")
name = input("Enter your name: ")
address = input("Enter your address: ")
phone = input("Enter your phone number: ")
email = input("Enter your email: ")
sex = input("Enter your gender: ")
age = input("Enter your age: ")
srCode = input("Enter your student code: ")
score = 0;

# set to N/A if empty
if not name:
    name = "N/A"
if not address:
    address = "N/A"
if not phone:
    phone = "N/A"
if not email: 
    email = "N/A"
if not sex:
    sex = "N/A"
if not age:
    age = "N/A"
if not srCode:
    srCode = "N/A"

if age.isdigit():
    age = int(age)

os.system('cls' if os.name == 'nt' else 'clear')

# math quiz
print("\nWelcome to the Math Quiz!")

print("\nQuestion 1: What is the square root of 144?")
answer1 = float(input("Your answer: "))
correct1 = math.sqrt(144)

if answer1 == correct1:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct1}")

print("Question 2: What is 20 add 30?")
answer2 = int(input("Your answer: "))
correct2 = 20 + 30
if answer2 == correct2:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct2}") 

print("Question 3: What is 15 multiply by 3?")
answer3 = int(input("Your answer: "))
correct3 = 15 * 3
if answer3 == correct3:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct3}")

print("Question 4: What is 20 divide by 4?")
answer4 = float(input("Your answer: "))
correct4 = 20 / 4
if answer4 == correct4:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct4}")

print("Question 5: What is 10 minus 4?")
answer5 = int(input("Your answer: "))
correct5 = 10 - 4
if answer5 == correct5:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct5}")

print("Question 6: What is 2 to the power of 3?")
answer6 = int(input("Your answer: "))
correct6 = 2 ** 3
if answer6 == correct6:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct6}")

print("Question: 7 What is percentage of 50 out of 200?")
answer7 = float(input("Your answer: "))
correct7 = (50 / 200) * 100
if answer7 == correct7:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct7}")

print("Question 8: What is the value of pi (up to 2 decimal places)?")
answer8 = float(input("Your answer: "))
correct8 = round(math.pi, 2)
if answer8 == correct8:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct8}")

print("Question 9: What is the factorial of 5?")    
answer9 = int(input("Your answer: "))
correct9 = math.factorial(5)
if answer9 == correct9:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct9}")

print("Question 10: What is Median of the following numbers: 3, 1, 4, 2, 5?")
answer10 = float(input("Your answer: "))
numbers = [3, 1, 4, 2, 5]
statistics.median(numbers)
correct10 = statistics.median(numbers)
if answer10 == correct10:
    print("Correct!")
    score += 1
else:
    print(f"Incorrect. The correct answer is {correct10}")


print(f"\n Your total score is: {score} out of 10")
# score logic 
if score >= 8:
    print("\nVery good ")
elif score >= 5 or score < 8:
    print("\n Good")

elif score >= 3 or score < 5:
    print("\nFair!")
else:
    print("\nBetter luck next time!")

