#include<iostream>

using namespace std;

int main(){
    int arr[10] = {1,2,3};
    int currentSize = 3;
    int arrayLength = sizeof(arr) / sizeof(arr[0]);
    


    if (currentSize < arrayLength)
    {
        arr[currentSize++] = 5;
    }
  
    
    int firstOut = currentSize-1;
    cout << "Top element before pop: " << arr[firstOut] << endl;

    if (currentSize > 0)
    {
        int poppedValue = arr[firstOut];
        currentSize--;
        cout << "Popped value: " << poppedValue << endl;
        
    }
    else{
        cout << "Stack is empty!" << endl;
    }

  
    
}