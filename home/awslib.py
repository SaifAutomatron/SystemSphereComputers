import logging
import os
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket="elasticbeanstalk-us-east-1-056934734804", object_key=None):
    """Upload a file to an S3 bucket
    :param object_key:
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param key: S3 object key. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 key was not specified, use file_name
    if object_key is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_key)
    except ClientError as e:
        logging.error(e)
        return False
    return True
