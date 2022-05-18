import json
import logging
from wickr_api import WickrAPILibrary
from incident_manager import IncidentManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Incoming event payload:")
    logger.info(event)

    wickr_api = WickrAPILibrary()
    users =  json.loads(wickr_api.get_ssm_param("IR-Wickr-Users"))
    moderators = json.loads(wickr_api.get_ssm_param("IR-Wickr-Moderators"))
    response_plan_arn = wickr_api.get_ssm_param("IR-Response-Plan_Arn")

    incident_manager = IncidentManager(event)
    logger.info(f"Finding description: {incident_manager.finding_description}")
    incident_arn = incident_manager.start_incident(response_plan_arn)

    thirty_days = 25536000
    burn_on_read_seconds = 0

    incident_manger_url = incident_manager.incident_manager_url
    logger.info(f"IM URL: {incident_manger_url}")
    
    room_id = wickr_api.add_room(incident_manager.finding_title, incident_manager.finding_description, thirty_days, burn_on_read_seconds, users, moderators)
    logger.info(f"New room ID: {room_id}")

    wickr_api.send_message_to_room(room_id, f"*A new incident has been initiated*\r\n\r\n{incident_manger_url}")
    wickr_api.send_message_to_room(room_id, f"*Incident:*\r\n\r\n*Description*: {incident_manager.finding_description}")

    # Add new room id to incident as metadata 
    #incident_manager.add_other_data(incident_arn,'vgroupid', room_id)

    return {
        "incident": json.dumps({
            "room_id": room_id,
            "incident_arn": incident_arn
        }),
    }
