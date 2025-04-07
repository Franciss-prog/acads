#include<iostream>
#include<vector>
#include<regex>
using namespace std;

struct Attendance {
  string SRCODE;
  string name;
  string timeIn;
};
int choice;
vector<Attendance> AttendanceList;

bool codeFormat(string srcode){
  // validation checker if the srcode has a legit format
   regex pattern{"^\\d{2}-\\d{5}$"};
   return regex_match(srcode, pattern); 
}
// bool function to validate the timeformat
void timeFormat(){
  return;
}
void listOfStudentAttendance(){
  cout << "\n--- List of Student Attendance ---\n";
  if (AttendanceList.empty()) {
    cout << "No records found.\n";
    return;
  }

  for (int i = 0; i < AttendanceList.size(); i++) {
    cout << i + 1 << ". " << AttendanceList[i].SRCODE
         << " - " << AttendanceList[i].name << " - " << AttendanceList[i].timeIn << endl;
  }
  cout << "----------------------------------\n";
}
void addAttendance(){
  string username, srCode, timeIn;
  cout << "Enter your Username: "; getline(cin, username);


do
{
  cout << "Enter your SR-CODE(43-45678): "; cin >> srCode;
  // validate the srCode
  if (!codeFormat(srCode))
  {
    cout << "Invalid SRCODE format...";
    return;
  }
} while (!codeFormat(srCode));

  cout << "Enter your Time-In: (7:00 AM) "; cin >> timeIn;
  AttendanceList.push_back({username,srCode, timeIn });
  listOfStudentAttendance();
  
}

void start() {
  cout << "<---------------Welcome to Student Attendance Library System!--------------->" << endl;
  cout << "1. Show List of Attendance" << endl;
  cout << "2. Add new Student Attendance" << endl;
  cout << " " << endl;
  cout << "Which one you want to do [1,2]: "; cin >> choice;


  switch (choice) {
    case 1:
    listOfStudentAttendance();
    break;
    case 2: 
    addAttendance();
    break;
    default:
      "Choose between 1 and 2";
      break;
  }
}
int main () {
  start();

  return 0;
}
