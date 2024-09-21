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
emp2 = Employee("Chase", 100000)

# Increasing the salary by 10%
emp.increase_salary(10)

# Increasing the salary by 50%
emp2.increase_salary(50)

# Print the updated salaries
print(f"Updated salary for {emp.name}: {emp.salary}")
print(f"Updated salary for {emp2.name}: {emp2.salary}")

# ChatGPT session: Code generated with assistance from ChatGPT.
# Prompt: "Please write a Python program to solve the question about Employee class salary increase."