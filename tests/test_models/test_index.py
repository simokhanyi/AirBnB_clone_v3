#!/usr/bin/python3
"""
Contains the TestIndex classes
"""

import unittest
from unittest.mock import patch
from index import app_views


class TestGetStats(unittest.TestCase):
    """Test get_stats endpoint"""

    @patch('index.storage')
    def test_get_stats(self, mock_storage):
        """Test get_stats() function"""

        # Mocking count method of storage object
        mock_storage.count.side_effect = lambda arg: {"Amenity": 5,
                                                      "City": 10,
                                                      "Place": 15,
                                                      "Review": 20,
                                                      "State": 25,
                                                      "User": 30}[arg]

        # Making a test client
        tester = app_views.test_client(self)

        # Getting response from the endpoint
        response = tester.get('/stats')

        # Checking if the status code is 200
        self.assertEqual(response.status_code, 200)

        # Checking if the response data matches expected data
        expected_data = {
            "amenities": 5,
            "cities": 10,
            "places": 15,
            "reviews": 20,
            "states": 25,
            "users": 30
        }
        self.assertEqual(response.json, expected_data)


if __name__ == '__main__':
    unittest.main()
