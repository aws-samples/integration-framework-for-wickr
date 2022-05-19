import json
import logging
import os
import requests
import boto3
from datetime import datetime
from requests.auth import HTTPBasicAuth
from wickr_api import WickrAPILibrary
from wickr_message import WickrMessage, WickrLocationMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

wickr_location_room_name = os.getenv('wickr_location_room_name', 'NOTSET')
wickr_pii_room_name = os.getenv('wickr_pii_room_name', 'NOTSET')

def lambda_handler(event, context):
    MESSAGE_TYPE_LOCATION = 8000
    MESSAGE_TYPE_TEXT = 1000
    MESSAGE_TYPE_CREATE_ROOM = 4001
    MESSAGE_TYPE_FILE_TRANSFER = 6000

    logger.info('Incoming event payload:')
    logger.info(json.dumps(event))

    # Determine if event came from an API Gateway or Lambda Function URL- it will have a body element if so
    incoming_event = event
    if "body" in event:
        logger.info('Using API Gateway Or Lambda Function URL payload')
        incoming_event = json.loads(event['body'])

    if "msgtype" in incoming_event:
        message_type_id = incoming_event['msgtype']
        if message_type_id == MESSAGE_TYPE_LOCATION:
            wickr_api = WickrAPILibrary()
            wickr_message = WickrLocationMessage(incoming_event)
            logger.info(wickr_message.message_type_id)
            logger.info(wickr_message.location_latitude)
            logger.info(wickr_message.location_longitude)
    
            location_room_id = wickr_api.get_room_by_name(wickr_location_room_name)
            wickr_api.send_message_to_room(location_room_id, json.dumps(incoming_event))
        elif message_type_id == MESSAGE_TYPE_TEXT:
            #wickr_api = WickrAPILibrary()
            logger.info('Room Message received...')
            #message_text = incoming_event['message']
            #pii_room_id = wickr_api.get_room_by_name(wickr_pii_room_name)
            #wickr_api.detect_pii(message_text,pii_room_id)
        elif message_type_id == MESSAGE_TYPE_FILE_TRANSFER:
            logger.info('File sent detected')
            logger.info(json.dumps(incoming_event))
    else:
        logger.info('Unknown payload.')

    return {}
