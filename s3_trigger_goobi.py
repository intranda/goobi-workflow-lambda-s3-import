#!/usr/bin/env python
"""Receives an AWS S3 event and calls the Goobi Workflow API accordingly, to import the uploaded data"""

import json
import urllib.parse
import boto3
import requests
import logging
import os

api_endpoint = os.environ["API_ENDPOINT"]
token = os.environ["TOKEN"]
templateid = os.environ["TEMPLATEID"]
update_templateid = os.environ["UPDATETEMPLATEID"]
hotfolder = os.environ["HOTFOLDER"]


headers = {'token': token}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Loading function")


def lambda_handler(event, context):
    logger.debug('Received event: ' + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        data = {'key': key,
                'bucket': bucket,
                'templateid': templateid,
                'updatetemplateid': update_templateid,
                'hotfolder': hotfolder}
        r = requests.post(url=api_endpoint, headers=headers, json=data)
        r.raise_for_status()
        logger.info(r.text)
        return r.text
    except Exception as e:
        logger.error('Received error %s', r.text)
        logger.exception(e)
        try:
            s3 = boto3.resource('s3')
            s3.Object(bucket, "failed/" +
                      key).copy_from(CopySource=bucket+"/"+key)
            s3.Object(bucket, key).delete()
            logger.info('moved %s to /failed/ prefix', key)
        except Exception as e:
            logger.error('Error when moving %s to /failed/ prefix', key)
            logger.exception(e)
