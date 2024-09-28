import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
import os

# Mock data for testing
mock_state_data = [
    {"date": 20200915, "positiveIncrease": 301},
    {"date": 20201015, "positiveIncrease": 200},
    {"date": 20201016, "positiveIncrease": 300},
    {"date": 20201017, "positiveIncrease": 0},
]

# Expected results for the mock state data
expected_stats = {
    "state_name": "UT",
    "average_new_daily_cases": 166.67,
    "date_with_highest_cases": 20201016,
    "most_recent_date_with_no_new_cases": 20201017,
    "month_with_highest_cases": "2020-10",
    "month_with_lowest_cases": "2020-10"
}


class TestCovidAnalyzer(unittest.TestCase):

    # Test analyze_state_data function
    def test_analyze_state_data(self):
        from CovidAnalyzer import CovidAnalyzer

        # Call the function with mock data
        result = CovidAnalyzer.analyze_state_data("ut", mock_state_data)

        # Validate
        self.assertEqual(result['state_name'], "UT")
        self.assertEqual(result['average_new_daily_cases'], sum([day['positiveIncrease'] for day in mock_state_data]) / len(mock_state_data))
        self.assertEqual(result['date_with_highest_cases'], 20200915)
        self.assertEqual(result['most_recent_date_with_no_new_cases'], 20201017)
        self.assertEqual(result['month_with_highest_cases'], "2020-10")
        self.assertEqual(result['month_with_lowest_cases'], "2020-09")

        # # Assert that the result matches the expected statistics
        # self.assertEqual(result, expected_stats)

    # Mocking os.path.exists and open to test fetch_covid_data loading from file
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_state_data))
    def test_fetch_covid_data_from_file(self, mock_open_file, mock_os_path_exists):
        from CovidAnalyzer import CovidAnalyzer
        
        # Adjust file path to use os.path.join
        state_code = "ut"
        filename = os.path.join('hw5', 'api_results', f'{state_code}.json')
        
        # Call the function
        result = CovidAnalyzer.fetch_covid_data(state_code)
        
        # Assert the file was opened with the correct path and mode
        mock_open_file.assert_called_once_with(filename, 'r')
        
        # Assert the result matches the mock state data
        self.assertEqual(result, mock_state_data)

    # Mocking requests.get to simulate API call when file doesn't exist
    @patch("os.path.exists", return_value=False)
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_fetch_covid_data_from_api(self, mock_open_file, mock_requests_get, mock_os_path_exists):
        from CovidAnalyzer import CovidAnalyzer
        
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_state_data
        
        state_code = "ut"
        filename = os.path.join('hw5', 'api_results', f'{state_code}.json')
        
        # Call the function
        result = CovidAnalyzer.fetch_covid_data(state_code)
        
        # Assert the API call was made with the correct URL
        mock_requests_get.assert_called_once_with(f"https://api.covidtracking.com/v1/states/{state_code}/daily.json")
        
        # Assert that the data was saved into the correct file
        mock_open_file.assert_called_once_with(filename, 'w')
        # mock_open_file().write.assert_called_once_with(json.dumps(mock_state_data, indent=4))
        
        # Assert the result matches the mock state data
        self.assertEqual(result, mock_state_data)

    # Test save_json function by checking if it writes the correct data to the file
    @patch("builtins.open", new_callable=mock_open)
    def test_save_json(self, mock_open_file):
        from CovidAnalyzer import CovidAnalyzer
        
        state_code = "ut"
        filename = os.path.join('hw5', 'api_results', f'{state_code}.json')
        
        # Call the function to save data
        CovidAnalyzer.save_json(state_code, mock_state_data)
        
        # Assert that the file was opened with the correct path and mode
        mock_open_file.assert_called_once_with(filename, 'w')
        
        # Assert the correct content was written to the file
        # mock_open_file().write.assert_called_once_with(json.dumps(mock_state_data, indent=4))

    # Test save_all_results function by checking if it writes the correct aggregated results to the file
    @patch("builtins.open", new_callable=mock_open)
    def test_save_all_results(self, mock_open_file):
        from CovidAnalyzer import CovidAnalyzer

        mock_results = {"ut": expected_stats}
        results_filename = os.path.join('hw5', 'results.json')
        
        # Call the function to save results
        CovidAnalyzer.save_all_results(mock_results)
        
        # Assert that the file was opened with the correct path and mode
        mock_open_file.assert_called_once_with(results_filename, 'w')

        # Get all calls to write and combine them into a single string
        # written_content = "".join(call.args[0] for call in mock_open_file().write.call_args_list)

        # Assert the combined written content matches the expected JSON output
        # self.assertEqual(written_content, json.dumps(mock_results, indent=4))
        
        # Assert the correct content was written to the file
        # mock_open_file().write.assert_called_with(json.dumps(mock_results, indent=4))


if __name__ == '__main__':
    unittest.main()
