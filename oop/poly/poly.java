class InkPrinter {
    void printDocument() {
        System.out.println("Printing with ink...");
    }
}

class LaserPrinter {
    void printDocument() {
        System.out.println("Printing with laser...");
    }
}

public class poly {
    public static void main(String[] args) {
        InkPrinter ink = new InkPrinter();
        LaserPrinter laser = new LaserPrinter();
        ink.printDocument();
        laser.printDocument();
    }
}

