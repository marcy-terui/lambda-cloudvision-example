import sys
import urllib
import base64
import json
import requests
import pprint
import lamvery

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='


def lambda_handler(event, context):
    image_content = base64.b64encode(requests.get(event['url']).content)
    for res in cloudvision(image_content).get('responses'):
        for txt in res.get('textAnnotations'):
            print(txt['description'])


def cloudvision(image_content):
    api_url = GOOGLE_CLOUD_VISION_API_URL + lamvery.secret.get('GOOGLE_API_KEY')
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()
