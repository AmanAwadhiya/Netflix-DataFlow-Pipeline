from prefect import flow, task
import pandas as pd
import yaml
from google.cloud import storage

# Load Config
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

GCP_PROJECT = config["gcp"]["project_id"]
BUCKET_NAME = config["gcp"]["bucket_name"]
DATASET = config["gcp"]["dataset"]
CREDENTIALS = config["gcp"]["credentials_file"]
RAW_DATA_PATH = config["paths"]["raw_data"]
PROCESSED_DATA_PATH = config["paths"]["processed_data"]

# Initialize GCS Client
client = storage.Client.from_service_account_json(CREDENTIALS)
bucket = client.bucket(BUCKET_NAME)

# Task 1: Extract Data from GCS
@task
def extract_data():
    """Downloads the raw Netflix dataset from GCS and loads it into a DataFrame."""
    local_file = "netflix_raw.csv"
    blob = bucket.blob("raw/netflix_movies.csv")
    blob.download_to_filename(local_file)

    df = pd.read_csv(local_file)
    return df

# Task 2: Transform Data
@task
def transform_data(df):
    """Cleans and processes the data."""
    df.dropna(subset=["title", "date_added"], inplace=True)  # Remove rows with missing values
    df["date_added"] = pd.to_datetime(df["date_added"])  # Convert to datetime
    return df

# Task 3: Load Data to GCS
@task
def load_to_gcs(df):
    """Uploads the cleaned dataset to the processed GCS path."""
    local_processed_file = "netflix_cleaned.csv"
    df.to_csv(local_processed_file, index=False)

    blob = bucket.blob("processed/netflix_cleaned.csv")
    blob.upload_from_filename(local_processed_file)

    print(f"Data uploaded to GCS: {PROCESSED_DATA_PATH}netflix_cleaned.csv")

# Prefect ETL Flow
@flow(name="Netflix_ETL")
def etl_pipeline():
    """Main ETL Flow: Extract, Transform, and Load."""
    df = extract_data()
    df_clean = transform_data(df)
    load_to_gcs(df_clean)

if __name__ == "__main__":
    etl_pipeline()