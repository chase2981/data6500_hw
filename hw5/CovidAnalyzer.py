import os
import requests
import json
from datetime import datetime
import os

os.system('pwd')

curr_dir = os.path.dirname(__file__)

class CovidAnalyzer:

    # Function to perform the required calculations and return results
    @staticmethod
    def analyze_state_data(state_code, data):
        state_name = state_code.upper()  # Assuming state code as name
        daily_cases = [day['positiveIncrease'] for day in data if 'positiveIncrease' in day]
        dates = [day['date'] for day in data]

        if not daily_cases or not dates:
            print(f"No data available for {state_code}")
            return None

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

        # Prepare statistics as a dictionary
        stats = {
            "state_name": state_name,
            "average_new_daily_cases": round(avg_new_cases, 2),
            "date_with_highest_cases": max_cases_date,
            "most_recent_date_with_no_new_cases": most_recent_no_cases,
            "month_with_highest_cases": highest_month,
            "month_with_lowest_cases": lowest_month
        }

        return stats


    # Function to get COVID data for a state (checks if the file exists first)
    @staticmethod
    def fetch_covid_data(state_code):
        filename = f"hw5/api_results/{state_code}.json"

        # Check if the JSON file already exists
        if os.path.exists(filename):
            print(f"Loading data for {state_code} from {filename}")
            with open(filename, 'r') as f:
                data = json.load(f)
            return data
        else:
            print(f"Fetching data for {state_code} from API")
            url = f"https://api.covidtracking.com/v1/states/{state_code}/daily.json"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                CovidAnalyzer.save_json(state_code, data)  # Save data to a JSON file
                return data
            else:
                print(f"Failed to fetch data for {state_code}")
                return []


    # Function to save JSON data into a file
    @staticmethod
    def save_json(state_code, data):
        filename = f"hw5/api_results/{state_code}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


    # Function to save all the results into a single JSON file
    @staticmethod
    def save_all_results(results):
        filename = "hw5/results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"All results saved to {filename}")