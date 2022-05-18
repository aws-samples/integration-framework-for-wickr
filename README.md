# Integration Framework for Wickr

The integration Framework for Wickr allows developers to create event driven archtiectures representing serverless "bots" that can be used to construct Wickr integrations such as chat bots, workflows and any other process using many AWS services.

The reference architecture presented here is designed to give you a head start based on working use cases which can be extended for your companies requirements.

### What's it Written In?
The framwork is written using [AWS SAM](https://aws.amazon.com/serverless/sam/) allowing developers to use common IDEs and local debugging.



## Reference Architecture 

![image-20220224113510352](assets/reference-architecture.png)

[^NOTE]: In the above diagram we depict two Lambda functions, in reality a library will contain many other functions

## Use Cases and Integration Points

### AWS StepFunctions

In this use case a workflow could be created based on numerous decision points utilising customer data to drive the  process.

### AWS API Gateway

The Wickr API can be exposed to other platforms internally and externally using the API Gateway.  Other features include enhanced authorisation using Cognito.

### AWS Event Bridge

Using an event based architecture opens up endless possibilites for 

## Wickr API Library

The library is built using SAM allowing contributors to build and test locally.

- Python 3.9
- API Lambda Layer
- Lambda examples

#### API Interface Methods

[auto generate from code?]

# How to Setup the Framework for Bot Development

The AWS Wickr integration Framework (AWIF) has been written with developers in mind and it uses the AWS SAM which allows local development/debugging of Lambda functions which are used for bot development.

## Prerequisites

- Install the latest SAM framework (this repo was built with v1.43.0)
- Install the AWS CLI V2
- Configure the AWS CLI crendentials
- You have configured the Wickr Web Interface API bot and have a Wickr API key, token and URL [TODO:ADD HELPER URL HERE]

## Create AWIF Parameters

**Wickr API Token**

AWIF uses AWS Systems Manager Parameter Store  to store the Wickr bot access token which is used in the AWS Lambda Layer.

Given you are in a command line session with adequate AWS credentials run the following from the folder where you have downloaded this repo:

```bash
aws ssm put-parameter \
--name "/AWIF/ApiToken" \
--value <token> \
--type "SecureString" \
--overwrite
```

NOTE:  The default throughput is 40 transactions per second for SSM Parameters.  If you need to increase this limit you can folllow the steps here: https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-throughput.html#parameter-store-throughput-increasing-cli

**Incident Response  - Wickr Room Users**

In order to run the IR example you must set the following:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Wickr-Users" \
--value '[{"name": "user1@somewhere.co.uk"},{"name": "user2@somewhere.com"}]' \
--type "String" \
--overwrite
```

**Incident Response  - Wickr Room Moderators**

In order to run the IR example you must set the following Wickr room moderators:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Wickr-Moderators" \
--value '[{"name": "admin1@somewhere.co.uk"},{"name": "admin2@somewhere.com"}]' \
--type "String" \
--overwrite
```

**Incident Response  - Incident Manager Response Plan**

In order to run the IR example you must set the response plan arn:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Response-Plan_Arn" \
--value "arn:aws:ssm-incidents::123456789012:response-plan/High-Security-Incident" \
--type "String" \
--overwrite
```



## Deploy AWIF

## Setting Up Wickr API Call Backs

Locate the deployed API Gateway URL from the Cloudformation stack outputs value "AdapaterGatewayApi"


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.








