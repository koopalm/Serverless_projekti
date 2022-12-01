import boto3
import urllib3
import json
import uuid
import datetime
from datetime import datetime
import random

def get_inspirobot_url():
    http = urllib3.PoolManager()
    url = 'https://inspirobot.me/api?generate=true'
    resp = http.request('GET', url)
    return resp.data.decode('utf-8')
    
def get_daily_series():
    now = datetime.now()
    time = str(now.strftime("%Y-%m-%d"))
    
    try:
        http = urllib3.PoolManager()
        url = 'https://api.tvmaze.com/schedule/web?date=' + time + '&country=US'
        resp = http.request('GET', url)
        data = json.loads(resp.data.decode('utf-8'))
        end = len(data) - 1
        i = random.randint(0, end)
    
        result = {}
        result['series'] = data[i]['_embedded']['show']['name']
        result['episode'] = data[i]['name']
        result['episode_url'] = data[i]['url']
        return result
    except:
        print("Something went wrong")


def post_to_dynamodb(inspiration_image_url, daily_series):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Project3Group3Table')
    id = str(uuid.uuid4())
    now = datetime.now()
    x = str(now.strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
    daily_series_db = str(daily_series['series'] + ": " + daily_series['episode'])

    response = table.put_item(
       Item={
            'id': id,
            'request_date': x,
            'daily_series': daily_series_db,
            'inspirobot': inspiration_image_url
        }
    )
    return response


def lambda_handler(event, context):

    inspiration_image_url = get_inspirobot_url()
    daily_series = get_daily_series()
    post_to_dynamodb(inspiration_image_url, daily_series)

    htmlbody = ('''
    <h1 style="color: #5e9ca0;">Your daily motivational picture</h1>
    <br>
    <img src="%s" alt="Motivate!" />
    <br>
    <h2 style="color: #2e6c80;">Today is coming this episode:</h2>
    <p>Series: %s | Episode: %s | URL: %s</p>
    ''' % (inspiration_image_url, daily_series['series'], daily_series['episode'], daily_series['episode_url']))

    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": htmlbody
    }

