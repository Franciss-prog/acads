abstract class Employee {
    abstract double calculatePay();
}

class HourlyEmployee extends Employee {
    double hourlyRate;
    int hoursWorked;

    HourlyEmployee(double rate, int hours) {
        this.hourlyRate = rate;
        this.hoursWorked = hours;
    }

    double calculatePay() {
        return hourlyRate * hoursWorked;
    }
}

class SalariedEmployee extends Employee {
    double monthlySalary;

    SalariedEmployee(double salary) {
        this.monthlySalary = salary;
    }

    double calculatePay() {
        return monthlySalary;
    }
}

public class abs_2 {
    public static void main(String[] args) {
        HourlyEmployee hourly = new HourlyEmployee(20, 40);
        SalariedEmployee salaried = new SalariedEmployee(5000);
        System.out.println("Hourly employee pay: " + hourly.calculatePay());
        System.out.println("Salaried employee pay: " + salaried.calculatePay());
    }
}
