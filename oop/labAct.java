
// Activity 1
public class labAct {

  class Book {
    String title;
    String author;
  }

  public static void main(String[] args) {
    // access outer
    labAct labAct = new labAct();
    // access inner
    Book book = labAct.new Book();
    book.title = "Java";
    book.author = "Franciss";

    System.out.println(book.author);
    System.out.println(book.title);
  }
}
