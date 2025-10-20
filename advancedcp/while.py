numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even = []
odd = []
for number in numbers:

    if number % 2 == 0:
        even.append(number)
    else:
        odd.append(number)

print("Numbers: ", numbers)
print("Even: ", even)
print("Odd: ", odd)
