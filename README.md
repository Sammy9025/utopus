# Work done for UTOPUS INSIGHTS PVT. LTD. BANGALORE as SITE RELIABILITY ENGINEER.

# PROJECT-NAME: AWS IAM User Credential Expiry Notifier

Send password expiry notification and access key expiry notification on slack and email to the respective users and AWS admin. Reminding user to reset password every 90 days and rotate access key every 180 days.

# AWS Products Used:

AWS LAMBDA (Serverless computation service) –

Function to get credential report from IAM and calculate credential age to send slack notification & mail notification (User, Admin).

AWS IAM (Identity access & management service)–

Stores user credential report.

AWS EventBridge (Serverless event trigger service) –

Triggers lambda at specified time (rate).

AWS S3 (Storage service) –

Storage for slack id & mail id of users. (Excel file)

AWS SES (email sending service) –

Sends email notification to users.

# Applications Used:

Slack – Slack Bot integration to Send slack notification to user & admin.

# Language Used:

Python Version 3.9 – Lambda function scripting language.

# SETUP-STEPS:

AWS IAM:

Create role for lambda providing read access to AWS IAM report.

Go to IAM service in AWS console -> Create role -> select trusted entity (Trusted entity type = AWS Service, use case = lambda) -> Add permission (s3: read access, Iam: read access) -> name role 

AWS Lambda:

Create AWS lambda function.

Go to lambda service in AWS console -> Author from scratch -> Name your function) -> choose runtime as Python 3.9 -> use existing role

For installing pandas:

add layer to lambda function.

(Download pandas zip file for lambda and upload to layer)

Function name: NAME-OF-FUNCTION

Amazon SES:

Create Identity -> Register domain/email (sender & receiver)-> used in lambda fuction

AWS EventBridge:

Lambda function (Getiam) -> Function overview -> Add trigger -> EventBridge ((awakehour)schedule expression: rate(12hours))

AWS S3:

Go to S3 service in AWS console -> Create S3 bucket -> s3-slackuserfile -> Upload file (upload excel file with user AWS name, slackid & email ID)

Slack:

Create app at https://api.slack.com/apps (userapp) (permission scopes chat:write , Im:write) -> install app to Workspace -> Get slack app token (Starts from ''xoxb-')(used in lambda function)

![image](https://user-images.githubusercontent.com/68280687/233784488-7bf2b46a-7bfd-42a9-8fb1-8385b2edde4f.png)


