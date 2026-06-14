import requests
import time

url = "http://a3fef5535b8f14a05a6aa3306ab88040-1540167051.us-east-2.elb.amazonaws.com/prediction_api"

payload = {
  "Gender": "Male",
  "Married": "Yes",
  "Dependents": "1",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 4583,
  "CoapplicantIncome": 1508.0,
  "LoanAmount": 128.0,
  "Loan_Amount_Term": 360.0,
  "Credit_History": 1.0,
  "Property_Area": "Rural"
}

print("Running first prediction (Model Execution)...")
start = time.time()
r1 = requests.post(url, json=payload)
end = time.time()
print(f"Result: {r1.json()}")
print(f"Time taken: {(end-start)*1000:.2f} ms")

print("\nRunning identical prediction (Redis Cache Execution)...")
start = time.time()
r2 = requests.post(url, json=payload)
end = time.time()
print(f"Result: {r2.json()}")
print(f"Time taken: {(end-start)*1000:.2f} ms")
