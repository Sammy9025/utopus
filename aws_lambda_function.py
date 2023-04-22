#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing required Packages
import json, boto3 #importing API
import pandas as pd #for data handling
import io #to read output
import requests #for slack app
from datetime import timedelta,datetime,timezone #to convert time to days

'''Lambda function to Get slack ID & Email (excel file with username,slcakID & email address) from AWS S3
   & Get user credential from AWS IAM to generate report to check user's password age (in Days)
   & Send User & Admin a slack message tagging the no. of daya passed since pasword change
   & Send user email with link for updating password if password age is more than 90 days'''


def lambda_handler(event, context):
#connection to AWS services

    s3=boto3.client('s3') #AWS for storage
    bucket='s3-bucketname'
    key='excel file name inside S3'
    s3response=s3.get_object(Bucket=bucket,Key=key)
    ses=boto3.client('ses',region_name="eu-west-1") #AWS for sending mail
    client = boto3.client('iam') #AWS to get user credentials
    w=client.generate_credential_report()
    response = client.get_credential_report()

#cleaning generated report & adding respective slack id and email id from S3

    df1 = pd.read_csv(io.BytesIO((response['Content'])))
    dfs = pd.read_excel(io.BytesIO((s3response['Body'].read())))
    date_now = datetime.now(tz=timezone.utc) + timedelta(days=90)
    x=pd.to_datetime(df1['password_last_changed'],errors='coerce')
    y=date_now-x
    s=y.astype('str')
    a1=pd.to_datetime(df1['access_key_1_last_rotated'], errors='coerce')
    a1d=date_now-a1
    a1s=a1d.astype('str',errors='ignore')
    for d in s:
        d=s.str.split(' ',1,expand=True)
    for a1dd in a1s:
        a1dd=a1s.str.split(' ',1,expand=True)
    df1['days']=d[0]
    df1['a1days']=a1dd[0]
    dfnew=pd.DataFrame({'name':dfs['slackname'],'pdays':df1['days'],'a1days':df1['a1days'],'slackID':dfs['slackID'],'emailID':dfs['emailID']})
    dfnew=dfnew.replace('NaT',0)
    dfnew=dfnew.dropna()
    dfnew[['pdays','a1days']]=dfnew[['pdays','a1days']].astype('int64')
    df=dfnew.loc[(dfnew['pdays'] >= 90),('name','pdays','slackID','emailID')]
    dfa1=dfnew.loc[(dfnew['a1days'] >= 180),('name','a1days','slackID','emailID')]
    #dfnewo1=dfnew[(dfnew['pdays']>= 90)|(dfnew['a1days']>=180)]

#Slack Notification(User):

    slack_token= 'xoxb-Bot-Token'
    for i in range(len(df)):
        df_p=df.iloc[i]
        first_name= df_p["name"].split(" ")[0:1]
        UID = df_p["slackID"]
        message = "Hi {},\n Your AWS IAM password age is {} days. \n To change credential please visit: \nLink-To-Update-Password".format(str(first_name)[1:-1],df_p['pdays'])
        data = {'token': slack_token, 'channel': UID, 'as_user': True, 'text': message}
        requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    for i in range(len(dfa1)):
        df_a=dfa1.iloc[i]
        first_name= df_a["name"].split(" ")[0:1]
        UID = df_a["slackID"]
        messagea = "Hi {},\n Your AWS IAM access key age is {} days. \n To change credential please visit: \nLink-To-Update-Password".format(str(first_name)[1:-1],df_a['a1days'])
        data = {'token': slack_token, 'channel': UID, 'as_user': True, 'text': messagea}
        requests.post(url='https://slack.com/api/chat.postMessage', data=data)

#Slack Notification(Admin):

    messageA = "Hi Admin,\n AWS credential age reminded to these user: \nUser reminded for password age : \n{}\nUser reminded for access key age : \n{}".format(df['name'].values,dfa1['name'].values)
    UIDA='Admin-User-Slack-ID'
    dataA = {'token': slack_token, 'channel': UIDA, 'as_user': True, 'text': messageA}
    requests.post(url='https://slack.com/api/chat.postMessage', data=dataA)
    #print (mailP['subject'])
    #print (mailA.head())
    
#Email Notification(User):

    for j in range(len(df)):
        df_ep=df.iloc[j]
        first_name= df_ep["name"].split(" ")[0:1]
        peID = df_ep["emailID"]
        body="Hello {},\n\nHope you are doing well!\n\nYou have not changed your password on AWS management console for more than 90 days.\n\nWe request you to login and reset the password -Link-To-Update-Password \n\nThank you!".format(str(first_name)[1:-1])
        ses.send_email(Source = 'Email-Usedin-SES',Destination = {'ToAddresses': ['Email-User-SES']},Message = {'Subject': {'Data': 'AWS IAM password reset','Charset': 'UTF-8'},'Body': {'Text':{'Data': body,'Charset': 'UTF-8'}}})
    for p in range(len(dfa1)):
        df_ep=dfa1.iloc[p]
        first_name= df_ep["name"].split(" ")[0:1]
        peID = df_ep["emailID"]
        body="Hello {},\n\nHope you are doing well!\n\nYou have not rotated your IAM user access key on AWS management console for more than 180 days. We request you to login and reset the password -Link-To-Update-Password \n\nThank you!".format(str(first_name)[1:-1])
        ses.send_email(Source = 'Email-Usedin-SES',Destination = {'ToAddresses': ['Email-Usedin-SES']},Message = {'Subject': {'Data': 'AWS IAM access key rotation','Charset': 'UTF-8'},'Body': {'Text':{'Data': body,'Charset': 'UTF-8'}}})
    print('Sent')

