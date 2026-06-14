FROM python:3.10-slim

RUN pip install --upgrade pip

WORKDIR /app

# Cache dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install dvc[s3]

COPY . /app 

#set permissions

RUN chmod +x /app/tests

RUN chmod +w /app/tests

RUN chmod +x /app/prediction_model

RUN chmod +w /app/prediction_model/trained_models

RUN chmod +w /app/prediction_model/datasets


ENV PYTHONPATH "${PYTHONPATH}:/app/prediction_model"

RUN pip install dvc[s3]

# AWS credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

# The model is trained and tested in the GitHub Actions pipeline prior to the Docker build.
# The FastAPI app will fetch the latest model from MLflow at runtime.

EXPOSE 8005

ENTRYPOINT ["python"]

CMD ["main.py"]


