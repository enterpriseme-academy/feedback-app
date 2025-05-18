import json
import os
import unittest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from send_notification import notification


class TestNotification(unittest.TestCase):
    def setUp(self):
        self.participant = "John Doe"
        self.session = "Network"
        self.rating = 5
        self.comments = "Great session!"
        self.current_date = "2025-05-18T10:00:00"
        self.topic_arn = "arn:aws:sns:eu-west-1:123456789012:test-topic"
        # Mock environment variable
        os.environ['SNS_TOPIC_ARN'] = self.topic_arn
        
    @patch('boto3.client')
    def test_notification_success(self, mock_boto3_client):

        mock_sns = Mock()
        mock_boto3_client.return_value = mock_sns
        mock_sns.publish.return_value = {'MessageId': '1234567890'}

        expected_message = {
            "default": f"New feedback from {self.participant}",
            "email": f"""
    New Feedback Submission
     
    - Participant: {self.participant}
    - Session: {self.session}
    - Rating: {self.rating}
    - Comments: {self.comments}
    - Sent At: {self.current_date}
    """,
            "sms": f"New feedback from {self.participant}: Rating {self.rating}/5"
        }

        result = notification(
            self.participant, 
            self.session, 
            self.rating, 
            self.comments, 
            self.current_date
        )

        mock_sns.publish.assert_called_once_with(
            TopicArn=self.topic_arn,  # Use mocked topic ARN
            Message=json.dumps(expected_message),
            Subject='New Feedback Submission',
            MessageStructure='json'
        )
        self.assertEqual(result, {'MessageId': '1234567890'})

    @patch('boto3.client')
    def test_notification_error(self, mock_boto3_client):
        # Arrange
        mock_sns = Mock()
        mock_boto3_client.return_value = mock_sns
        error_response = {
            'Error': {
                'Code': 'InvalidParameter',
                'Message': 'Invalid parameter'
            }
        }
        mock_sns.publish.side_effect = ClientError(error_response, 'Publish')

        result = notification(
            self.participant, 
            self.session, 
            self.rating, 
            self.comments, 
            self.current_date
        )

        self.assertIsNone(result)

    def tearDown(self):
        # Clean up environment variable after test
        if 'SNS_TOPIC_ARN' in os.environ:
            del os.environ['SNS_TOPIC_ARN']
