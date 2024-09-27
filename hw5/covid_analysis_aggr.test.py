import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
import os

# Example mock data for testing
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

# Sample mock aggregated results for testing the saving functionality
mock_aggregated_stats = {
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

# Mock json data as string
mock_results_json = json.dumps(mock_results)
# Path to the results-aggr.json file using os.path.join for compatibility
results_json_path = os.path.join('hw5', 'results.json')
results_aggr_json_path = os.path.join('hw5', 'results-aggr.json')

class TestCovidAnalysis(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open, read_data=mock_results_json)
    def test_load_results(self, mock_file):
        from covid_analysis_aggr import load_results
        
        # Load the results
        results = load_results()
        
        # Check that the results match the mock data
        self.assertEqual(results, mock_results)
        mock_file.assert_called_once_with(results_json_path, 'r')

    def test_compute_cross_state_stats(self):
        from covid_analysis_aggr import compute_cross_state_stats
        
        # Capture the function's print statements to validate them
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Perform the cross-state analysis
            stats = compute_cross_state_stats(mock_results)
            
            # Validate the overall average daily cases
            self.assertEqual(stats['overall_avg_daily_cases'], 729.15)
            
            # Validate the state with the highest and lowest average cases
            self.assertEqual(stats['state_with_highest_avg_daily_cases']['state'], 'ny')
            self.assertEqual(stats['state_with_lowest_avg_daily_cases']['state'], 'ut')
            
            # Validate the months with highest and lowest cases
            self.assertEqual(stats['month_with_highest_cases'], "2020-10")
            self.assertEqual(stats['month_with_lowest_cases'], "2021-06")
            
    # @patch("builtins.open", new_callable=mock_open)
    # def test_save_aggregated_stats(self, mock_file):
    #     from covid_analysis_aggr import save_aggregated_stats
    #
    #     # Save the mock aggregated stats to a file
    #     save_aggregated_stats(mock_aggregated_stats)
    #
    #     # Check that the file was opened and written to correctly
    #     mock_file.assert_called_once_with('hw5/results-aggr.json', 'w')
    #
    #     # Get the actual content written to the file
    #     written_content = mock_file().write.call_args[0][0]
    #
    #     # Verify the content matches the mock aggregated stats
    #     self.assertEqual(json.loads(written_content), mock_aggregated_stats)


    @patch("builtins.open", new_callable=mock_open)
    def test_save_aggregated_stats(self, mock_file):
        from covid_analysis_aggr import save_aggregated_stats
        
        # Save the mock aggregated stats to a file
        save_aggregated_stats(mock_aggregated_stats)
        
        # Verify the correct file was opened
        mock_file.assert_called_once_with(results_aggr_json_path, 'w')
        
        # Check the actual content written to the file
        written_content = mock_file().write.call_args[0][0]
        
        # Validate the written content
        self.assertEqual(json.loads(written_content), mock_aggregated_stats)

if __name__ == '__main__':
    unittest.main()
