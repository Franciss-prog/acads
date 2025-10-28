interface Speakable {
    void speak();
}

class Bird implements Speakable {
    public void speak() {
        System.out.println("Tweet!");
    }
}

class Robot implements Speakable {
    public void speak() {
        System.out.println("Beep boop!");
    }
}

public class DuckTyping {
    static void makeItSpeak(Speakable obj) {
        obj.speak();
    }

    public static void main(String[] args) {
        makeItSpeak(new Bird());
        makeItSpeak(new Robot());
    }
}
public class poly_2 {
  public static void main(String[] args) {
    DuckTyping.makeItSpeak(new Bird());
    DuckTyping.makeItSpeak(new Robot());
    DuckTyping.makeItSpeak(123);
  }
}
