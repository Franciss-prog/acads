#include <ctime>
#include <iostream>
#include <regex>
#include <sstream>
#include <vector>
using namespace std;

struct Attendance {
  string SRCODE;
  string name;
  string timeIn;
  string timeOut;
};

vector<Attendance> AttendanceList;

string getCurrentTimeInFormat() {
  // Get the current system time
  time_t now = time(0);
  tm *currentTime = localtime(&now);

  // Buffer to store formatted time
  char timeBuffer[80];

  // Format the time to "HH:MM AM/PM"
  strftime(timeBuffer, sizeof(timeBuffer), "%I:%M %p", currentTime);

  return string(timeBuffer); // E.g., "10:30 AM"
}

// Validates SR-CODE format
bool isValidSRCode(string srcode) {
  regex pattern("^\\d{2}-\\d{5}$");
  return regex_match(srcode, pattern);
}

// Placeholder for time validation (optional)
bool isValidTime(string timeOut) {
  regex pattern("^((0?[1-9])|(1[0-2])):[0-5][0-9]\\s?(AM|PM)$",
                regex_constants::icase);
  if (!regex_match(timeOut, pattern)) {
    cout << "❌ Invalid time format. Use HH:MM AM/PM.\n";
    return false;
  }
  // parsed the time
  int inputHour, inputMinute;
  string period;
  char colon;

  istringstream iss(timeOut);
  iss >> inputHour >> colon >> inputMinute >> period;

  // Convert to 24hour format
  if (period == "PM" && inputHour != 12) {
    inputHour += 12;
  } else if (inputHour == 12 && period == "AM") {
    inputHour = 0;
  }
  // convert minutes
  int inputMinutes = inputHour * 60 + inputMinute;
  time_t now = time(0);

  tm *current = localtime(&now);

  // struct for time
  tm inputTime = *current;
  inputTime.tm_hour = inputHour;
  inputTime.tm_min = inputMinute;
  inputTime.tm_sec = 0;

  // Convert both to time_t (epoch seconds)
  time_t inputEpoch = mktime(&inputTime);
  time_t currentEpoch = mktime(current);

  if (inputEpoch < currentEpoch) {
    cout << "❌ Entered time is earlier than the current time.\n";
    return false;
  }
  cout << currentEpoch;
  return true;
}

void listOfStudentAttendance() {
  system("clear");
  cout << "\n--- List of Student Attendance ---\n";
  if (AttendanceList.empty()) {
    cout << "No records found.\n";
    return;
  }

  int index = 1;
  for (const auto &entry : AttendanceList) {
    cout << index++ << ". " << entry.SRCODE << " | " << entry.name << " | "
         << entry.timeIn << "->" << entry.timeOut << endl;
  }
  cout << "----------------------------------\n";
}

void addAttendance() {
  system("clear");
  string name, srcode, timeOut;
  string timeIn = getCurrentTimeInFormat();
  cin.ignore(); // Clear input buffer
  cout << "Enter your Name: ";
  getline(cin, name);

  while (true) {
    cout << "Enter your SR-CODE (24-45678): ";
    getline(cin, srcode);

    if (isValidSRCode(srcode))
      break;
    cout << "❌ Invalid SR-CODE format. Try again.\n";
  }
  // print the current time so that the user will know
  cout << "Time In: " << timeIn << endl;
  while (true) {
    cout << "Enter your Timeout (HH:MM AM/PM): ";
    getline(cin, timeOut);

    if (isValidTime(timeOut))
      break;
    cout << "❌ Invalid time format. Try again.\n";
  }

  AttendanceList.push_back({srcode, name, timeIn, timeOut});
  cout << "\n✅ Attendance Recorded!\n";
  listOfStudentAttendance();
  system("clear");
}
void showMenu() {
  cout << "\n<--------------- Student Attendance Library System "
          "--------------->\n";
  cout << "1. Show List of Attendance\n";
  cout << "2. Add New Student Attendance\n";
  cout << "3. Exit\n";
  cout << "-------------------------------------------------------------------"
          "\n";
  cout << "Enter choice [1-3]: ";
}
int main() {
  int choice;
  do {
    showMenu();
    cin >> choice;

    switch (choice) {
    case 1:
      listOfStudentAttendance();
      break;
    case 2:
      addAttendance();
      break;
    case 3:
      cout << "👋 Exiting... Thank you!\n";
      break;
    default:
      cout << "❗ Invalid choice. Please enter 1, 2, or 3.\n";
    }
  } while (choice != 3);
  return 0;
}
