import json
import boto3
import logging
import json
import uuid
from datetime import datetime
from logger import Logger

class IncidentManager:
    _LOGGER = Logger(loglevel='info')

    def __init__(self, finding):
        self.incident_arn = ''
        self.finding = finding
        self.region = ''
        self.account = ''
        self.incident_id = ''
        self.response_plan_arn = ''
        self.source = finding["source"]

        if self.source=="aws.guardduty":
            self.finding_description = finding["detail"]["description"]
            self.finding_title = finding["detail"]["title"]
            self.account = finding["account"]
            self.region = finding["region"]
        elif self.source=="aws.securityhub":
            self.finding_description = finding["detail"]["findings"][0]["Description"]
            self.finding_title = finding["detail"]["findings"][0]["Title"]            
            self.account = finding["account"]
            self.region = finding["region"]

    def parse_arn(self, arn):
        # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
        elements = arn.split(':', 5)
        result = {
            'arn': elements[0],
            'partition': elements[1],
            'service': elements[2],
            'region': elements[3],
            'account': elements[4],
            'resource': elements[5],
            'resource_type': None
        }
        if '/' in result['resource']:
            result['resource_type'], result['resource'] = result['resource'].split('/',1)
        elif ':' in result['resource']:
            result['resource_type'], result['resource'] = result['resource'].split(':',1)
        return result

    def build_arn_for_instance(self, partition, region, account, instance_id):
        return f"arn:{partition}:ec2:{region}:{account}:instance/{instance_id}"

    @property
    def incident_manager_url(self):
        return f"https://{self.region}.console.aws.amazon.com/systems-manager/incidents/home?region={self.region}#/{self.account}/{self.incident_id}"

    def start__incident_from_guard_duty_finding(self):
        event = self.finding
        resource_arn = self.build_arn_for_instance( 
            event["detail"]["partition"],
            event["detail"]["region"],
            event["detail"]["accountId"],
            event["detail"]["resource"]["instanceDetails"]["instanceId"])

        trigger_arn = event["detail"]["arn"]
        title = event["detail"]["title"]
        description = event["detail"]["description"]


        client = boto3.client('ssm-incidents')
        response = client.start_incident(
            clientToken=str(uuid.uuid4()),
            impact=1,
            relatedItems=[
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'url': "http://www.google.com"
                        }
                    },
                    'title': 'Remediation guide for this incident'
                },
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'arn': resource_arn,
                        }
                    },
                    'title': 'EC2 Instance With Detected Activity'
                },
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'arn': trigger_arn,
                        }
                    },
                    'title': 'Product'
                },
            ],
            responsePlanArn=self.response_plan_arn,
            title=title,
            triggerDetails={
                'rawData': '',
                'source': f'custom.{event["source"]}',
                'timestamp': datetime.today().strftime('%Y-%m-%d'),
                'triggerArn': trigger_arn
            }
        )

        self._LOGGER.info(f"Incident response: {response}")

        incident_arn = response["incidentRecordArn"]
        related_items = client.list_related_items(
            incidentRecordArn=incident_arn,
            maxResults=10,
        )

        ops_item_arn = list(filter(lambda x:x["identifier"]["type"]=="PARENT",related_items["relatedItems"]))[0]["identifier"]["value"]["arn"]

        # Enrich parent ops item with related resource
        opsitem = boto3.client('ssm',region_name='eu-west-1')
        opsitem_id = self.parse_arn(ops_item_arn)['resource']
        response = opsitem.update_ops_item(
            OperationalData={
                '/aws/resources': {
                    'Value': "[{\"arn\":\"" + resource_arn + "\"}]",
                    'Type': 'SearchableString'
                }
            },
        OpsItemId=opsitem_id,
        )
        
        self.incident_arn = incident_arn
        return incident_arn

    def add_other_data(self, incident_arn, title, data):
        client = boto3.client('ssm-incidents')
        response = client.update_related_items(
        clientToken='',
        incidentRecordArn=incident_arn,
        relatedItemsUpdate={
            'itemToAdd': {
                'identifier': {
                    'type': 'OTHER',
                    'value': {
                        'url': data
                    }
                },
                'title': title
            }}   
            )

    def start__incident_from_security_hub_finding(self):
        event = self.finding
        resource_arn = event["detail"]["findings"][0]["Resources"][0]["Id"]

        trigger_arn = event["detail"]["findings"][0]["Id"]
        title = event["detail"]["findings"][0]["Title"]
        description = event["detail"]["findings"][0]["Description"]
        remediation_guide = event["detail"]["findings"][0]["Remediation"]["Recommendation"]["Url"]

        client = boto3.client('ssm-incidents')
        response = client.start_incident(
            clientToken=str(uuid.uuid4()),
            impact=1,
            relatedItems=[
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'url': remediation_guide
                        }
                    },
                    'title': 'Remediation guide for this incident'
                },
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'arn': resource_arn,
                        }
                    },
                    'title': 'EC2 Instance With Detected Activity'
                },
                {
                    'identifier': {
                        'type': 'OTHER',
                        'value': {
                            'arn': trigger_arn,
                        }
                    },
                    'title': 'Product'
                },
            ],
            responsePlanArn=self.response_plan_arn,
            title=title,
            triggerDetails={
                'rawData': '',
                'source': f'custom.{event["source"]}',
                'timestamp': datetime.today().strftime('%Y-%m-%d'),
                'triggerArn': trigger_arn
            }
        )

        incident_arn = response["incidentRecordArn"]
        related_items = client.list_related_items(
            incidentRecordArn=incident_arn,
            maxResults=10,
        )

        ops_item_arn = list(filter(lambda x:x["identifier"]["type"]=="PARENT",related_items["relatedItems"]))[0]["identifier"]["value"]["arn"]

        # Enrich parent ops item with related resource
        opsitem = boto3.client('ssm',region_name='eu-west-1')
        opsitem_id = self.parse_arn(ops_item_arn)['resource']
        response = opsitem.update_ops_item(
            OperationalData={
                '/aws/resources': {
                    'Value': "[{\"arn\":\"" + resource_arn + "\"}]",
                    'Type': 'SearchableString'
                }
            },
        OpsItemId=opsitem_id,
        )

        return ''

    def start_incident(self, response_plan_arn):
        
        self.response_plan_arn = response_plan_arn

        if self.source=="aws.guardduty":
            self.start__incident_from_guard_duty_finding()
        elif self.source=="aws.securityhub":
            self.start__incident_from_security_hub_finding()
        else:
            self._LOGGER.error(f"Events from source {self.source} are not supported.")

        return ''