# Rectangle.py
# Easy Question: Create a class called Rectangle with attributes length and width. 
# Implement a method within the class to calculate the area of the rectangle.

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width

# Instantiating the Rectangle object with length = 5 and width = 3
rect = Rectangle(5, 3)

# Print the area of the rectangle
print(f"The area of the rectangle is: {rect.area()}")

# ChatGPT session: Code generated with assistance from ChatGPT.
# Prompt: "Please write a Python program to solve the question about Rectangle class."