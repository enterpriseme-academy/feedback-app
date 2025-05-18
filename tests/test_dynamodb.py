import logging
import unittest
from unittest.mock import Mock, patch

from botocore.exceptions import ClientError
from dynamodb import create_feedback_table


class TestCreateFeedbackTable(unittest.TestCase):
    def setUp(self):
        self.mock_dynamodb = Mock()
        self.mock_table = Mock()
        self.mock_dynamodb.create_table.return_value = self.mock_table

    def test_create_table_success(self):
        # Arrange
        expected_params = {
            'TableName': 'Feedback',
            'KeySchema': [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'customer',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'customer',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }

        create_feedback_table(self.mock_dynamodb)

        self.mock_dynamodb.create_table.assert_called_once_with(**expected_params)
        self.mock_table.wait_until_exists.assert_called_once()

    def test_create_table_already_exists(self):
        error_response = {
            'Error': {
                'Code': 'ResourceInUseException',
                'Message': 'Table already exists'
            }
        }
        self.mock_dynamodb.create_table.side_effect = ClientError(
            error_response, 'CreateTable')

        with self.assertLogs(level='INFO') as captured:
            create_feedback_table(self.mock_dynamodb)
            self.assertIn("Table already exists", captured.records[0].getMessage())

    def test_create_table_unexpected_error(self):
        error_response = {
            'Error': {
                'Code': 'UnexpectedError',
                'Message': 'Something went wrong'
            }
        }
        self.mock_dynamodb.create_table.side_effect = ClientError(
            error_response, 'CreateTable')

        with self.assertLogs(level='ERROR') as captured:
            create_feedback_table(self.mock_dynamodb)
            self.assertIn("Unexpected error", captured.records[0].getMessage())
