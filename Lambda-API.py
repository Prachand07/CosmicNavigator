import boto3

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Testingbytrigger' 
    table = dynamodb.Table('Testingbytrigger')

    try:
        name = event['name']
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': 'Missing required parameter: name'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': 'Error parsing request body: {}'.format(str(e))
        }

    try:
        # Query DynamoDB table
        response = table.query(
            KeyConditionExpression='#name = :name',
            ExpressionAttributeNames={'#name': 'Name'},
            ExpressionAttributeValues={':name': name}
        )

        items = response.get('Items', [])
        
        if items:
            # Convert Decimal objects to suitable types
            result = {}
            for item in items:
                result['Name'] = item['Name']
                result['Description'] = item['Description']
                result['Major Stars'] = item['Major Stars']
                result['Asterisms'] = item['Asterisms']
                result['Season of Visibility'] = item['Season of Visibility']
                result['Interesting Facts'] = item['Interesting Facts']
                result['ImageURL'] = item.get('ImageURL')  
                result['Also Known as'] = item['Also Known as']
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': result
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': {'Error!': 'No details found for the provided name.'}
            }
            

    except Exception as e:
        print('Error:', str(e))
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': 'Internal Server Error'
        }
