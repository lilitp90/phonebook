import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError

from phonebook.settings import AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

REQUIRED_COLUMNS = ['Name', 'Phone Number', 'Email Address']


def validate_uploaded_file(file_path):
    """ Read the excel file and remove the rows where phone number is missing."""
    df = pd.read_excel(file_path)
    if df.columns.tolist() != REQUIRED_COLUMNS:
        return None
    return df[df['Phone Number'].notna()].fillna('')


def aws_upload(local_file, s3_file):
    """ Upload the file to s3 storage."""
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        s3.upload_file(local_file, AWS_STORAGE_BUCKET_NAME, s3_file)
        print("Successfully uploaded to s3 storage")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
