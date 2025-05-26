import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import os
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        # Test the index route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.table')
    @patch('app.notification')
    def test_submit_success(self, mock_notification, mock_table):
        # Arrange
        test_data = {
            'customer': 'John Doe',
            'session': 'Network',
            'rating': '5',
            'comments': 'Great session!'
        }
        mock_table.put_item.return_value = {}
        mock_notification.return_value = {}

        # Act
        response = self.app.post('/submit', data=test_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_table.put_item.assert_called_once()
        mock_notification.assert_called_once()

    def test_submit_missing_fields(self):
        # Test submission with missing required fields
        test_data = {
            'customer': '',
            'session': '',
            'rating': '5',
            'comments': 'Great session!'
        }
        response = self.app.post('/submit', data=test_data)
        self.assertIn(b'Please enter required fields', response.data)

    @patch('app.table')
    def test_submit_database_error(self, mock_table):
        # Arrange
        test_data = {
            'customer': 'John Doe',
            'session': 'Network',
            'rating': '5',
            'comments': 'Great session!'
        }
        mock_table.put_item.side_effect = Exception('Database error')

        # Act
        response = self.app.post('/submit', data=test_data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'You have already submitted feedback', response.data)

if __name__ == '__main__':
    unittest.main()