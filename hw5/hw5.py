import os
import requests
import json
from datetime import datetime
import os

from CovidAnalyzer import CovidAnalyzer

os.system('pwd')

curr_dir = os.path.dirname(__file__)


# Main function to loop through states, analyze data, and save results
def main():
    all_results = {}

    file_path = 'hw5/states_territories.txt'

    state_codes = [line.strip() for line in open(file_path).readlines()]

    print(state_codes)
    
    for state in state_codes:
        data = CovidAnalyzer.fetch_covid_data(state)
        if data:
            stats = CovidAnalyzer.analyze_state_data(state, data)
            if stats:
                all_results[state] = stats
    
    # Save all results into a single JSON file
    CovidAnalyzer.save_all_results(all_results)

if __name__ == '__main__':
    main()
