import json
from collections import defaultdict
from hw5.CovidAggrAnalyzer import CovidAggrAnalyzer


def main():
    # Load the results from results.json
    results = CovidAggrAnalyzer.load_results()
    
    # Compute and save cross-state statistics
    aggregated_stats = CovidAggrAnalyzer.compute_cross_state_stats(results)

    # Save the aggregated stats to a file
    CovidAggrAnalyzer.save_aggregated_stats(aggregated_stats)

if __name__ == '__main__':
    main()
