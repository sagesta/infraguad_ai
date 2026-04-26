output "vm_external_ip" {
  description = "External IP address of the InfraGuard VM"
  value       = google_compute_address.infraguard_ip.address
}

output "artifact_registry_url" {
  description = "Docker image registry URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.infraguard_repo.repository_id}"
}
