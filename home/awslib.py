import boto3
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-east-1'
AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:337084155662:SystemSphere-Notifier'

# for retreiving secret for AWS Secretmanager
def get_secret(secret_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=AWS_REGION
    )

    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']
        secret_data = json.loads(secret_string)
        return secret_data

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"The secret with name '{secret_name}' was not found.")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print(f"Invalid request for the secret with name '{secret_name}'.")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print(f"Invalid parameter for the secret with name '{secret_name}'.")
        else:
            print(f"Error retrieving the secret with name '{secret_name}': {e}")


def subscribe_email_to_sns(email_address):
    sns_client = boto3.client('sns', region_name=AWS_REGION)
    response = sns_client.subscribe(
        TopicArn=AWS_SNS_TOPIC_ARN,
        Protocol='email',
        Endpoint=email_address,
    )
    return response
    
    

def send_email_sns(subject, message, email):
    sns_client = boto3.client('sns', region_name=AWS_REGION)

    response = sns_client.publish(
        TopicArn=AWS_SNS_TOPIC_ARN,
        Subject=subject,
        Message=message,
        MessageStructure='string',
    )

    return response
