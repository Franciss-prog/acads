#include<iostream>
#include<ctime>
#include<chrono>
#include<thread>
using namespace std;

int main () { 
  while (true) {
    time_t now = time(nullptr);

    cout << "Time: " << ctime(&now) << flush << endl;
    cin.clear();
    this_thread::sleep_for(chrono::seconds(1));
  }
  return 0;
}


