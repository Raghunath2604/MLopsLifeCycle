import pandas as pd
import numpy as np
import os

def generate_mock_data(n_samples=200):
    np.random.seed(42)
    data = {
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Married': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['0', '1', '2', '3+'], n_samples),
        'Education': np.random.choice(['Graduate', 'Not Graduate'], n_samples),
        'Self_Employed': np.random.choice(['Yes', 'No'], n_samples),
        'ApplicantIncome': np.random.uniform(1000, 20000, n_samples).round(2),
        'CoapplicantIncome': np.random.uniform(0, 10000, n_samples).round(2),
        'LoanAmount': np.random.uniform(50, 500, n_samples).round(2),
        'Loan_Amount_Term': np.random.choice([120, 180, 240, 360], n_samples),
        'Credit_History': np.random.choice([0.0, 1.0], n_samples),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples),
        'Loan_Status': np.random.choice(['Y', 'N'], n_samples)
    }
    return pd.DataFrame(data)

# Generate train and test datasets
train_df = generate_mock_data(500)
test_df = generate_mock_data(100)

# Ensure directories exist
os.makedirs('prediction_model/datasets', exist_ok=True)

# Save to CSV
train_df.to_csv('prediction_model/datasets/train.csv', index=False)
test_df.to_csv('prediction_model/datasets/test.csv', index=False)

print("Mock datasets created successfully!")
