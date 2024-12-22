import os 
import subprocess 
import boto3 
from datetime import datetime
from botocore.exceptions import NoCredentialsError

# Configuration
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
BACKUP_DIR = "/tmp/"
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_REGION = os.environ.get('AWS_REGION')

def create_backup():
    try:
        # Generate a timestamp for the backup file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}{DATABASE_NAME}_backup_{timestamp}.sql"

        # Construct the mysqldump command
        dump_command = f"mysqldump -h {os.environ.get('DB_HOST')} -u {DATABASE_USER} -p{DATABASE_PASSWORD} {DATABASE_NAME} > {backup_file}"

        # Execute the mysqldump command
        subprocess.run(dump_command, shell=True, check=True)

        print(f"Backup created at {backup_file}")
        return backup_file

    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def upload_to_s3(file_path):
    try:
        # Create an S3 client
        s3_client = boto3.client('s3', region_name=AWS_REGION)

        # Get the filename from the file path
        file_name = os.path.basename(file_path)

         # Upload the file to S3
        s3_client.upload(file_path, AWS_BUCKET_NAME, file_name)
        print(f"Backup uploaded to S3: {file_name}")

    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"Error uploading to S3: {e}")



def main():
    # Create the backup
    backup_file = create_backup()

    # If backup was created successfully, upload it to S3, and remove the local backup file after successful upload
    if backup_file:
        upload_to_s3(backup_file)
        os.remove(backup_file)

if __name__ == "__main__":
    main()