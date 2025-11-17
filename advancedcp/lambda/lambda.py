# calcu using lambda
add = lambda x, y: x + y
sub = lambda x, y: x - y
mul = lambda x, y: x * y
div = lambda x, y: x / y


while True:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    operator = input("Enter your operation (+, -, *, /): ")

    # validate the operator
    if operator not in ["+", "-", "*", "/"]:
        print("Invalid operator. Please choose from +, -, *, /")
        exit()

    if operator == "+":
        print(num1, "+", num2, "=", add(num1, num2))
    if operator == "-":
        print(num1, "-", num2, "=", sub(num1, num2))
    if operator == "*":
        print(num1, "*", num2, "=", mul(num1, num2))
    if operator == "/":
        print(num1, "/", num2, "=", div(num1, num2))

    while True:
        next_calculation = input("Let's do next calculation? (yes/no): ")
        if next_calculation is not "yes":
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue
        if next_calculation == 'yes':
            break
        print("Goodbye!")
        exit()
