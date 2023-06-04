import json

def lambda_handler(event, context):

# get message from the first lambda function
    secondsFromMinutes = int(event['message']) * 60

# return a properly formatted JSON object
    return {
    'statusCode': 200,
    'body': json.dumps('Total seconds is: ' + str(secondsFromMinutes))
    }