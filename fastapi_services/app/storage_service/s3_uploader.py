import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException


def upload_file_to_s3(file, bucket_name, object_name=None):
    """
    Uploads a file to AWS S3

    :param file: File to upload.
    :param bucket_name: Name of the bucket to upload to.
    :param object_name: S3 object name. If not specified, file.name is used.
    :return: True if file was uploaded, else False.
    """

    if object_name is None:
        object_name = file.filename

    # AWS SDK (boto3) find the credentials automatically in its default search paths
    s3_client = boto3.client('s3', region_name='us-east-1')
    

    try:
        s3_client.upload_fileobj(file.file, bucket_name, object_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found.")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"AWS S3 Client Error: {e}")

    return True

