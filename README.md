[![Python application tests](https://github.com/enterpriseme-academy/feedback-app/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/enterpriseme-academy/feedback-app/actions/workflows/main.yml)
[![CodeBuild Container Build](https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiWHRTbCs5eXBzTTJVc0tRRWdNYnJkY1pQeno5ZE5iNmpjQmpSR1phd2ZDQTE3SG81QjRyb1NMb0hrbnBFc1ZwbklqOW5rcGJQcnhrajE3TTlpK2gweXpZPSIsIml2UGFyYW1ldGVyU3BlYyI6IlFHVnRmYUgvVitpQzRCKzIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

# feedback-app

Python Application for collecting feedback

```bash
export SNS_TOPIC_ARN=
export AWS_REGION="eu-west-1"
export TABLE_NAME="feedback"
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
```

## Build the Docker image

`docker build -t feedback-app .`

## Run the container

```bash
docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxx" \
  -e AWS_SECRET_ACCESS_KEY="yyyyyyyyyyy" \
  -e AWS_SESSION_TOKEN="zzzzzzzzzzzzzzz" \
  -e SNS_TOPIC_ARN="arn:aws:sns:eu-west-1:123456789012:feedback_notifications" \
  -e TABLE_NAME="feedback" \
  -e AWS_REGION="eu-west-1" \
  feedback-app
```

## Run tests

`python -m pytest tests/ -v`

