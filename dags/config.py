import yaml
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yml")

with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

GCP_PROJECT = config["gcp"]["project_id"]
BUCKET_NAME = config["gcp"]["bucket_name"]
DATASET = config["gcp"]["dataset"]
CREDENTIALS = os.path.join(os.path.dirname(__file__), config["gcp"]["credentials_file"])

RAW_DATA_PATH = config["paths"]["raw_data"]
PROCESSED_DATA_PATH = config["paths"]["processed_data"]
