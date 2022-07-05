from xmlrpc.client import ResponseError
import requests
import json
import boto3
import os
from requests.auth import HTTPBasicAuth
from logger import Logger
from botocore.exceptions import ClientError

class WickrAPILibrary:
  _LOGGER = Logger(loglevel='info')
  _PARAM_SSM_PATH = '/AWIF/'
  _PARAM_WICKR_URL = 'ApiUrl'
  _PARAM_WICKR_API_KEY = 'ApiKey'
  _PARAM_WICKR_API_TOKEN = 'ApiToken'
  _PARAM_WICKR_VERIFY_CERT = 'VerifyCert'

  def __init__(self, url = '', api_key = '', token = '', verify_cert = True):
    if not url:
      self._LOGGER.info(f'No class params specified, checking environment variables and then SSM params...')
      self.url = self._get_default_param_value(self._PARAM_WICKR_URL).rstrip('/')
      self.api_key = self._get_default_param_value(self._PARAM_WICKR_API_KEY)
      self.token = self._get_default_param_value(self._PARAM_WICKR_API_TOKEN, True)
      self.verify_cert = self._str2bool(self._get_default_param_value(self._PARAM_WICKR_VERIFY_CERT))
    else:
      self.url = url.rstrip('/')
      self.api_key = api_key
      self.token = token
      self.verify_cert = verify_cert

    self.wickr_url = f'{self.url}/{self.api_key}'
    self.wickr_url_params = {'Accept': '*/*', 'Content-Type': 'application/json', 'Authorization': f'Basic {self.token}'}

  def _str2bool(self, value): 
      if not isinstance(value, bool):
          return value.lower() in ('yes', 'true')
      else:
          return value

  def _verify_token_params(self, token, token_path):
    if not token and not token_path:
      raise Exception("You must specify params 'token or 'token_path'")

  #  Use hierachy to find param values 1) environment varibles 2) lastly SSM parameter store
  def _get_default_param_value(self, param, decrypt = False):
    param_value = os.getenv(param, '')
    if (len(param_value) == 0):
      param_value = self.get_ssm_param(param, decrypt)
      if (len(param_value) > 0):
        self._LOGGER.info(f'{param} value found in SSM Parameter Store')
    else:
      self._LOGGER.info(f'{param} value found in environment varibles')

    return param_value

  def get_ssm_param(self, path_suffix, decrypt = False):
    """
    Returns a value from AWS SSM Parameter Store.

    Args:
        path_suffix (string): Do not enter the full SSM parameter path as this is based on a convention.  Enter the suffix.
        decrypt (bool, optional): True if SSM is of type SecureString. Defaults to False.

    Returns:
        string: Value from AWS SSM Parameter Store
    """    
    ssm_client=boto3.client('ssm')
    param_value = ''

    try:
        awif_path = f'{self._PARAM_SSM_PATH}{path_suffix}'
        awif_path = f'{self._PARAM_SSM_PATH}{path_suffix}'
        self._LOGGER.info(f'Looking for param: {awif_path} decrypt: {decrypt}')
        param=ssm_client.get_parameter(Name=awif_path, WithDecryption = decrypt)
        param_value = param['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        self._LOGGER.error(f'Param {awif_path} not found')
        raise
    except Exception as e:
        self._LOGGER.error(e)
        raise
    
    return param_value  

  def _call_wickr_api_post(self, url, data = {}):
      self._LOGGER.info(f'Call Wickr API: {url}') 
      response = requests.post(url,
                            headers=self.wickr_url_params,
                            verify=self.verify_cert,
                            data=json.dumps(data))
      
      self._LOGGER.info(f'Response code: {response.status_code}')
      if response.status_code in[400, 401, 404]:
        self._LOGGER.error(response.text)
        raise ValueError(response.text)

      return response

  def _call_wickr_api_get(self, url, data = {}):
      self._LOGGER.info(f'Call Wickr API: {url}') 
      response = requests.get(url,
                            headers=self.wickr_url_params,
                            verify=self.verify_cert,
                            data=json.dumps(data))
      
      self._LOGGER.info(f'Response code: {response.status_code}')      
      if response.status_code in[400, 401, 404]:
        self._LOGGER.error(response.text)
        raise ValueError(response.text)

      return response

  def add_room(self, title, description, message_expiry_in_millisecond, burn_on_read_seconds, users, moderators):
      data = {
          "room": {
              "title": title,
              "description": description,
              "ttl": message_expiry_in_millisecond,
              "bor": burn_on_read_seconds,
              "members": users,
              "masters": moderators
          }
      }
      room_id =''
      try:
        add_room = self._call_wickr_api_post(self.wickr_url + "/Rooms", data)
        json_data = json.loads(add_room.text)
        room_id = json_data['vgroupid']
        self._LOGGER.info(f'Created room with id: {room_id}')        
      except Exception as e:
        self._LOGGER.error(e)
        raise e
      return room_id

  def get_rooms(self):
      output = []
      try:
        rooms = self._call_wickr_api_get(self.wickr_url + "/Rooms")
        json_data = json.loads(rooms.text)

        for room in json_data['rooms']:
            self._LOGGER.info(room)
            output.append({'vgroupid':room['vgroupid'], 'title' : room['title']})
        
        self._LOGGER.info(f'Rooms: {output}')     
      except Exception as e:
        self._LOGGER.error(e)
        raise e

      return output

  def get_room_by_name(self, room_name):
      room_id = ''
      try:
        rooms = self._call_wickr_api_get(self.wickr_url + "/Rooms")
        self._LOGGER.info(f'get_rooom_by_name: {rooms.content}')
        json_data = json.loads(rooms.text)

        for room in json_data['rooms']:
            if (room['title'] == room_name):
              room_id = room['vgroupid']
      except Exception as e:
        self._LOGGER.error(e)

      if not room_id:
        self._LOGGER.error(f'Room {room_name} not found.')
      
      return room_id

  def room_blaster(self, message, burn_on_read_seconds=0,):
      rooms = self.get_rooms()
      for room in rooms:
          vgroupid = room['vgroupid']
          self.send_message_to_room(vgroupid, message, burn_on_read_seconds)
          self._LOGGER.info(f'Room blaster sent to room:{vgroupid}')

  def detect_pii(self, message, room_id):
      self._LOGGER.info('Start PII detection')
      client = boto3.client('comprehend') 
      response = client.detect_pii_entities(
            Text= message,
            LanguageCode='en')

      if len(response['Entities']) >0:
        self._LOGGER.info(f'Found PII...Reporting to room: ({room_id})')
        self.send_message_to_room(room_id, json.dumps(response))

      return response

  def send_message_to_room(self, room_id, message, burn_on_read_seconds = 0):
      data = {
          "message": message,
          "vgroupid": room_id,
          "bor": burn_on_read_seconds
      }

      self._LOGGER.info(f'Sending message to room: {room_id} bor: {burn_on_read_seconds}')
      send_message = self._call_wickr_api_post(self.wickr_url + "/Messages", data)
      self._LOGGER.info(f'Send Message Results: {send_message.content}')

      return send_message.content

  def set_callback_url(self, url):
    data = {
        "callbackurl": url,
    }

    try:
      response = self._call_wickr_api_post(self.wickr_url + "/MsgRecvCallback")
      self._LOGGER.info(f'Set callback URL:{response.content}')
    except Exception as e:
      self._LOGGER.error(e)

    return response.content
