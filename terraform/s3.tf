resource "aws_s3_bucket" "dvc_data_bucket" {
  bucket        = var.s3_bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "dvc_versioning" {
  bucket = aws_s3_bucket.dvc_data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "dvc_public_access" {
  bucket                  = aws_s3_bucket.dvc_data_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
