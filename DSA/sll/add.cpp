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
    void addNodeToEnd(int val) {
        Node* newNode = new Node(val); // Create a new node with the given value

        // If the list is empty, set newNode as head
        if (head == nullptr) {
            head = newNode;
        }
        else {
            Node* temporary = head; // Start from the head

            // Traverse to the last node
            while (temporary->next != nullptr) {
                temporary = temporary->next; // Move to the next node
            }

            // Attach the new node to the last node's next pointer
            temporary->next = newNode;
        }
    }

     
    // Function to delete the selected node
void deleteNode(int value) {
    if (head == nullptr) return; // If the list is empty, do nothing

    // Check if the first node is the one to be deleted
    if (head->data == value) {
        Node* firstNode = head; // Store the current head as firstNode
        head = head->next; // Move head to the next node
        delete firstNode; // Delete the old head (firstNode)
        return;
    }
    Node* current = head; // Start from the head
    Node* prev = nullptr; // Keep track of the previous node


    // Traverse the list to find the node to delete
    while (current != nullptr && current->data != value) {
        prev = current;
        current = current->next;
    }

    // If the value was not found, do nothing
    if (current == nullptr) return;

    // Remove the node from the list
    prev->next = current->next;
    delete current; // Delete the node
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
     // Function to insert a node after a specific node (for your second step)
     void insertAfter(int prevValue, int newValue) {
        Node* newNode = new Node(newValue); // Create a new node

        Node* current = head;
        // Traverse the list to find the node after which we want to insert the new node
        while (current != nullptr && current->data != prevValue) {
            current = current->next;
        }

        // If the prevValue node was found, insert the new node
        if (current != nullptr) {
            newNode->next = current->next; // Link the new node to the next node
            current->next = newNode; // Link the previous node to the new node
        }
    }
};

int main() {
    LinkedList list;

    // Add nodes to the list
    list.addNodeToEnd(20);
    list.addNodeToEnd(10);
    list.addNodeToEnd(30);
    list.addNodeToEnd(40);

    cout << "list(forward): ";
    list.printData();  // Output: 20 -> 10 -> 30 -> 40 -> NULL

    cout << "Deleting 10..." << endl;
    list.deleteNode(10); // Delete the node 10
    cout << "list(forward): ";
    list.printData();  //  20 -> 30 -> 40 -> NULL

    // Insert 10 again after the first node (20)
    list.insertAfter(20, 10);

    // Now delete the first node (20)
    list.deleteNode(20);
    list.printData();  // Output after deleting 20: 10 -> 30 -> 40 -> NULL

    return 0;
}