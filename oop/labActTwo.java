
public class labActTwo {

  class Student {
    String name;
    int age;

    // constructor
    public Student(String name, int age) {
      this.name = name;
      this.age = age;
    }

  }

  public static void main(String[] args) {
    // access outer
    labActTwo labActTwo = new labActTwo();
    Student student = labActTwo.new Student("Franciss", 19);

    // print the name and age
    System.out.println("Name: " + student.name);
    System.out.println("Age: " + student.age);
  }
}
