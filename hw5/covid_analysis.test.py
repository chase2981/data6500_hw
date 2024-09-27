import unittest
from unittest.mock import patch, mock_open, call
import json
from io import StringIO
import os

# Sample data for testing
mock_state_data = [
    {"date": 20201015, "positiveIncrease": 200},
    {"date": 20201016, "positiveIncrease": 300},
    {"date": 20201017, "positiveIncrease": 0},
]

# Expected results for the sample data
expected_stats = {
    "state_name": "UT",
    "average_new_daily_cases": 166.67,
    "date_with_highest_cases": 20201016,
    "most_recent_date_with_no_new_cases": 20201017,
    "month_with_highest_cases": "2020-10",
    "month_with_lowest_cases": "2020-10"
}

class TestCovidAnalysis(unittest.TestCase):

    # Mocking os.path.exists to simulate file existence check
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_state_data))
    def test_fetch_covid_data_from_file(self, mock_open_file, mock_os_path_exists):
        from covid_analysis import fetch_covid_data
        
        # Call the function
        state_code = "ut"
        result = fetch_covid_data(state_code)
        
        # Check if the file was read correctly
        mock_open_file.assert_called_once_with(f"hw5/api_results/{state_code}.json", 'r')
        
        # Assert the result matches the mocked data
        self.assertEqual(result, mock_state_data)

    # Mocking requests.get to simulate API call when the file doesn't exist
    @patch("os.path.exists", return_value=False)
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_fetch_covid_data_from_api(self, mock_open_file, mock_requests_get, mock_os_path_exists):
        from covid_analysis import fetch_covid_data
        
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_state_data
        
        # Call the function
        state_code = "ut"
        result = fetch_covid_data(state_code)
        
        # Check if the API was called correctly
        mock_requests_get.assert_called_once_with(f"https://api.covidtracking.com/v1/states/{state_code}/daily.json")
        
        # Check if the data was saved to a file
        mock_open_file.assert_called_once_with(f"hw5/api_results/{state_code}.json", 'w')
        mock_open_file().write.assert_called_once_with(json.dumps(mock_state_data, indent=4))
        
        # Assert the result matches the mocked data
        self.assertEqual(result, mock_state_data)

    def test_analyze_state_data(self):
        from covid_analysis import analyze_state_data
        
        # Call the function
        result = analyze_state_data("ut", mock_state_data)
        
        # Assert the returned statistics match the expected results
        self.assertEqual(result, expected_stats)

    # Testing the save_all_results function
    @patch("builtins.open", new_callable=mock_open)
    def test_save_all_results(self, mock_open_file):
        from covid_analysis import save_all_results
        
        mock_results = {"ut": expected_stats}
        
        # Call the function to save results
        save_all_results(mock_results)
        
        # Check if the correct file was written
        mock_open_file.assert_called_once_with("hw5/results.json", 'w')
        
        # Check the content written to the file
        mock_open_file().write.assert_called_once_with(json.dumps(mock_results, indent=4))

if __name__ == '__main__':
    unittest.main()
