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

variable "https_source_ranges" {
  description = "CIDR ranges allowed to reach the HTTPS ingress on port 443. Empty by default so ingress is not exposed before TLS is configured."
  type        = list(string)
  default     = []

  validation {
    condition     = alltrue([for cidr in var.https_source_ranges : can(cidrnetmask(cidr))])
    error_message = "Every https_source_ranges value must be a valid IPv4 CIDR."
  }
}

variable "enable_http_ingress" {
  description = "Whether to allow port 80 for an HTTP-to-HTTPS redirect. Keep false unless a redirecting ingress is configured."
  type        = bool
  default     = false
}

variable "http_source_ranges" {
  description = "CIDR ranges allowed to reach optional HTTP redirect ingress on port 80."
  type        = list(string)
  default     = []

  validation {
    condition     = alltrue([for cidr in var.http_source_ranges : can(cidrnetmask(cidr))])
    error_message = "Every http_source_ranges value must be a valid IPv4 CIDR."
  }
}

variable "management_source_ranges" {
  description = "Trusted private, VPN, IAP, or tightly scoped operator CIDRs allowed to reach ports 8080, 3100, and 9090. World-open ranges are rejected."
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for cidr in var.management_source_ranges :
      can(cidrnetmask(cidr)) && !contains(["0.0.0.0/0", "::/0"], trimspace(cidr))
    ])
    error_message = "Management source ranges must be valid, trusted CIDRs; 0.0.0.0/0 and ::/0 are forbidden."
  }
}
