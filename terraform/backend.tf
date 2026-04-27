terraform {
  backend "gcs" {
    bucket = "infraguard-terraform-state-project-4b1700d0-2b09-4852-8e3"
    prefix = "terraform/state"
  }
}
