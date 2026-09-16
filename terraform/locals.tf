locals {
    prefix = "de-${var.environment}"
    common_labels = {
        environment = var.environment
        managed_by = "terraform"
        team = "data"
    }
}