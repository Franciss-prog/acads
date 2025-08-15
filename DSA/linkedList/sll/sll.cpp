#include<iostream>
using namespace std;



struct Node{
  Node*next;
  int data;

  Node(int value){
    next = nullptr;
    data = value;
  }
};
Node*head;

void addNode(int value) {
  // create a new Node based on Struct Node inserting the value of params
  Node*newNode = new Node(value);

  // check the first Node if the first Node have value
  if (head == nullptr) {
    head = newNode;
  }
  else {
    // Create a Temporary Node
    Node*temporary = head;

    // check if the next nodes have value 
    while (temporary->next != nullptr) {
      // increment
      temporary = temporary->next;
    }
    // set the next node to newNode
    temporary->next = newNode;
  }
}

void printNodes(){

  // create a temporary node 
  Node *listOfNodes = head;

while (listOfNodes != nullptr) {
  cout << listOfNodes->data << " -> ";
  listOfNodes = listOfNodes->next;
}
cout << "NULL\n";
}
int main(){
  int nodeInput;

  cout << "Enter a number to add to Node: "; cin >> nodeInput;
  addNode(nodeInput);
  printNodes();


  return 0;
}
