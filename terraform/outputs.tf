output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.mlops_repo.repository_url
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "dvc_s3_bucket_name" {
  description = "Name of the S3 bucket for DVC"
  value       = aws_s3_bucket.dvc_data_bucket.bucket
}

output "instructions" {
  description = "Next steps for deployment"
  value       = <<EOF
1. Replace 'YOUR_S3_BUCKET_NAME' in .dvc/config with the 'dvc_s3_bucket_name' above.
2. Replace 'YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/mlops:latest' in deployment.yml with the 'ecr_repository_url' above.
3. Update GitHub Secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REPO_NAME) with your actual AWS keys and the ECR repo name.
4. Run 'aws eks update-kubeconfig --name mlops --region us-east-2' to connect kubectl.
EOF
}
