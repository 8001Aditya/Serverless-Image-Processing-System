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

        response = s3.get_object(Bucket=bucket_name, key=object_key)
        image_data = response['Body'].read()

        image = Image.open(io.BytesIO(image_data))

        resized_image = image.resize((300,300))

        buffer =  io.BytesIO()
        resized_image.save(buffer, format=image.format)
        buffer.seek(0)

        processed_key = f"processed/{object_key}"
        s3.put_object(Bucket=PROCESSED_BUCKET, key=processed_key, Body=buffer)

        print(f"Processed image saved to: {PROCESSED_BUCKET}/{processed_key}")

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ImageMetadata')
        table.put_item(item={
            'ImageID' : object_key,
            'ProcessedURL' : f"s3://{PROCESSED_BUCKET}/{processed_key}",
            'Size': f"{resized_image.size[0]}x{resized_image.size[1]}",
            'Timestamp': response['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {e}"
        }