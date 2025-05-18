import json
import os

import boto3
from botocore.exceptions import ClientError


def notification(participant, session, rating, comments, current_date):
    # Create an SNS client
    sns = boto3.client('sns',
        region_name=os.environ.get('AWS_REGION', 'eu-west-1'),
    )

    # Create HTML message
    html_message = f"""
    New Feedback Submission
     
    - Participant: {participant}
    - Session: {session}
    - Rating: {rating}
    - Comments: {comments}
    - Sent At: {current_date}
    """

    # Create message structure with HTML formatting
    message = {
        "default": f"New feedback from {participant}",
        "email": html_message,
        "sms": f"New feedback from {participant}: Rating {rating}/5"
    }

    try:
        response = sns.publish(
            TopicArn=os.environ.get('SNS_TOPIC_ARN'),
            Message=json.dumps(message),
            Subject='New Feedback Submission',
            MessageStructure='json'
        )
        return response
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None