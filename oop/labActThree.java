public class labActThree {

  // class for creating student
  class Student {
    String name;
    int age;

    // create a constructor for
    public Student(String name, int age) {
      this.name = name;
      this.age = age;
    }
  }

  public static void main(String[] args) {
    // access outer
    labActThree labActThree = new labActThree();
    // access inner
    Student student = labActThree.new Student("Franciss", 19);
    System.out.println("Name: " + student.name);
    System.out.println("Age: " + student.age);
  }
}
