# 1. create 5 food list
food = ["pasta", "spaghetti", "pancit", "adobo", "noodles"]
# implement reomve an add food
# ask user for input to add and remove food
addFood = input("Enter food to add: ")
food.append(addFood)  # remove food
# print the result
print(food)
removeFood = input("Enter food to remove: ")
food.remove(removeFood)
print(food)


# 2.  create a tuple of favorite cars
cars = ("toyota", "honda", "bmw", "ford", "audi")
# print all the cars
print(cars)
# access the 2nd car and last car and print
print("2nd car:" + "" + cars[1])
print("last car:" + "" + cars[-1])

# try to change the 2nd car and observe the error
# cars[1] = "honda"
# print the result
print(cars)

# 3. create a set of 6 hoobies
physicalHobbies = {
    "swimming",
    "running",
    "biking",
    "coding",
    "swimming",
    "weightlifting",
}
mentalHobbies = {
    "reading",
    "coding",
    "listening to music",
    "playing video games",
    "watching movies",
    "playing board games"
}

# spacing
print("\n")

print("Set A: ", physicalHobbies)
print("Set B: ", mentalHobbies)
print("\n")

print("\n")


union = physicalHobbies | mentalHobbies
difference = physicalHobbies - mentalHobbies
intersection = physicalHobbies & mentalHobbies
print("Union: ", union)
print("Difference: ", difference)
print("Intersection: ", intersection)
