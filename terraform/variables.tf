variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "vm_name" {
  description = "Name of the GCE VM instance"
  type        = string
  default     = "infraguard-vm"
}

variable "app_name" {
  description = "Application name (used for naming resources)"
  type        = string
  default     = "infraguard-ai"
}
