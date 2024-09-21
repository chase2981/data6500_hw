# Employee.py
# Medium Question: Create a class called Employee with attributes name and salary.
# Implement a method within the class that increases the salary of the employee by a given percentage.

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def increase_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)

# Instantiating the Employee object with name = "John" and salary = 5000
emp = Employee("John", 5000)

# Increasing the salary by 10%
emp.increase_salary(10)

# Print the updated salary
print(f"Updated salary for {emp.name}: {emp.salary}")

# ChatGPT session: Code generated with assistance from ChatGPT.
# Prompt: "Please write a Python program to solve the question about Employee class salary increase."