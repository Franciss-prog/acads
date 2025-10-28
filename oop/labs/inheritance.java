class Animal {
  public void speak() {
    System.out.println("The animal makes a sound");
  }
}

class Dog extends Animal {
  public void speak() {
    System.out.println("chao chao");
    System.out.println("Arf!");
    System.out.println("woof!");
  }
}
class Cat extends Animal {
  public void speak() {
    System.out.println("meow");
    System.out.println("purr");
    System.out.println("psspss");
  }
}



public class inheritance {
  public static void main(String[] args) {
    Dog dog = new Dog();
    dog.speak();
    Cat cat = new Cat();
    cat.speak();
  }
}
