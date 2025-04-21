#include <iostream>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;


struct Traveler {
    string name;
    int age;
    bool isLocal;
    bool isnotLocal;
    string destination;
    double fare;
    int discount;
};


class JetSetCode {
private:
    vector<Traveler> travelers;
    const int maxCapacity = 50;
    int currentCapacity = 0;
       double discount = 0.0;
    double baseFare = 160.00;


   double calculateFare(int age, bool isSummer, bool isLocal, bool isnotLocal) {
    double fare = baseFare;


    // Age-based fixed fares
    if (age >= 60) {
        fare = 104.00; // Senior fare
    }
    else if (age >= 13 && age <= 23) {
        fare = 116.00; // Student fare
    }
    else if (age >= 3 && age <= 12) {
        fare = 72.00;  // Child fare
    }
    else if (age < 3) {
        fare = 0.00;   // Infants free
    }


    // Summer discount
    if (isSummer) {
        fare *= 0.90;
    }


    // Environmental fee for non-locals
    if (!isLocal) {
        fare += 50.00;
    }


    return fare;
}




public:
    void registerTraveler(bool isSummer) {
        system("clear");
        if (currentCapacity >= maxCapacity) {
            cout << "Sorry, the ferry is at full capacity.\n";
            return;
        }


        Traveler t;
        cout << "\n--- Register New Traveler ---\n";
        cout << "Name: ";
        getline(cin >> ws, t.name);
        cout << "Age: ";
        cin >> t.age;
        cout << "Is the traveler local? (1 = Yes, 0 = No): ";
        cin >> t.isLocal;
        cout << "Destination (Tingloy/Mabini): ";
        cin >> ws;
        getline(cin, t.destination);


        t.fare = calculateFare(t.age, isSummer, t.isLocal, t.isnotLocal);
        travelers.push_back(t);
        currentCapacity++;


        cout << "Registration successful!\n";
        cout << "Fare: ₱" << fixed << setprecision(2) << t.fare << endl;
        cout << "Environmental Fee:" << endl;
        cout << "Total:" << endl;
        cout << "Remaining seats: " << (maxCapacity - currentCapacity) << "\n";
    }


    void showPassengerList() {
        system("clear");
        cout << "\n--- Passenger List ---\n";
        if (travelers.empty()) {
            cout << "No passengers registered.\n";
            return;
        }
        for (const auto& t : travelers) {
            cout << "Name: " << t.name
                 << " | Age: " << t.age
                 << " | Local: " << (t.isLocal ? "Yes" : "No")
                 << " | Destination: " << t.destination
                 << " | Fare: ₱" << fixed << setprecision(2) << t.fare
                 <<  " | Discount Percentage: ₱" << discount*100 << endl;
        }
        cout << "Total passengers: " << currentCapacity << "/" << maxCapacity << "\n";
    }
    void mainMenu() {
        system("clear");
        int choice;
        bool isSummer;
        cout << "===Welcome to Montenegro E-Ticket Services===" << endl << "        powered by: JetSetCode" << endl;
        cout << ""<< endl;
       


        do {
            cout << "\n==== JetSetCode Menu ====\n";
            cout << "1. Register Traveler\n";
            cout << "2. Show Passenger List\n";
            cout << "3. Exit\n";
            cout << "Choose option: ";
            cin >> choice;


            switch (choice) {
                case 1: registerTraveler(isSummer); break;
                case 2: showPassengerList(); break;
                case 3: cout << "Goodbye!\n"; break;
                default: cout << "Invalid choice.\n"; break;
            }



        } while (choice != 3);
    }
};


int main() {
    JetSetCode system;
    system.mainMenu();
    return 0;
}

