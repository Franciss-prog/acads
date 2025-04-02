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
    void deleteNode(int value) {
        if (head == nullptr) return; // If the list is empty, do nothing
        
        // Check if the first node is the one to be deleted
        if (head->data == value) {
            Node* firstNode = head; // Store the current head as firstNode
            head = head->next; // Move head to the next node
    
            // If the list is not empty after deleting the head, update the previous pointer of the new head to null
            if (head != nullptr) {
                head->prev = nullptr;
            }
            
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
        prev->next = current->next; // Connect previous node to the next node
    
        // If the node to be deleted is not the last node, update the previous pointer of the next node
        if (current->next != nullptr) {
            current->next->prev = prev;
        }
    
        delete current; // Delete the node
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
    list.printData();  // 20 <-> 10 <-> 30 <-> 40 <-> NULL

    list.reverseList(); // Reverse the list
    cout << "list(backward): ";
    list.printData();  // 40 <-> 30 <-> 10 <-> 20 <-> NULL

    cout << "Delete 10..." << endl;
    list.deleteNode(10); // Delete  node (10)
    list.printData();  // 40 <-> 30 <-> 20 <-> NULL

    // reverse the list
    list.reverseList(); //reverse the current list
    cout << "list(forward): ";
    list.printData(); // 20 <-> 30 <-> 40 <->  NULL
    return 0;
}
