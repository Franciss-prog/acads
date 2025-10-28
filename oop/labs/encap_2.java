class Person {
    private int age;

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age > 0) {
            this.age = age;
        } else {
            System.out.println("Age must be positive!");
        }
    }
}

public class encap_2 {
    public static void main(String[] args) {
        Person person = new Person();
        person.setAge(20);
        System.out.println("Age: " + person.getAge());
    }
}
