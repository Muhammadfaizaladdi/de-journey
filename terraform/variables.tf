variable "project_id" {
  type    = string
}

variable "region" {
  type    = string
}

variable "environment" {
  type    = string

}

variable "data_zone" {
    type = map(object({
        location = string
    }))
    description = "zona mapping"
}