import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from dynamodb import create_feedback_table
from flask import Flask, render_template, request
from lib import check_env_vars
from send_notification import notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Check environment variables before creating AWS session
try:
    check_env_vars([
        'AWS_REGION',
        'TABLE_NAME',
        'SNS_TOPIC_ARN'
    ])
    session = boto3.Session(
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE_NAME'))
except EnvironmentError as e:
    logger.error(f"Environment configuration error: {e}")
    raise

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        session = request.form['session']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if customer == '' or session == '':
            return render_template('index.html', message='Please enter required fields')
        
        try:
            # Add new feedback
            current_date = datetime.now().isoformat()
            feedback_item = {
                'customer': customer,
                'session': session,
                'rating': int(rating),
                'comments': comments,
                'created_at': current_date
            }
            logger.info(feedback_item)
            table.put_item(Item=feedback_item)
            notification(customer, session, rating, comments, current_date)
            return render_template('success.html')
        except Exception as e:
            logger.error(f"Error: {e}")
            return render_template('index.html', 
                                message='You have already submitted feedback'), 400

  
if __name__ == '__main__':
    create_feedback_table(dynamodb)
    app.run()