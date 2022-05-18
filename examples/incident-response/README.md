
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

