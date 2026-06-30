# variables.tf — variables d'entrée du module
# ──────────────────────────────────────────────

variable "container_name" {
  description = "Nom du conteneur MinIO"
  type        = string
  default     = "anfa-minio-tf"
}

variable "minio_api_port" {
  description = "Port externe pour l'API MinIO (S3)"
  type        = number
  default     = 9010
}

variable "minio_console_port" {
  description = "Port externe pour la console web MinIO"
  type        = number
  default     = 9011
}

variable "minio_root_user" {
  description = "Nom d'utilisateur administrateur MinIO"
  type        = string
  default     = "anfa-admin"
}

variable "minio_root_password" {
  description = "Mot de passe administrateur MinIO (sensible)"
  type        = string
  sensitive   = true
}