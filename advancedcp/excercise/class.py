class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposed PHP{amount}. New balance: PHP{self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(
                f"{self.owner} withdrew PHP{amount}. Reamaining balance: PHP{self.balance}"
            )
        else:
            print("Insufficient funds")


account1 = BankAccount("Jasmin", 5000)
account1.deposit(1500)
account1.withdraw(2000)
account1.withdraw(6000)
