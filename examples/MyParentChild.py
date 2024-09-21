class Building:
    def __init__(self, year, sq_footage, original_price):
        self.sq_footage = sq_footage
        self.year = year
        self.original_price = original_price
        
    def current_value(self, current_year):
        return self.original_price * (1.1 ** (current_year - self.year))
        
        
andys_building = Building(2017, 1800, 450000)

print("andys_building value:", andys_building.current_value(2024))

class ResidentialBuilding(Building):
    def current_value(self, current_year):
        return self.original_price * (1.2 ** (current_year - self.year))

class CommercialBuilding(Building):
    def current_value(self, current_year):
        return self.original_price * (1.2 ** (current_year - self.year))
        
        
chases_building = CommercialBuilding(2010, 2710, 450000)

print("chases building value: ", chases_building.current_value(2024))

#Polymorphism

building_portfolio = [andys_building, chases_building]

total_value = 0.0

for building in building_portfolio:
    total_value += building.current_value(2024)
    print(type(building))
    
print("all buildings value: ", total_value)

