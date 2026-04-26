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

resource "google_compute_firewall" "infraguard_allow" {
  name    = "${var.app_name}-allow-ingress"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "3100", "9090", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
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
