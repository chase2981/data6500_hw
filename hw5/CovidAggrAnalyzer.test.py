import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
import os

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

class TestCovidAggrAnalyzer(unittest.TestCase):
    
    # Test load_results method by mocking file open
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_results))
    def test_load_results(self, mock_open_file):
        from CovidAggrAnalyzer import CovidAggrAnalyzer
        
        # Adjust file path to use os.path.join
        results_filename = os.path.join('hw5', 'results.json')

        # Call the load_results function
        result = CovidAggrAnalyzer.load_results()

        # Assert the file was opened with the correct path and mode
        mock_open_file.assert_called_once_with(results_filename, 'r')
        
        # Assert the loaded data matches the mock results
        self.assertEqual(result, mock_results)
    
    # Test compute_cross_state_stats method with mock data
    def test_compute_cross_state_stats(self):
        from CovidAggrAnalyzer import CovidAggrAnalyzer
        
        # Call the function with mock data
        aggregated_stats = CovidAggrAnalyzer.compute_cross_state_stats(mock_results)

        # Validate the overall average daily cases
        # sum(state['average_new_daily_cases'] for state in mock_results.values()) / len(mock_results)
        self.assertEqual(aggregated_stats['overall_avg_daily_cases'], 729.15)
        
        # Validate the state with the highest and lowest average cases
        self.assertEqual(aggregated_stats['state_with_highest_avg_daily_cases']['state'], 'ny')
        self.assertEqual(aggregated_stats['state_with_lowest_avg_daily_cases']['state'], 'ut')
        
        # Validate the months with highest and lowest cases
        self.assertEqual(aggregated_stats['month_with_highest_cases'], "2020-10")
        self.assertEqual(aggregated_stats['month_with_lowest_cases'], "2021-06")
        
        # Assert that the computed stats match the expected aggregated stats
        # self.assertEqual(aggregated_stats, expected_aggregated_stats)
    
    # Test save_aggregated_stats by mocking file writing
    @patch("builtins.open", new_callable=mock_open)
    def test_save_aggregated_stats(self, mock_open_file):
        from CovidAggrAnalyzer import CovidAggrAnalyzer

        # Adjust file path to use os.path.join
        results_aggr_path = os.path.join('hw5', 'results-aggr.json')

        # Call the function to save the aggregated stats
        CovidAggrAnalyzer.save_aggregated_stats(expected_aggregated_stats)

        # Assert that the file was opened with the correct path and mode
        mock_open_file.assert_called_once_with(results_aggr_path, 'w')

        # # Combine all the write calls into a single string
        # written_content = "".join(call.args[0] for call in mock_open_file().write.call_args_list)
        #
        # # Assert that the content written to the file matches the expected JSON output
        # self.assertEqual(written_content, json.dumps(expected_aggregated_stats, indent=4))


if __name__ == '__main__':
    unittest.main()
