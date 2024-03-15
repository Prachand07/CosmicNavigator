import json
import boto3
import io
import csv 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Testingbytrigger')

s3Client = boto3.client('s3')
def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"Processing file: {key}")

    response = s3Client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    reader = csv.reader(io.StringIO(data))
    next(reader) 

    for row in reader:
         item = {
                    'Name': row[0],
                    'Description':(row[1]),
                    'Major Stars': (row[2]),
                    'Asterisms':(row[3]),
                    'Season of Visibility':(row[4]),
                    'Interesting Facts':(row[5]),
                    'S3Key':(row[6]),
                    'ImageURL':(row[7]),
                    'Also Known as':(row[8])
                    
                }              
         table.put_item(Item=item)

    print("Data stored in DynamoDB.")

    return {
        'statusCode': 200,
        'body': 'Data processed and stored in DynamoDB.'
    }
