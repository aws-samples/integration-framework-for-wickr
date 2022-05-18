import json
import logging
import requests
import os
from requests.auth import HTTPBasicAuth
from wickr_api import WickrAPILibrary

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Incoming event payload:")
    logger.info(event)

    wickr_api = WickrAPILibrary()
    room_name = os.getenv('RoomName', 'NOTSET')
    room_id = wickr_api.get_room_by_name(room_name)

    wickr_api.detect_pii('Here is my passport number: 533380006',room_id)

    return {
        "results": json.dumps({
            "room_id": room_id,
        }),
    }
