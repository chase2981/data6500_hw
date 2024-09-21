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
rect2 = Rectangle(2, 3)
rect3 = Rectangle(50, 90)

# Print the area of the rectangle
print(f"The area of the rectangle is: {rect.area()}")
print(f"The area of the rectangle2 is: {rect2.area()}")
print(f"The area of the rectangle3 is: {rect3.area()}")

# ChatGPT session: Code generated with assistance from ChatGPT.
# Prompt: "Please write a Python program to solve the question about Rectangle class."