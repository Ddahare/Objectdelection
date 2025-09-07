import os
import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.getenv("S3_BUCKET", "your-detection-bucket")

def s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'ap-south-1')
    )

def upload_file(local_path: str, s3_key: str) -> bool:
    client = s3_client()
    try:
        client.upload_file(local_path, S3_BUCKET, s3_key)
        print(f"Uploaded {local_path} to s3://{S3_BUCKET}/{s3_key}")
        return True
    except ClientError as e:
        print("S3 Upload error:", e)
        return False

def download_file(s3_key: str, local_path: str) -> bool:
    client = s3_client()
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        client.download_file(S3_BUCKET, s3_key, local_path)
        print(f"Downloaded s3://{S3_BUCKET}/{s3_key} to {local_path}")
        return True
    except ClientError as e:
        print("S3 Download error:", e)
        return False
