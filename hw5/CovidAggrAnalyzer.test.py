import os
import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO

# Mock data for testing
mock_results = {
    "ut": {
        "state_name": "UT",
        "average_new_daily_cases": 257.56,
        "date_with_highest_cases": 20201015,
        "most_recent_date_with_no_new_cases": 20210502,
        "month_with_highest_cases": "2020-10",
        "month_with_lowest_cases": "2021-06"
    },
    "ny": {
        "state_name": "NY",
        "average_new_daily_cases": 1200.75,
        "date_with_highest_cases": 20200330,
        "most_recent_date_with_no_new_cases": "N/A",
        "month_with_highest_cases": "2020-03",
        "month_with_lowest_cases": "2021-07"
    }
}

# Expected aggregated stats based on the mock data
expected_aggregated_stats = {
    "overall_avg_daily_cases": 729.15,
    "state_with_highest_avg_daily_cases": {
        "state": "ny",
        "avg_cases": 1200.75
    },
    "state_with_lowest_avg_daily_cases": {
        "state": "ut",
        "avg_cases": 257.56
    },
    "month_with_highest_cases": "2020-10",
    "month_with_lowest_cases": "2021-06",
    "state_with_most_zero_case_days": "ut"
}

results_path = os.path.join('hw5', 'results.json')
results_aggr_path = os.path.join('hw5', 'results-aggr.json')


class TestCovidAggregation(unittest.TestCase):
    
    # Mocking os.path.exists and open to test loading the results.json file
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_results))
    def test_load_results(self, mock_open_file):
        from covid_analysis_aggr import load_results
        
        # Call the function
        results = load_results()
        
        # Assert the file was opened and the data matches the mock results
        mock_open_file.assert_called_once_with(results_path, 'r')
        self.assertEqual(results, mock_results)
    
    # Test the compute_cross_state_stats function with mock results
    def test_compute_cross_state_stats(self):
        from covid_analysis_aggr import compute_cross_state_stats
        
        # Call the function with mock data
        stats = compute_cross_state_stats(mock_results)
        
        # Assert the aggregated statistics match the expected results
        # self.assertEqual(aggregated_stats, expected_aggregated_stats)

        # Validate the overall average daily cases
        self.assertEqual(stats['overall_avg_daily_cases'], 729.15)
        
        # Validate the state with the highest and lowest average cases
        self.assertEqual(stats['state_with_highest_avg_daily_cases']['state'], 'ny')
        self.assertEqual(stats['state_with_lowest_avg_daily_cases']['state'], 'ut')
        
        # Validate the months with highest and lowest cases
        self.assertEqual(stats['month_with_highest_cases'], "2020-10")
        self.assertEqual(stats['month_with_lowest_cases'], "2021-06")  
          
    # Mocking open to test saving aggregated statistics to a file
    @patch("builtins.open", new_callable=mock_open)
    def test_save_aggregated_stats(self, mock_open_file):
        from covid_analysis_aggr import save_aggregated_stats
        
        # Call the function to save the aggregated stats
        save_aggregated_stats(expected_aggregated_stats)
        
        # Check if the correct file was written to
        mock_open_file.assert_called_once_with(results_aggr_path, 'w')
        
        # Get the content that was written to the file
        written_content = mock_open_file().write.call_args[0][0]
        
        # Assert the written content matches the expected aggregated stats
        self.assertEqual(json.loads(written_content), expected_aggregated_stats)


if __name__ == '__main__':
    unittest.main()
