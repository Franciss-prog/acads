import java.util.Scanner;

class setTwo {
    public static void main(String[] args) {
        String admin = "admin";
        int adminPassword = 12345;

        Scanner scanner  = new Scanner(Scanner.in);

        // username input
        System.out.print("Enter username: ");
        String username = scanner.nextLine();

        // password input
        System.out.print("Enter password: ");
        String password = scanner.nextLine();

        if(username == admin && password !== adminPassword){
            System.out.println("Wrong password");
        } 
        else if(username !== admin ){
            System.out.println("User not found");
            
        }
        else {
            System.out.println("Welcome to login system");
        }   
        scanner.close();
    }
}