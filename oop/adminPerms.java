
class adminPerms {
  public static void main(String[] args) {
    boolean isAdmin = false;
    boolean isLoggedIn = true;
    int securityLevel = 1;

    if (iLoggedIn && (isAdmin || securityLevel <= 2)) {
      System.out.println("Access granted");
    } else if (isAdmin) {
      System.out.println("Overwrite access granted");
    } else {
      System.out.println("Access denied");
    }
  }

}
