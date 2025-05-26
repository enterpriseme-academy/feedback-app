import os

os.environ['SNS_TOPIC_ARN'] = "arn:aws:sns:eu-west-1:123456789012:test-topic"
os.environ['AWS_REGION'] = "eu-west-1"
os.environ['TABLE_NAME'] = "feedback-table"