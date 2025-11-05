// Base class
class Person {
  protected String name; // Protected = only subclasses can access

  void showInfo() {
    System.out.println("I am " + name);
  }
}

// Child class 1
class Student extends Person {
  // Constructor to set name
  Student(String name) {
    this.name = name;
  }

  // Overriding showInfo()
  void showInfo() {
    System.out.println("I am " + name + ", a student.");
  }

  // Method Overloading
  void sendMessage() {
    System.out.println("Message sent to teacher.");
  }

  void sendMessage(String msg) {
    System.out.println("Message sent to teacher: " + msg);
  }
}

// Child class 2
class Teacher extends Person {
  // Constructor to set name
  Teacher(String name) {
    this.name = name;
  }

  // Overriding showInfo()
  void showInfo() {
    System.out.println("I am " + name + ", a teacher.");
  }

  void sendMessage() {
    System.out.println("Message sent to student.");
  }
}

// Composition Example (School has Students and Teachers)
class School {
  Student student;
  Teacher teacher;

  School(Student student, Teacher teacher) {
    this.student = student;
    this.teacher = teacher;
  }

  void schoolInfo() {
    System.out.println("School has: " + student.name + " and " + teacher.name);
  }
}

// Main class
public class wala_si_maam {
  public static void main(String[] args) {
    // Polymorphism: same parent type, different child behavior
    Person p1 = new Student("Francis");
    Person p2 = new Teacher("Mr. Cruz");

    p1.showInfo(); // Student version
    p2.showInfo(); // Teacher version

    System.out.println();

    // Overloading and extra features
    Student s1 = new Student("Francis");
    s1.sendMessage();
    s1.sendMessage("Can I submit my project tomorrow?");

    System.out.println();

    // Composition: A School has a Student and a Teacher
    Teacher t1 = new Teacher("Mr. Cruz");
    School school = new School(s1, t1);
    school.schoolInfo();
  }
}
