
public class student {
  private String name;
  private String email;
  private String phoneNumber;

  // getters
  public String getStudentName() {
    return name;
  }

  public String getStudentEmail() {
    return email;
  }

  public String getStudentPhoneNumber() {
    return phoneNumber;
  }

  // setters
  public void setStudentName(String name) {
    this.name = name;
  }

  public void setStudentEmail(String email) {
    this.email = email;
  }

  public void setStudentPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public static void main(String[] args) {
    // initalize student
    student studentName = new student();

    // set student name
    studentName.setStudentName("Christian");
    // set student email
    studentName.setStudentEmail("Gc2Ud@example.com");
    // set student phone number
    studentName.setStudentPhoneNumber("0987654321");

    // print name
    System.out.println("Name: " + studentName.getStudentName());
    // print email
    System.out.println("Email: " + studentName.getStudentEmail());
    // print phone number
    System.out.println("Phone Number: " + studentName.getStudentPhoneNumber());

  }
}
