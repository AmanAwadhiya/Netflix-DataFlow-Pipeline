from pyspark.sql import SparkSession
import pandas as pd
import yaml
import gcsfs

# Load configuration
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

GCP_PROJECT = config["gcp"]["project_id"]
BUCKET_NAME = config["gcp"]["bucket_name"]
DATASET = config["gcp"]["dataset"]
CREDENTIALS = config["gcp"]["credentials_file"]
GCS_FILE_PATH = f"gs://{BUCKET_NAME}/raw/netflix_movies.csv"
BQ_TABLE = f"{GCP_PROJECT}.{DATASET}.netflix_movies"

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("NetflixDataProcessing") \
    .getOrCreate()

# ✅ Read CSV from GCS using gcsfs
fs = gcsfs.GCSFileSystem(token=CREDENTIALS)
with fs.open(GCS_FILE_PATH, 'rb') as f:
    pdf = pd.read_csv(f)  

# ✅ Convert Pandas DataFrame to Spark DataFrame
df = spark.createDataFrame(pdf)

# Show Data Preview
df.show(5)

# Write Data to BigQuery
df.write \
    .format("bigquery") \
    .option("table", BQ_TABLE) \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .mode("overwrite") \
    .save()

print("✅ Data successfully loaded into BigQuery!")

# Stop Spark session
spark.stop()
