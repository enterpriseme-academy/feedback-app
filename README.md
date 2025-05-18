# feedback-app

Python Application for collecting feedback

export SNS_TOPIC_ARN=
export AWS_REGION="eu-west-1"
export TABLE_NAME="feedback"
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN

## Build the Docker image

docker build -t feedback-app .

## Run the container

docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxx" \
  -e AWS_SECRET_ACCESS_KEY="yyyyyyyyyyy" \
  -e AWS_SESSION_TOKEN="zzzzzzzzzzzzzzz" \
  -e SNS_TOPIC_ARN="arn:aws:sns:eu-west-1:123456789012:feedback_notifications" \
  -e TABLE_NAME="feedback" \
  -e AWS_REGION="eu-west-1" \
  feedback-app

## Run tests

python -m pytest tests/ -v