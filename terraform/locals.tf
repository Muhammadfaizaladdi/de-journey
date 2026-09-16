local {
    prefix = "de-${var.environment}"

    commmon_labels = {
        environment = var.environment
        managed_by = "terraform"
        team = "data"
    }
}