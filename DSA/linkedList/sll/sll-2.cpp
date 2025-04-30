#include<iostream>

using namespace std;


// sll
struct Node
{
    Node*next;
    int data;
    
    Node(int value){
        next = nullptr;
        data = value;
    }
};
Node*head;


void printNodes () {
 Node*listOfNodes = head;

 while (listOfNodes != nullptr)
 {
    cout << listOfNodes->data << " "  ;
    listOfNodes = listOfNodes->next;
 }
 cout << "NULL" << endl;
 
}
void addNode (int value){
    // create a node based on struct
    Node*newNode = new Node(value);

    // validate if the list of node has a value 
    // if the node doesnt have a value set the head to newNode
    if (head == nullptr)
    {
        head = newNode;
    }
    else{
        // create a temporaryNode that has head value
        // head = value
       Node*temporaryNode = head;

       while (temporaryNode != nullptr)
       {
        // incrementation
        temporaryNode = temporaryNode->next;
       }
        // set the next to new node 
       temporaryNode->next = newNode;
    }
    
    printNodes();
}
int main (){
    int nodeInput;
    cout << "enter a number to add In node: "; cin >>nodeInput;
    addNode(nodeInput);    
    return 0;
}

