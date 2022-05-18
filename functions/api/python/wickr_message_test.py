import json
from wickr_message import WickrMessage, WickrLocationMessage

#  Setup up mock data
with open('events/wickr_location_via_api_gateway.json') as finding_json:
    event = json.load(finding_json)


wickr_message = WickrLocationMessage(json.loads(event['body']))
print(wickr_message.message_type_id)
print(wickr_message.location_latitude)
print(wickr_message.location_longitude)

