terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# --- Static External IP ---

resource "google_compute_address" "infraguard_ip" {
  name   = "${var.app_name}-ip"
  region = var.region
}

# --- Firewall Rules ---

# No ingress rule is created by default. Operators must deliberately provide
# HTTPS source ranges after a TLS terminator/reverse proxy is configured.
resource "google_compute_firewall" "infraguard_https" {
  count = length(var.https_source_ranges) > 0 ? 1 : 0

  name        = "${var.app_name}-allow-https"
  description = "Allow HTTPS to InfraGuard from explicitly configured source ranges"
  network     = "default"
  direction   = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = var.https_source_ranges
  target_tags   = [var.app_name]
}

# HTTP is opt-in and intended only for a controlled redirect to HTTPS. The
# application itself remains bound to loopback by docker-compose.yml.
resource "google_compute_firewall" "infraguard_http_redirect" {
  count = var.enable_http_ingress ? 1 : 0

  name        = "${var.app_name}-allow-http-redirect"
  description = "Optional HTTP ingress for redirecting clients to HTTPS"
  network     = "default"
  direction   = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = var.http_source_ranges
  target_tags   = [var.app_name]

  lifecycle {
    precondition {
      condition     = length(var.http_source_ranges) > 0
      error_message = "http_source_ranges must contain at least one trusted CIDR when enable_http_ingress is true."
    }
  }
}

# Dashboard/API and observability ports are never opened globally. This rule is
# omitted unless trusted private, VPN, IAP, or tightly scoped operator CIDRs are
# supplied. Docker Compose additionally binds the API to host loopback.
resource "google_compute_firewall" "infraguard_management" {
  count = length(var.management_source_ranges) > 0 ? 1 : 0

  name        = "${var.app_name}-allow-management"
  description = "Allow dashboard and telemetry ports from trusted management networks only"
  network     = "default"
  direction   = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["8080", "3100", "9090"]
  }

  source_ranges = var.management_source_ranges
  target_tags   = [var.app_name]
}

# --- GCE VM ---

resource "google_compute_instance" "infraguard_vm" {
  name         = var.vm_name
  machine_type = "e2-medium"
  zone         = var.zone

  tags = [var.app_name]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
      type  = "pd-balanced"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.infraguard_ip.address
    }
  }

  metadata_startup_script = <<-SCRIPT
    #!/bin/bash
    set -e

    # Install Docker
    if ! command -v docker &> /dev/null; then
      apt-get update
      apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
      apt-get update
      apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
      usermod -aG docker ubuntu
      systemctl enable docker
      systemctl start docker
    fi

    echo "Docker setup complete"
  SCRIPT

  service_account {
    scopes = ["cloud-platform"]
  }
}

# --- Artifact Registry ---

resource "google_artifact_registry_repository" "infraguard_repo" {
  location      = var.region
  repository_id = var.app_name
  format        = "DOCKER"
  description   = "Docker images for InfraGuard AI"
}
