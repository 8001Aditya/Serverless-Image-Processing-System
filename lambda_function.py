import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')
SOURCE_BUCKET = "my-image-processing-bucket"
PROCESSED_BUCKET = "my-image-processing-bucket-processed"

def lambda_handler(event, context):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {e}"
        }
