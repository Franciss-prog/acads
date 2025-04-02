#include <iostream>
using namespace std;

// Node structure for the doubly linked list
struct Node {
    int data;     // Stores the value
    Node* next;   // Points to the next node
    Node* prev;   // Points to the previous node

    Node(int value) {
        data = value;
        next = nullptr;
        prev = nullptr;
    }
};

// Doubly linked list class
class LinkedList {
public:
    Node* head;  // Points to the first node

    LinkedList() {
        head = nullptr;  // Start with an empty list
    }

    // Add a node to the end of the list
    void addNodeToEnd(int value) {
        Node* newNode = new Node(value);

        // If the list is empty, set newNode as head
        if (head == nullptr) {
            head = newNode;
        } else {
            // Create a pointer to traverse the list
            Node* currentNode = head;  

            // Move to the last node
            while (currentNode->next != nullptr) {
                currentNode = currentNode->next;
            }

            // Attach newNode at the end
            currentNode->next = newNode;
            newNode->prev = currentNode; // Link back to previous node
        }
    }

    // Print all nodes in the list
    void printData() {
        Node* listOfData = head;

        while (listOfData != nullptr) {
            cout << listOfData->data << " <-> ";
            listOfData = listOfData->next;
        }
        cout << "NULL" << endl;
    }

    // Reverse the linked list
    void reverseList() {
        Node* temporary = nullptr;
        Node* current = head;

        while (current != nullptr) {
            // Swap next and prev pointers
            temporary = current->prev;
            current->prev = current->next;
            current->next = temporary;

            // Move to the next node (which is prev after swapping)
            current = current->prev;
        }

        // Update head to the last node (which is now the first)
        if (temporary != nullptr) {
            head = temporary->prev;
        }
    }

    // Delete the first node
    void deleteFirstNode() {
        if (head == nullptr) return; // Nothing to delete

        Node* temporary = head;
        head = head->next; // Move head to the next node

        if (head != nullptr) {
            head->prev = nullptr; // Remove old head's reference
        }

        delete temporary; // Delete the old head
    }
};

int main() {
    LinkedList list;

    // Add nodes to the list
    list.addNodeToEnd(20);
    list.addNodeToEnd(10);
    list.addNodeToEnd(30);
    list.addNodeToEnd(40);

    list.printData();  // Output: 20 <-> 10 <-> 30 <-> 40 <-> NULL

    list.reverseList(); // Reverse the list
    list.printData();  // Output: 40 <-> 30 <-> 10 <-> 20 <-> NULL

    list.deleteFirstNode(); // Delete the first node (40)
    list.printData();  // Output: 30 <-> 10 <-> 20 <-> NULL

    return 0;
}
