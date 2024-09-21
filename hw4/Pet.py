# Pet.py
# Hard Question: Create a class called Pet with attributes name and age.
# Implement a method to calculate the age of the pet in equivalent human years.
# Create a Species class to handle species-specific behavior and average lifespan.

class Species:
    # Class for species and their average lifespan
    species_avg_lifespan = {
        "dog": 13,
        "cat": 15,
        "rabbit": 10,
        "bird": 5
    }
    
    def __init__(self, species_name):
        self.species_name = species_name
    
    def get_avg_lifespan(self):
        # Method to get the average lifespan for the species
        return Species.species_avg_lifespan.get(self.species_name, "Unknown species")
    
    def convert_to_human_years(self, pet_age):
        # Convert pet's age to human years based on species
        if self.species_name == "dog":
            return pet_age * 7
        elif self.species_name == "cat":
            return pet_age * 6
        else:
            return pet_age * 5  # Default for other pets

class Pet:
    def __init__(self, name, age, species_name):
        self.name = name
        self.age = age
        self.species = Species(species_name)  # Link to Species class
    
    def age_in_human_years(self):
        # Use species class to calculate human years equivalent
        return self.species.convert_to_human_years(self.age)
    
    def get_avg_lifespan(self):
        # Use species class to get average lifespan
        return self.species.get_avg_lifespan()

# Instantiating three Pet objects with different names, ages, and species
pet1 = Pet("Buddy", 3, "dog")
pet2 = Pet("Whiskers", 5, "cat")
pet3 = Pet("Fluffy", 2, "rabbit")

# Calculating and printing the age of each pet in human years
print(f"{pet1.name}'s age in human years: {pet1.age_in_human_years()}")
print(f"{pet2.name}'s age in human years: {pet2.age_in_human_years()}")
print(f"{pet3.name}'s age in human years: {pet3.age_in_human_years()}")

# Retrieving and printing the average lifespan for each pet's species
print(f"{pet1.name}'s species average lifespan: {pet1.get_avg_lifespan()} years")
print(f"{pet2.name}'s species average lifespan: {pet2.get_avg_lifespan()} years")
print(f"{pet3.name}'s species average lifespan: {pet3.get_avg_lifespan()} years")

# ChatGPT session: Code generated with assistance from ChatGPT.
# Prompt: "Please write a Python program to solve the question about Pet class with Species handling human years and lifespan."

# https://chatgpt.com/share/66ee2198-3e2c-8002-98d3-d65a5383a109