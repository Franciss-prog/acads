
public class ArrayActivity {
  public static void main(String[] args) {
    int scores[] = new int[10];
    scores[0] = 72;
    scores[1] = 85;
    scores[2] = 90;
    scores[3] = 78;
    scores[4] = 99;
    scores[5] = 92;
    scores[6] = 88;
    scores[7] = 75;
    scores[8] = 82;
    scores[9] = 74;

    // Activity 1
    System.out.println("Activity 1 \n");
    // print the first element\
    System.out.println("first  element: " + scores[0]);
    // print the lowest
    System.out.println("Lowest score: " + scores[0]);
    // print the highest element
    System.out.println("Higest score: " + scores[4]);
    // print the last element
    System.out.println("Last element: " + scores[9]);

    System.out.println("\n");

    // Activity 2
    System.out.println("Activity 2 \n");

    // Use a for loop to print all the elements of the scores array with their index
    for (int i = 0; i < scores.length; i++) {
      System.out.println("index: " + i);
      // Then use a for-each loop to print only the values.
      System.out.println("element: " + scores[i]);
    }
    System.out.println("\n");

    // Activity 3
    System.out.println("Activity 3 \n");
    // Using the scores array, calculate the average score.
    int sum = 0;
    // print the sum of score
    for (int i = 0; i < scores.length; i++) {
      sum += scores[i];
    }
    // get the average by dividing the sum by the length of the array
    double average = sum / scores.length;
    // print the average
    System.out.println("Average score: " + average);
  }
}
