from django.db import models
import boto3
import os
import logging

STARTUP_SIGNUP_TABLE = os.environ['STARTUP_SIGNUP_TABLE']
AWS_REGION = os.environ['AWS_REGION']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']


logger = logging.getLogger(__name__)


class Leads(models.Model):

    def insert_lead(self, name, email, previewAccess):
        try:
            dynamodb = boto3.resource('dynamodb',
                                      region_name=AWS_REGION,
                                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                      aws_session_token=AWS_SESSION_TOKEN )
            table = dynamodb.Table(STARTUP_SIGNUP_TABLE)
        except Exception as e:
            logger.error(
                'Error connecting to database table: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
            return 403
        try:
            response = table.put_item(
                Item={
                    'name': name,
                    'email': email,
                    'preview': previewAccess,
                },
                ReturnValues='ALL_OLD',
            )
        except Exception as e:
            logger.error(
                'Error adding item to database: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
            return 403
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status == 200:
            if 'Attributes' in response:
                logger.error('Existing item updated to database.')
                return 409
            logger.error('New item added to database.')
        else:
            logger.error('Unknown error inserting item to database.')

        return status
