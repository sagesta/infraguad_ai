terraform {
  backend "gcs" {
    bucket = "infraguard-ai-tfstate"
    prefix = "terraform/state"
  }
}
