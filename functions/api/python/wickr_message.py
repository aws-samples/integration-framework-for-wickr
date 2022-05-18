from logger import Logger

class WickrMessage:
    MESSAGE_TYPE_LOCATION = 8000
    MESSAGE_TYPE_TEXT = 1000
    MESSAGE_TYPE_CREATE_ROOM = 4001
    _LOGGER = Logger(loglevel='info')

    message = {}
    message_type_id = ''

    def __init__(self, message):
        self.message = message
        self.message_type_id = self.message['msgtype']

    def _validate_message_type(self, required_message_type_id):
        is_valid = True
        if not (self.message_type_id == required_message_type_id):
            self._LOGGER.info(f'Ignoring message type: {self.message_type_id}')
            is_valid = False
            # raise Exception(f'Message type {self.message_type_id} is not yet supported')
        return is_valid

class WickrLocationMessage(WickrMessage):
    location_longitude = ''
    location_latitude = ''

    def __init__(self, message):
        super().__init__(message)

        if self._validate_message_type(self.MESSAGE_TYPE_LOCATION):
            self.location_longitude = self.message['location']['longitude']
            self.location_latitude = self.message['location']['latitude']