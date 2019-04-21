import boto3
import json

credentials = {}
with open('secrets.json') as json_file:
    credentials = json.load(json_file)

#initialize comprehend module
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=credentials['aws_access_key_id'],
    aws_secret_access_key=credentials['aws_secret_access_key'],region_name=credentials['aws_region'])

sentimentData = comprehend.detect_sentiment(Text='teste', LanguageCode='pt')
print(sentimentData)
