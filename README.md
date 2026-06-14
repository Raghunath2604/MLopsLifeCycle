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

![System Architecture](architecture_diagram.png)

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
