import os
import io
import paramiko
from google.cloud import storage
import functions_framework

# ─────────────────────────────────────────────────────────────
# Configuration - Environment Variables (set via env_vars.json)
# ─────────────────────────────────────────────────────────────

SFTP_HOST = os.environ.get('SFTP_HOST')  # Your SFTP server hostname or IP (e.g., sftp.example.com)
SFTP_PORT = int(os.environ.get('SFTP_PORT', 22))  # Optional: custom port if not using default 22
SFTP_USERNAME = os.environ.get('SFTP_USERNAME')  # SFTP username
SFTP_PASSWORD = os.environ.get('SFTP_PASSWORD')  # Stored in Secret Manager, not in env_vars.json
SFTP_DIRECTORY = os.environ.get('ROOT_FOLDER')  # The remote directory to check for files (e.g., /data/files)
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')  # The target Google Cloud Storage bucket name
GCP_PROJECT_NAME = os.environ.get('GCP_PROJECT_NAME')  # Your GCP project ID

# ─────────────────────────────────────────────────────────────
# Cloud Function Entry Point
# ─────────────────────────────────────────────────────────────

@functions_framework.http
def sftp_to_gcs(request):
    """
    HTTP-triggered Cloud Function to transfer the latest file 
    from an SFTP directory to a Google Cloud Storage bucket.
    """
    try:
        # Establish SFTP connection
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get list of files in the specified directory
        print(f"Listing files in: {SFTP_DIRECTORY}")
        file_list = sftp.listdir_attr(SFTP_DIRECTORY)
        if not file_list:
            print("No files found in the SFTP directory.")
            return "No files found on SFTP.", 404

        # Identify the most recently modified file
        latest_file = max(file_list, key=lambda x: x.st_mtime)
        latest_file_path = f"{SFTP_DIRECTORY}/{latest_file.filename}"
        print(f"Latest file found: {latest_file.filename}")

        # Download file to memory
        with sftp.open(latest_file_path, mode='rb') as sftp_file:
            file_data = io.BytesIO(sftp_file.read())

        # Upload the file to the specified GCS bucket
        print(f"Uploading {latest_file.filename} to bucket {GCS_BUCKET_NAME}...")
        storage_client = storage.Client(project=GCP_PROJECT_NAME)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(latest_file.filename)
        blob.upload_from_file(file_data, rewind=True)

        print("Upload successful.")
        return f"File {latest_file.filename} transferred successfully!", 200

    except Exception as e:
        print(f"Error during SFTP to GCS transfer: {e}")
        return "An internal error occurred. Please check logs.", 500
