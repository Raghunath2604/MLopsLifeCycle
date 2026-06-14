# Enterprise MLOps Architecture

[![CI/CD Pipeline](https://github.com/Raghunath2604/MLops-LifeCycle/actions/workflows/main.yml/badge.svg)](https://github.com/Raghunath2604/MLops-LifeCycle/actions/workflows/main.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-AWS%20EKS-326CE5)](https://kubernetes.io/)

A complete, self-healing, cloud-native ecosystem that covers the entire software lifecycle: Continuous Integration (CI), Continuous Deployment (CD), Continuous Testing (CT), and Continuous Monitoring (CM).

*"Building a model is data science. Engineering a reliable, observable infrastructure around that model is MLOps."*

## 🚀 The 6-Phase Architectural Roadmap

1. **Data & Model Lineage** ── Integrated **DVC** to version-track raw data and **MLflow** for model binaries, ensuring absolute experiment reproducibility on AWS S3.
2. **High-Performance Serving** ── Wrapped the XGBoost model logic inside an asynchronous **FastAPI** web service, optimized with a **Redis** caching layer for `<1ms` production inference.
3. **Automated CI/CD Workflows** ── Configured **GitHub Actions** pipelines to trigger automated unit testing via **Pytest**, build optimized Docker containers, and ship them to **Amazon ECR** on every code change.
4. **Cloud-Native Orchestration** ── Authored declarative Kubernetes manifests to deploy pods to an **Amazon EKS** cluster, managing horizontal auto-scaling, routing, and zero-downtime availability.
5. **The Observability Loop** ── Instrumented the application to expose telemetry metrics to **Prometheus**, visualizing live API request traffic and cluster health via custom **Grafana** dashboards.
6. **Proactive Drift Monitoring** ── Deployed a continuous evaluation dashboard via **Streamlit** using **Evidently AI** to automatically catch data drift and target drift before they impact production accuracy.

---

## 🗺️ System Architecture

```mermaid
graph TD
    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:white;
    classDef k8s fill:#326CE5,stroke:#fff,stroke-width:2px,color:white;
    classDef docker fill:#2496ED,stroke:#fff,stroke-width:2px,color:white;
    classDef python fill:#3776AB,stroke:#fff,stroke-width:2px,color:white;
    classDef db fill:#003B57,stroke:#fff,stroke-width:2px,color:white;

    %% Data & Training Layer
    subgraph "1. Machine Learning Pipeline"
        A[Raw CSV Data] --> B[Data Preprocessing]
        B --> C[XGBoost Model Training]
        C --> D[(MLflow Artifacts to S3)]
    end

    %% CI/CD & Containerization
    subgraph "2. Containerization (Docker)"
        D -- MLflow Model Registry --> E[FastAPI Application]
        E --> F[Docker Image Build]
        F -- push --> G[AWS Elastic Container Registry]
    end

    %% Deployment Layer
    subgraph "3. Production Environment (EKS)"
        G -- pull --> H(MLOps API Pods)
        
        subgraph "Ingress & Traffic Control"
            I[AWS Load Balancer] --> J[NGINX Ingress Controller]
            J -- 10 req/sec limit --> H
        end
        
        subgraph "Performance Layer"
            H -- "Cache Hit (<1ms)" --> K[(Redis Cache Cluster)]
            H -- "Cache Miss (~3s)" --> L[XGBoost Inference Engine]
        end
        
        subgraph "Monitoring & Observability"
            M[Prometheus] -.-> H
            M -.-> J
            N[Grafana Dashboards] --- M
        end
    end

    %% Connect the stages
    C -.->|Triggers| F

    %% Apply Classes
    class I aws;
    class H,J,M,N k8s;
    class F,G docker;
    class B,C,E,L python;
    class D,K db;
```

---

## 📊 Dashboard Showcases

### Data Drift & Quality Checks (Evidently AI)
![Data Drift](https://github.com/Chandru-21/MLOps_Project/assets/64595758/af0df23d-9980-4ee4-94c0-ddebdb923237)
![Data Quality](https://github.com/Chandru-21/MLOps_Project/assets/64595758/c1c62d64-9b69-4ca7-ba45-45ae226a7620)

### API Traffic & Cluster Health (Prometheus + Grafana)
![Grafana API Traffic](https://github.com/Chandru-21/MLOps_Project/assets/64595758/930f0a9a-352f-41f9-8106-9b6735af8ce4)
![Grafana Cluster Health](https://github.com/Chandru-21/MLOps_Project/assets/64595758/d046d9f9-1477-4975-9041-f4aa128bb0f3)

---

## 🛠️ Quick Start Guide

### Local Development
To run the model training pipeline locally:
```bash
pip install -r requirements.txt
dvc pull
python prediction_model/training_pipeline.py
```

To run the FastAPI server locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
```

### Production Deployment
The infrastructure is deployed automatically via GitHub Actions upon pushing to the `main` branch. To manually deploy or update the Kubernetes cluster:
```bash
aws eks update-kubeconfig --name mlops-v3
kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl apply -f service-monitor.yml
```
