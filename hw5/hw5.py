import os
import requests
import json
from datetime import datetime
import os

os.system('pwd')

curr_dir = os.path.dirname(__file__)

file_path = 'hw5/states_territories.txt'

# states = []

# file1 = open(file_path)

# for line in file1.readlines():
#     # print(line)
#     states.append(line.strip())

# # print(states)

state_codes = [line.strip() for line in open(file_path).readlines()]

print(state_codes)



# List of state and territory codes
# state_codes = ['ut', 'ny', 'ca', 'tx', 'fl']  # Example state codes, update with all

# Function to get COVID data for a state
def fetch_covid_data(state_code):
    url = f"https://api.covidtracking.com/v1/states/{state_code}/daily.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        save_json(state_code, data)
        return data
    else:
        print(f"Failed to fetch data for {state_code}")
        return []

# Function to save json data into a file
def save_json(state_code, data):
    filename = f"hw5/{state_code}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Function to perform the required calculations
def analyze_state_data(state_code, data):
    state_name = state_code.upper()  # Assuming state code as name
    daily_cases = [day['positiveIncrease'] for day in data if 'positiveIncrease' in day]
    dates = [day['date'] for day in data]
    
    if not daily_cases or not dates:
        print(f"No data available for {state_code}")
        return
    
    avg_new_cases = sum(daily_cases) / len(daily_cases)
    
    # Find the date with highest cases
    max_cases = max(daily_cases)
    max_cases_date = dates[daily_cases.index(max_cases)]
    
    # Find most recent date with no new cases
    no_cases_dates = [dates[i] for i in range(len(daily_cases)) if daily_cases[i] == 0]
    most_recent_no_cases = no_cases_dates[0] if no_cases_dates else "N/A"
    
    # Calculate monthly sums
    monthly_cases = {}
    for i in range(len(daily_cases)):
        date_str = str(dates[i])
        year_month = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m')
        if year_month in monthly_cases:
            monthly_cases[year_month] += daily_cases[i]
        else:
            monthly_cases[year_month] = daily_cases[i]
    
    # Find month with highest and lowest cases
    highest_month = max(monthly_cases, key=monthly_cases.get)
    lowest_month = min(monthly_cases, key=monthly_cases.get)
    
    # Output the statistics
    print(f"State name: {state_name}")
    print(f"Average new daily cases: {avg_new_cases:.2f}")
    print(f"Date with highest cases: {max_cases_date}")
    print(f"Most recent date with no new cases: {most_recent_no_cases}")
    print(f"Month with highest cases: {highest_month}")
    print(f"Month with lowest cases: {lowest_month}")
    print('-' * 40)

# Main function to loop through states and analyze data
def main():
    for state in state_codes:
        data = fetch_covid_data(state)
        if data:
            analyze_state_data(state, data)

if __name__ == '__main__':
    main()
