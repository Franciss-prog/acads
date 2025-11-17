
public class Handling {
  public static void main(String[] args) {
    try {
      // code that may throw an exception
      int[] arr = { 1, 2, 3, 4, 5 };
      // if have a error
      // this will throw an exception
      System.out.println(arr[10]);
    } catch (Exception e) {
      // so the code print this
      System.out.println("Error: " + e);
    }
  }
}
