import json
from collections import defaultdict

# Load the saved results.json file
def load_results():
    with open('hw5/results.json', 'r') as f:
        data = json.load(f)
    return data

# Function to compute cross-state statistics
def compute_cross_state_stats(results):
    total_avg_daily_cases = 0
    state_count = len(results)
    state_with_highest_avg = None
    state_with_lowest_avg = None
    highest_avg_cases = float('-inf')
    lowest_avg_cases = float('inf')
    
    # Dictionary to hold monthly case sums across all states
    monthly_case_sums = defaultdict(int)
    
    # Track the state with the most days with zero new cases
    zero_case_days = defaultdict(int)
    
    for state_code, stats in results.items():
        avg_cases = stats['average_new_daily_cases']
        
        # Sum the average new daily cases across all states
        total_avg_daily_cases += avg_cases
        
        # Identify state with highest average daily cases
        if avg_cases > highest_avg_cases:
            highest_avg_cases = avg_cases
            state_with_highest_avg = state_code
        
        # Identify state with lowest average daily cases
        if avg_cases < lowest_avg_cases:
            lowest_avg_cases = avg_cases
            state_with_lowest_avg = state_code
        
        # Sum cases for each month across all states
        highest_month = stats['month_with_highest_cases']
        lowest_month = stats['month_with_lowest_cases']
        monthly_case_sums[highest_month] += avg_cases
        monthly_case_sums[lowest_month] += avg_cases
        
        # Count zero case days for this state
        most_recent_no_cases = stats['most_recent_date_with_no_new_cases']
        if most_recent_no_cases != "N/A":
            zero_case_days[state_code] += 1
    
    # Calculate the overall average daily cases across states
    overall_avg_daily_cases = total_avg_daily_cases / state_count
    
    # Find the months with the highest and lowest total cases across states
    month_with_highest_cases = max(monthly_case_sums, key=monthly_case_sums.get)
    month_with_lowest_cases = min(monthly_case_sums, key=monthly_case_sums.get)
    
    # Find the state with the most days with zero new cases
    state_with_most_zero_cases = max(zero_case_days, key=zero_case_days.get) if zero_case_days else "N/A"

    print(f"Overall average daily cases across states: {overall_avg_daily_cases:.2f}")
    print(f"State with highest average daily cases: {state_with_highest_avg} ({highest_avg_cases:.2f})")
    print(f"State with lowest average daily cases: {state_with_lowest_avg} ({lowest_avg_cases:.2f})")
    print(f"Month with highest cases across states: {month_with_highest_cases}")
    print(f"Month with lowest cases across states: {month_with_lowest_cases}")
    print(f"State with most days of zero new cases: {state_with_most_zero_cases}")
    
    # Create a dictionary to store the aggregated statistics
    aggregated_stats = {
        "overall_avg_daily_cases": round(overall_avg_daily_cases, 2),
        "state_with_highest_avg_daily_cases": {
            "state": state_with_highest_avg,
            "avg_cases": round(highest_avg_cases, 2)
        },
        "state_with_lowest_avg_daily_cases": {
            "state": state_with_lowest_avg,
            "avg_cases": round(lowest_avg_cases, 2)
        },
        "month_with_highest_cases": month_with_highest_cases,
        "month_with_lowest_cases": month_with_lowest_cases,
        "state_with_most_zero_case_days": state_with_most_zero_cases
    }

    return aggregated_stats

# Function to save aggregated statistics into results-aggr.json
def save_aggregated_stats(aggregated_stats):
    filename = "hw5/results-aggr.json"
    with open(filename, 'w') as f:
        json.dump(aggregated_stats, f, indent=4)
    print(f"Aggregated statistics saved to {filename}")

def main():
    # Load the results from results.json
    results = load_results()
    
    # Compute and save cross-state statistics
    aggregated_stats = compute_cross_state_stats(results)

    # Save the aggregated stats to a file
    save_aggregated_stats(aggregated_stats)

if __name__ == '__main__':
    main()
