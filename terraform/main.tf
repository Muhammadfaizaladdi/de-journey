resource "google_storage_bucket" "raw" {
  name                        = "${local.prefix}dockerex_test"
  location                    = var.region
  uniform_bucket_level_access = true

  labels = merge(
    local.common_labels,
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

resource "google_storage_bucket" "zone" {
    for_each = var.data_zone
    name = "${var.project_id}-${var.environment}-${each.key}"
    location = each.value.location
    uniform_bucket_level_access = true
    labels = merge(local.common_labels, { zone = each.key })
}