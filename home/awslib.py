import boto3
from botocore.exceptions import ClientError
import json

def get_secret(secret_name):
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']
        # You can also access other fields such as 'SecretBinary' if needed

        # Modify this part based on the structure of your secret data
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



