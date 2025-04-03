
#include<iostream>

using namespace std;

struct Node{
    int data;
    Node*next;

    Node(int value){
        data = value;
        next = nullptr;
    }
};

class SLL {
    public: 
        Node*head;

        SLL(){
            head = nullptr;
        }

        
    void addNode(int value){
        Node*newNode = new Node(value);

        if (head == nullptr)
        {
            head = newNode;
        }
        else{
            Node*temporary = head;

            while (temporary->next != nullptr)
            {
                // move to the nextNODE
                temporary = temporary->next;
            }
            temporary->next = newNode;
        }
        

    }
    void printNodes(){
        Node*listOfNodes = head;

        while (listOfNodes != nullptr)
        {
            cout << listOfNodes->data << ",";
            listOfNodes = listOfNodes->next;
        }
        cout << "NULL" << endl;
    }
    void printHeadAndTail(){
        if (head == nullptr) {
            cout << "List is empty." << endl;
            return;
        }
        // print head
       cout << "head: " << head->data << endl;

       Node*temporary  = head;
        while (temporary->next != nullptr)
        {
            temporary = temporary->next;
        }
        cout << "Tail: " << temporary->data << endl;
    }
    void deleteNode(int value) {
        if (head == nullptr) return;
        
        if (head->data == value)
        {
            Node*firstNode = head;
            head  = head->next;
            delete firstNode;
            return;
        }
        else{
            Node*currentNode = head;
            Node*prev = nullptr;
            
            while (currentNode != nullptr && currentNode->data != value)
            {
                prev = currentNode;
                currentNode = currentNode->next;
            }
            if (currentNode->data != value)
            {
                cout << "Value not Found" << endl;
                return;
            }
            prev->next = currentNode->next;
            delete currentNode;            
        }
        

    }
    void sortNode(){
        if (head == nullptr || head->next == nullptr)return;

        Node*currentNode;
        int temporary;
        Node*prev;
        Node*nextNode;


        for (currentNode = head; currentNode->next != nullptr; currentNode = currentNode->next){
            for (nextNode = currentNode->next; nextNode != nullptr; nextNode = nextNode->next)
            {
                if (currentNode->data > nextNode->data)
                {
                    temporary = currentNode->data;
                    currentNode->data = nextNode->data;
                    nextNode->data = temporary;

                }
                
            }
            
        }
   
        
    }
     bool searchNode(int key) {
        Node* temporary = head;
        
       while (temporary != nullptr)
       {
       if (temporary->data == key)
        {
            cout << "Found the data" << endl;
         return true;
        }
        temporary = temporary->next;
       }
       cout << "not found the data" << endl;

      return false;
    };
};
int main(){
    SLL link;
    link.addNode(10);
    link.addNode(9);
    link.addNode(8);
    link.addNode(7);
    link.addNode(6);
    link.addNode(5);
    link.addNode(4);
    link.addNode(3);
    link.addNode(2);
    link.addNode(1);

    link.printNodes();
   
    
    link.printHeadAndTail();

    // insert Node
    cout << "After Insert: ";link.addNode(11);link.printNodes();

    // after delete
    cout << "After Delete: : ";link.deleteNode(11);link.printNodes();
    cout << "sorting: : ";link.sortNode();link.printNodes();
    cout << "search 1: : ";link.searchNode(1);
    cout << "search 11: : ";link.searchNode(11);
    return 0;
}