public class labActThree {

  // class for creating student
  class Student {
    String name;
    int age;

    // getter
    public String getName() {
      return name;
    }

    public int getAge() {
      return age;
    }
  }

  public static void main(String[] args) {
    // access outer
    labActThree labActThree = new labActThree();
    // access inner
    Student student = labActThree.new Student();
    System.out.println("Name: " + student.name);
    System.out.println("Age: " + student.age);
  }
}
