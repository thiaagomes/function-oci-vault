import io
import json
import logging
import random
import string
import boto3
from fdk import response


access_key = '3932056f4f8a85b736dc5deedfce2cf6529f87d1'
secret_key = 'EH9rJi7kLfSsg7Lqp7NxrNpZCc9zlh5pC4/9jnPJEaQ='


bucket_name = 'bucket-demo'


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def handler(ctx, data: io.BytesIO = None):
    try:
        random_password = generate_random_password()

        
        client = boto3.client('s3',
                              region_name='sa-saopaulo-1',
                              endpoint_url='https://idi1o0a010nx.compat.objectstorage.sa-saopaulo-1.oraclecloud.com',
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key)

        
        object_name = 'random_password.txt'
        client.put_object(Bucket=bucket_name, Key=object_name, Body=random_password)

        return response.Response(
            ctx,
            response_data=json.dumps(
                {"message": "Random password generated and stored in Object Storage."},
            ),
            headers={"Content-Type": "application/json"}
        )

    except Exception as ex:
        logging.getLogger().info('Error: ' + str(ex))
        return response.Response(
            ctx,
            response_data=json.dumps(
                {"error": "Failed to generate and store the random password."},
            ),
            headers={"Content-Type": "application/json"},
            status_code=500
        )