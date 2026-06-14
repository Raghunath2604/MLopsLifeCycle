import pandas as pd
import numpy as np
import os
import boto3
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "raghunath2604-mlops-dvc-data")

print(f"Uploading drift data to S3 Bucket: {BUCKET_NAME}")

def generate_mock_data(n_samples=200, drift=False):
    data = {
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Married': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['0', '1', '2', '3+'], n_samples),
        'Education': np.random.choice(['Graduate', 'Not Graduate'], n_samples),
        'Self_Employed': np.random.choice(['Yes', 'No'], n_samples),
        # Introduce drift in income if requested
        'ApplicantIncome': np.random.uniform(5000 if drift else 1000, 30000 if drift else 20000, n_samples).round(2),
        'CoapplicantIncome': np.random.uniform(0, 10000, n_samples).round(2),
        'LoanAmount': np.random.uniform(200 if drift else 50, 700 if drift else 500, n_samples).round(2),
        'Loan_Amount_Term': np.random.choice([120, 180, 240, 360], n_samples),
        'Credit_History': np.random.choice([0.0, 1.0], n_samples),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples),
        'Loan_Status': np.random.choice(['Y', 'N'], n_samples)
    }
    return pd.DataFrame(data)

def upload_to_s3(df, key):
    csv_buffer = df.to_csv(index=False)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=csv_buffer)
    print(f"Uploaded: s3://{BUCKET_NAME}/{key}")

if __name__ == "__main__":
    np.random.seed(42)
    
    # Generate Baseline Data
    baseline_df = generate_mock_data(500, drift=False)
    upload_to_s3(baseline_df, "datadrift/baseline.csv")

    # Generate Drifted Data for the past 3 days
    for i in range(3):
        # Day 0 is today, Day 1 is yesterday, etc.
        target_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        # We increase drift probability slightly each day
        is_drifted = i < 2 # Recent days have drift
        daily_df = generate_mock_data(100, drift=is_drifted)
        upload_to_s3(daily_df, f"datadrift/{target_date}/data.csv")

    print("[SUCCESS] Mock Drift Data successfully populated in S3!")
