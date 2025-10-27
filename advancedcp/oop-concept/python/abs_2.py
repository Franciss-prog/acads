class Employee:
    def calculate_pay(self):
        print("calculate_pay not implemented")


class HourlyEmployee(Employee):
    def __init__(self, hours, rate):
        self.hours = hours
        self.rate = rate

    def calculate_pay(self):
        print(self.hours * self.rate)


class SalariedEmployee(Employee):
    def __init__(self, salary):
        self.salary = salary

    def calculate_pay(self):
        print(self.salary)


# Test
e1 = HourlyEmployee(40, 15)
e2 = SalariedEmployee(600)
e1.calculate_pay()  # 600
e2.calculate_pay()  # 600
