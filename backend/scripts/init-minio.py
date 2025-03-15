from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../../frontend/.env")

def create_minio_client():
    return Minio(
        "localhost:9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

def init_minio():
    try:
        # Initialize the MinIO client
        client = create_minio_client()
        
        # Define buckets to create
        buckets = ["files", "processed", "markdown"]
        
        # Create each bucket if it doesn't exist
        for bucket in buckets:
            try:
                if not client.bucket_exists(bucket):
                    client.make_bucket(bucket)
                    print(f"Created bucket: {bucket}")
                    
                    # Set bucket policy to private
                    policy = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": ["*"]},
                                "Action": ["s3:GetBucketLocation"],
                                "Resource": [f"arn:aws:s3:::{bucket}"]
                            }
                        ]
                    }
                    client.set_bucket_policy(bucket, policy)
                else:
                    print(f"Bucket already exists: {bucket}")
                    
            except S3Error as err:
                print(f"Error creating bucket {bucket}: {err}")
                
        print("MinIO initialization completed successfully")
        
    except Exception as err:
        print(f"Error initializing MinIO: {err}")
        raise

if __name__ == "__main__":
    init_minio()
