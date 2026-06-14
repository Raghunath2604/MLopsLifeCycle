import streamlit as st
import boto3
import pandas as pd
import os
import io
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="Enterprise Drift Monitor", page_icon="📈", layout="wide")

# Load environment variables
load_dotenv()
BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "raghunath2604-mlops-dvc-data")

@st.cache_resource
def get_s3_client():
    return boto3.client('s3')

@st.cache_data(ttl=3600)
def list_folders(bucket_name, prefix):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    return [content.get('Prefix') for content in response.get('CommonPrefixes', [])]

@st.cache_data(ttl=3600)
def list_csv_files(bucket_name, folder):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder)
    return [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.csv')]

@st.cache_data
def load_csv_from_s3(bucket_name, key):
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(io.BytesIO(response['Body'].read()))

@st.cache_data
def generate_evidently_report(baseline_df, latest_df, preset_type):
    if preset_type == "Data Drift":
        preset = DataDriftPreset()
    elif preset_type == "Data Quality":
        preset = DataSummaryPreset()
    elif preset_type == "Target Drift":
        preset = DataDriftPreset()
    else:
        preset = DataDriftPreset()
        
    report = Report(metrics=[preset])
    snapshot = report.run(reference_data=baseline_df, current_data=latest_df)
    
    # Save to string instead of disk to prevent I/O bottlenecks
    html_content = snapshot.get_html_str(as_iframe=False)
    return html_content

def find_most_recent_folder(bucket_name, prefix, max_days=7):
    folders = list_folders(bucket_name, prefix)
    for i in range(max_days):
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        check_date_folder = f'{prefix}{check_date}/'
        if check_date_folder in folders:
            return check_date_folder
    return None

def main():
    st.sidebar.title("📈 MLOps Drift Monitor V2")
    st.sidebar.markdown(f"**Connected Bucket:** `{BUCKET_NAME}`")
    
    page = st.sidebar.radio("Select Analysis Type:", ["Data Drift", "Data Quality", "Target Drift"])

    st.title(f"{page} Analysis")
    prefix = 'datadrift/'

    most_recent_folder = find_most_recent_folder(BUCKET_NAME, prefix)

    if most_recent_folder:
        try:
            baseline_csv_key = 'datadrift/baseline.csv'
            baseline_df = load_csv_from_s3(BUCKET_NAME, baseline_csv_key)

            # Target Drift requires the target column, Data Drift doesn't.
            if page in ["Data Drift", "Data Quality"]:
                baseline_df = baseline_df.drop(columns=['Loan_ID', 'Loan_Status'], errors='ignore')
            elif page == "Target Drift":
                baseline_df = baseline_df.drop(columns=['Loan_ID'], errors='ignore')

            latest_csv_files = list_csv_files(BUCKET_NAME, most_recent_folder)
            
            if not latest_csv_files:
                st.warning(f"No CSV files found in {most_recent_folder}")
                return

            st.markdown(f"### Monitoring Date: `{most_recent_folder.split('/')[1]}`")
            selected_file = st.selectbox('Select the target dataset stream', latest_csv_files)

            if selected_file:
                with st.spinner("Crunching Evidenty ML metrics..."):
                    latest_df = load_csv_from_s3(BUCKET_NAME, selected_file)
                    
                    if page in ["Data Drift", "Data Quality"]:
                        latest_df = latest_df.drop(columns=['Prediction', 'Loan_Status', 'Loan_ID'], errors='ignore')
                    elif page == "Target Drift":
                        latest_df = latest_df.drop(columns=['Prediction', 'Loan_ID'], errors='ignore')

                    html_report = generate_evidently_report(baseline_df, latest_df, page)
                    
                    # Display the cached HTML report
                    st.components.v1.html(html_report, height=1200, scrolling=True)

        except Exception as e:
            st.error(f"Error loading data from S3: {e}")
    else:
        st.warning('No recent data drift folders found in the last 7 days.')

if __name__ == "__main__":
    main()
