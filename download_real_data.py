import urllib.request
import os

print("Downloading real Loan Prediction dataset...")
os.makedirs('prediction_model/datasets', exist_ok=True)

train_url = "https://raw.githubusercontent.com/shrikant-temburwar/Loan-Prediction-Dataset/master/train.csv"
test_url = "https://raw.githubusercontent.com/shrikant-temburwar/Loan-Prediction-Dataset/master/test.csv"

urllib.request.urlretrieve(train_url, "prediction_model/datasets/train.csv")
urllib.request.urlretrieve(test_url, "prediction_model/datasets/test.csv")

print("Real dataset downloaded successfully!")
