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
Node*head;

void addNode(int value) {
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

  Node *listOfNodes = head;

while (listOfNodes != nullptr) {
  cout << listOfNodes->data << " -> ";
  listOfNodes = listOfNodes->next;
}
cout << "NULL\n";
}
int main(){
  
  addNode(10);  
  printNodes();


  return 0;
}
