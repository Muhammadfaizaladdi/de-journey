resource "google_storage_bucket" "raw" {
  name                        = "${local.prefix}dockerex_test"
  location                    = var.region
  uniform_bucket_level_access = true

  labels = merge(
    locals.commmon_labels,
    {
    bucket_type = "raw-data"
    }
  )
}

output "raw_bucket_name" {
  value = google_storage_bucket.raw.name
}

resource "google_storage_bucket" "processed" {
  name                        = "dockerex_processed"
  location                    = var.region
  uniform_bucket_level_access = true

  labels = {
    environment   = var.environment
    source_bucket = google_storage_bucket.raw.name
  }
}