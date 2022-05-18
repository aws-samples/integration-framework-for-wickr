import json
import logging
import os
from wickr_api import WickrAPILibrary

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Incoming event payload:")
    logger.info(event)
    room_id = ''

    wickr_api = WickrAPILibrary()
    burn_on_read_seconds = 0
    room_name = os.getenv('ChatBotRoomName', 'NOTSET')
    room_id = wickr_api.get_room_by_name(room_name)

    wickr_api.send_message_to_room(room_id,json.dumps(event))

    return {
        "results": json.dumps({
            "room_id": room_id,
        }),
    }
