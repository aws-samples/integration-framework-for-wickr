import json
import logging
from wickr_api import WickrAPILibrary

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Incoming event payload:")
    logger.info(event)

    wickr_api = WickrAPILibrary()
    thirty_days = 25536000
    burn_on_read_seconds = 0

    wickr_api.room_blaster('*CRITICAL FIELD MESSAGE:*\r\nCode red\r\n\r\n Return to base.', burn_on_read_seconds)

    return {
        "results": json.dumps({
        }),
    }
