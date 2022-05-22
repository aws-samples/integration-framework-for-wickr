# **Incident Response (IR)  - Wickr War Room**

This example uses AWS Systems Manager Incident Manager to form part of an incident response workflow where the goal is to create a "war room" for secure out of band collaboration.

The sample is designed to provide a basic workflow which can be extended for your organisations requirements.

### Wickr War Room Incident Resonders

The workflow will create a new Wickr war room designed for the incident responders, configure the users by running the following:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Wickr-Users" \
--value '[{"name": "nikki.wolf@example.com"},{"name": "john.doe@example.com"}]' \
--type "String" \
--overwrite
```

### Wickr Room Moderators

In order to run the IR example you must set the following Wickr room moderators:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Wickr-Moderators" \
--value '[{"name": "admin1@example.com"},{"name": "admin2@example.com"}]' \
--type "String" \
--overwrite
```

### AWS Incident Manager Response Plan

A prerequisite for using AWS Incident Manager is creating a resonse plan that can include escalation processes:

```bash
aws ssm put-parameter \
--name "/AWIF/IR-Response-Plan_Arn" \
--value "arn:aws:ssm-incidents::123456789012:response-plan/High-Security-Incident" \
--type "String" \
--overwrite
```

