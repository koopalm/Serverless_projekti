# Motivational picture and daily series with API Gateway and SES (AWS SAM) 

![Architecture](https://i.imgur.com/C3M4ECf.png)

## Prerequisites
* AWS CLI
* AWS SAM CLI
* Git

## Installation
Git clone this repository:
```bash
git clone https://github.com/koopalm/Serverless_projekti.git
```

Go to root of Serverless_projekti and build and deploy with AWS SAM CLI. Give stack name, preferred region and email address where you want daily motivation email:
```bash
sam build
sam deploy --guided
```

After deploy is complete you should see API Gateway url to test if it works. Also all your GET calls will be recorded to DynamoDB table.

You will get ugly (not-html) motivational email daily at 06:00:00 UTC.