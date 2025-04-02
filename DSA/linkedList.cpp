#include<iostream>
using namespace std;

// node struct
struct Node
{
    // holds the data 
    int data;
    // holds the pointer of next data
    Node* next; // Pointer to the next node

    // initialize a node (new Node())
    Node(int value){
        data = value;
        next = nullptr; // The next pointer is set to nullptr initially
    }
};

class LinkedList{
public:
    // head pointer to the first node of the list
    Node* head;

    // constructor to initialize an empty list
    LinkedList(){
        head = nullptr; // When the list is created, it starts as empty
    }

    // function to insert node to the end of the list
    void insertToEnd(int val){
        // declare a new Node based on Node
        Node* newNode = new Node(val); // Create a new node with the given value

        // set the head to newNode if the head doesn't have a value
        if (head == nullptr) { // If the list is empty
            head = newNode; // Set the new node as the head
        }
        else {
            // initialize a tempvar and set the tempvar to head
            Node* tempvar = head; // Start from the head node

            // Traverse to the last node in the list
            while (tempvar->next != nullptr) {
                tempvar = tempvar->next; // Move to the next node
            }
            tempvar->next = newNode; // Attach the new node to the last node's next pointer
        }
    }

    // function to print the data in the list
    void printData(){
        Node* currentNode = head; // Start from the head node

        // Traverse the list and print each node's data
        while (currentNode != nullptr) {
            cout << currentNode->data << "->";// Print the current node's data
            currentNode = currentNode->next; // Move to the next node
           
        }
        cout <<"null"<< endl;
    }
};

int main(){
    LinkedList list;

    list.insertToEnd(10); // Insert 10 into the list
    list.insertToEnd(20); // Insert 20 into the list
    list.insertToEnd(30); // Insert 30 into the list

    list.printData(); // Output: 10 20 30
    return 0;
}
