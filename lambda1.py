import json
import math

import boto3
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table(DB_NAME)
# store the current time in a human readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
# second lambda function
secondLambda = boto3.client('lambda')

region = REGION
ec2 = boto3.client('ec2',region_name=region)

def lambda_handler(event, context):


    if int(event['days']) > 20:
        instance = [INSTANCE_ID]
        
        ec2.stop_instances(InstanceIds=instance)
        
        return {
        'statusCode': 200,
        'body': json.dumps("Stopped ec2 instance" +str(instance))
        }
        
    # extract the two numbers from the Lambda service's event object
    minutesFromDays = int(event['days']) * 1440
    minutesFromHours = int(event['hours']) * 60
    totalMinutes = minutesFromDays + minutesFromHours
    
    # call second lambda function if operation type is seconds
    if event['operation'] == 'seconds':
        message = {"message": str(totalMinutes) }
        
        responseFromSecondLambda = secondLambda.invoke(
            FunctionName=ARN_OF_SECOND_LAMBDA,
            InvocationType='RequestResponse',
            Payload=json.dumps(message),
        )
            
        secondLambdaResponse = json.load(responseFromSecondLambda['Payload'])
        
        return secondLambdaResponse

    # write result and time to the DynamoDB table using the object we instantiated and save response in a variable
    response = table.put_item(
        Item={
            'ID': str(totalMinutes),
            'LatestGreetingTime':now
            })

    # return a properly formatted JSON object
    return {
    'statusCode': 200,
    'body': json.dumps('Total minutes is: ' + str(totalMinutes))
    }