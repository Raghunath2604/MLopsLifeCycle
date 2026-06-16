import pandas as pd
import numpy as np
from prediction_model.config import config  
import mlflow
import redis
import json
import hashlib
import os

# Initialize Redis connection
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-master")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
redis_client = None
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    redis_client.ping()
except Exception as e:
    redis_client = None
    print(f"Redis connection failed: {e}")


def generate_predictions(data_input):
    # 1. Try fetching from Redis Cache
    if redis_client:
        try:
            # Create a consistent hash of the input dictionary payload
            payload_str = json.dumps(data_input, sort_keys=True)
            cache_key = f"predict:{hashlib.md5(payload_str.encode()).hexdigest()}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                print("Cache hit! Returning prediction from Redis.")
                return {"prediction": json.loads(cached_result), "source": "redis_cache"}
        except Exception as e:
            print(f"Redis cache read error: {e}")

    # 2. Cache Miss: Run XGBoost model
    data = pd.DataFrame(data_input)
    experiment_name = config.EXPERIMENT_NAME
    experiment = mlflow.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id
    runs_df=mlflow.search_runs(experiment_ids=experiment_id, filter_string="status = 'FINISHED'", order_by=['metrics.f1_score DESC'])
    best_run=runs_df.iloc[0]
    best_run_id=best_run['run_id']
    best_model='runs:/' + best_run_id + config.MODEL_NAME
    loan_prediction_model=mlflow.sklearn.load_model(best_model)
    prediction=loan_prediction_model.predict(data)
    output = np.where(prediction==1,'Y','N')
    
    result_val = output.tolist() if isinstance(output, np.ndarray) else output
    
    # 3. Save result to Redis Cache for 1 hour (3600 seconds)
    if redis_client:
        try:
            redis_client.setex(cache_key, 3600, json.dumps(result_val))
        except Exception as e:
            print(f"Redis cache write error: {e}")

    result = {"prediction": result_val, "source": "xgboost_model"}
    return result


def generate_predictions_batch(data_input):
    # data = pd.DataFrame(data_input)
    experiment_name = config.EXPERIMENT_NAME
    experiment = mlflow.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id
    runs_df=mlflow.search_runs(experiment_ids=experiment_id, filter_string="status = 'FINISHED'", order_by=['metrics.f1_score DESC'])
    best_run=runs_df.iloc[0]
    best_run_id=best_run['run_id']
    best_model='runs:/' + best_run_id + config.MODEL_NAME
    loan_prediction_model=mlflow.sklearn.load_model(best_model)
    prediction=loan_prediction_model.predict(data_input)
    output = np.where(prediction==1,'Y','N')
    result = {"prediction":output}
    return result


    


if __name__=='__main__':
    generate_predictions()