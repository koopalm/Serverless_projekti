import boto3
from crudGet import lambda_handler as getdata
import os

def lambda_handler(event, context):

    htmldata = getdata(None, None)
    htmlbody = htmldata['body']
    snsarn = os.environ['snsarn']

    client = boto3.client('sns')
    response = client.publish(
        TargetArn=snsarn,
        Message=str(htmlbody),
        MessageStructure='text/html'
        )