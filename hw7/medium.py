# Medium Task: Searching for a value in a Binary Search Tree
# ChatGPT Prompt: "How do I search for a value in a binary search tree in Python?"
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

def search_bst(root, value):
    if root is None:
        return False
    if root.value == value:
        return True
    elif value < root.value:
        return search_bst(root.left, value)
    else:
        return search_bst(root.right, value)

# Example usage:
root = TreeNode(10)
root = insert_bst(root, 5)
root = insert_bst(root, 15)
root = insert_bst(root, 3)
root = insert_bst(root, 7)
root = insert_bst(root, 12)
root = insert_bst(root, 18)

# Display the tree
display(root)

# Search for values in the tree
print(search_bst(root, 7))  # Returns True
print(search_bst(root, 12)) # Returns True
print(search_bst(root, 20)) # Returns False
