#include <iostream>
using namespace std;

// Node structure for a singly linked list
struct Node {
    int data;   // Stores the value
    Node* next; // Pointer to the next node

    // Constructor to initialize a new node
    Node(int value) {
        data = value;
        next = nullptr; // The next pointer is set to nullptr initially
    }
};

// Linked List class
class LinkedList {
public:
    Node* head; // Pointer to the first node of the list

    // Constructor to initialize an empty list
    LinkedList() {
        head = nullptr; // The list starts as empty
    }   

    // Function to insert a node at the end of the list
    void insertToEnd(int val) {
        Node* newNode = new Node(val); // Create a new node with the given value

        // If the list is empty, set newNode as head
        if (head == nullptr) {
            head = newNode;
        }
        else {
            Node* tempvar = head; // Start from the head

            // Traverse to the last node
            while (tempvar->next != nullptr) {
                tempvar = tempvar->next; // Move to the next node
            }

            // Attach the new node to the last node's next pointer
            tempvar->next = newNode;
        }
    }

    // Function to delete the first node
    void deleteFirstNode() {
        if (head == nullptr) return; // If the list is empty, do nothing

        Node* temp = head;  // Store the head node in temp
        head = head->next;  // Move head to the next node
        delete temp;        // Delete the old head

        printData(); // Print the list after deletion
    }

    // Function to print all nodes in the list
    void printData() {
        Node* currentNode = head; // Start from the head

        // Traverse the list and print each node's data
        while (currentNode != nullptr) {
            cout << currentNode->data << " -> "; // Print the current node's data
            currentNode = currentNode->next; // Move to the next node
        }

        cout << "NULL" << endl; // Indicate the end of the list
    }
};

int main() {
    LinkedList list;

    list.insertToEnd(20); // Insert 20 into the list
    list.insertToEnd(10); // Insert 10 into the list
    list.insertToEnd(30); // Insert 30 into the list
    list.insertToEnd(40); // Insert 40 into the list

    list.printData(); // Output: 20 -> 10 -> 30 -> 40 -> NULL

    list.deleteFirstNode(); // Delete the first node (20)
    return 0;
}
