import pathlib
import os


current_directory = os.path.dirname(os.path.realpath(__file__)) #current directory of the script

PACKAGE_ROOT = os.path.dirname(current_directory) #parent directory of current directory


# PACKAGE_ROOT = pathlib.Path(prediction_model.__file__).resolve().parent

DATAPATH = os.path.join(PACKAGE_ROOT,"datasets")

TRAIN_FILE = 'train.csv'
TEST_FILE = 'test.csv'

TARGET = 'Loan_Status'

#Final features used in the model
FEATURES = ['Gender', 'Married', 'Dependents', 'Education',
       'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area']

NUM_FEATURES = ['ApplicantIncome', 'LoanAmount', 'Loan_Amount_Term']

CAT_FEATURES = ['Gender',
 'Married',
 'Dependents',
 'Education',
 'Self_Employed',
 'Credit_History',
 'Property_Area']

# in our case it is same as Categorical features
FEATURES_TO_ENCODE = ['Gender',
 'Married',
 'Dependents',
 'Education',
 'Self_Employed',
 'Credit_History',
 'Property_Area']

FEATURE_TO_MODIFY = ['ApplicantIncome']
FEATURE_TO_ADD = 'CoapplicantIncome'

DROP_FEATURES = ['CoapplicantIncome']

LOG_FEATURES = ['ApplicantIncome', 'LoanAmount'] # taking log of numerical columns

S3_BUCKET = os.environ.get("S3_BUCKET", "YOUR_S3_BUCKET_NAME")

FOLDER="datadrift"

# Use local sqlite db or remote EC2 instance via environment variable
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")

EXPERIMENT_NAME="loan_prediction_model"

MODEL_NAME="/Loanprediction-model"

