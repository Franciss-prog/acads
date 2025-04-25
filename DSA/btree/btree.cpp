#include <iostream>
#include <queue>
#include <set>
using namespace std;

// Node structure
struct Node {
    int data;
    Node* left;
    Node* right;

    Node(int value) {
        data = value;
        left = right = nullptr;
    }
};

// Insert in level-order to make a simple binary tree
Node* insertLevelOrder(const int values[], int n) {
    if (n == 0) return nullptr;

    Node* root = new Node(values[0]);
    queue<Node*> q;
    q.push(root);

    int i = 1;
    while (i < n) {
        Node* current = q.front();
        q.pop();

        if (i < n) {
            current->left = new Node(values[i++]);
            q.push(current->left);
        }

        if (i < n) {
            current->right = new Node(values[i++]);
            q.push(current->right);
        }
    }

    return root;
}

// Show parent-child relationships
void showParentChild(Node* root) {
    if (!root) return;

    if (root->left)
        cout << "Parent: " << root->data << " -> Left Child: " << root->left->data << endl;
    if (root->right)
        cout << "Parent: " << root->data << " -> Right Child: " << root->right->data << endl;

    showParentChild(root->left);
    showParentChild(root->right);
}

// Depth of each node
void showDepth(Node* root, int depth = 0) {
    if (!root) return;
    cout << "Node: " << root->data << " | Depth: " << depth << endl;
    showDepth(root->left, depth + 1);
    showDepth(root->right, depth + 1);
}

// Count total nodes
int countNodes(Node* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

// Get height of tree
int treeHeight(Node* root) {
    if (!root) return -1;
    return 1 + max(treeHeight(root->left), treeHeight(root->right));
}

int main() {
    int values[] = {12, 19, 10, 28, 1, 69, 39, 29, 81, 75, 8, 0, 50, 30, 11, 20};
    int n = sizeof(values) / sizeof(values[0]);

    Node* root = insertLevelOrder(values, n);

    cout << "\n--- Binary Tree Info ---\n";
    cout << "Root Node: " << root->data << endl;

    cout << "\nParent-Child Relationships:\n";
    showParentChild(root);

    cout << "\nDepth of Each Node:\n";
    showDepth(root);

    cout << "\nTotal Number of Nodes: " << countNodes(root) << endl;
    cout << "Height of the Tree: " << treeHeight(root)+1 << endl;

    return 0;
}
