# Easy Task: Inserting a value into a Binary Search Tree
# ChatGPT Prompt: "How can I write a function to insert a value into a binary search tree in Python?"
from print_tree import display

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert_bst(root, value):
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert_bst(root.left, value)
    else:
        root.right = insert_bst(root.right, value)
    return root

# Example usage:
root = TreeNode(10)
insert_bst(root, 5)
insert_bst(root, 15)
display(root)
