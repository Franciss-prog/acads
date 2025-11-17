class BankAccount {
    private double balance;

    public BankAccount(double balance) {
        this.balance = balance;
    }

    public void deposit(double amount) {
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= balance) {
            balance -= amount;
        } else {
            System.out.println("Insufficient funds!");
        }
    }

    public double getBalance() {
        return balance;
    }
}

public class encap {
    public static void main(String[] args) {
        BankAccount account = new BankAccount(1000.0);
        account.deposit(500.0);
        account.withdraw(200.0);
        System.out.println("Current balance: " + account.getBalance());
    }
}

