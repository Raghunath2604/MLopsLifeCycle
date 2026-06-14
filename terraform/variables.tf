variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "mlops"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "mlops"
}

variable "ecr_repo_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "mlops"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for DVC (MUST be globally unique)"
  type        = string
  default     = "raghunath2604-mlops-dvc-data"
}
