terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

locals {
  token     = "y0_AgAAAAAiCiftAATuwQAAAAD_Hb01AADMnnggvYpBd6Lziky78Hl5BitVMQ"
  cloud_id  = "b1grm0vij3q8r6gl05ms"
  folder_id = "b1gr4ni8543ilvnsjf7i"
}
 
provider "yandex" {
  token     = local.token
  cloud_id  = local.cloud_id
  folder_id = local.folder_id
  zone      = "ru-central1-d"
}

resource "yandex_iam_service_account" "sa" {
  name        = "uralintern"
  description = "Admin's service account"
}

resource "yandex_resourcemanager_folder_iam_member" "admin-account-iam" {
  folder_id = local.folder_id
  role      = "admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = "${yandex_iam_service_account.sa.id}"
  description        = "static access key for object storage"
}

resource "yandex_storage_bucket" "frontend" {
  access_key = ${yandex_iam_service_account_static_access_key.sa-static-key.access_key}"
  secret_key = ${yandex_iam_service_account_static_access_key.sa-static-key.secret_key}"
  bucket = "lk-crm"
}

resource "yandex_vpc_network" "default" {
  name = "uralintern-network"
  description = "Network for uralintern project"
}

resource "yandex_vpc_subnet" "default-central1-a" {
  v4_cidr_blocks = ["172.16.6.0/28"]
  zone           = "ru-central1-a"
  network_id     = "${yandex_vpc_network.default.id}"
}

resource "yandex_vpc_subnet" "default-central1-b" {
  v4_cidr_blocks = ["192.168.0.0/16"]
  zone           = "ru-central1-b"
  network_id     = "${yandex_vpc_network.default.id}"
}

resource "yandex_vpc_subnet" "default-central1-d" {
  v4_cidr_blocks = ["10.10.0.0/28"]
  zone           = "ru-central1-d"
  network_id     = "${yandex_vpc_network.default.id}"
}

resource "yandex_vpc_security_group" "group1" {
  name        = "uralintern-sec-group"
  description = "Security group for uralintern project"
  network_id  = "${yandex_vpc_network.default.id}"

  ingress {
    protocol       = "ANY"
    description    = "Allow all ports"
    from_port      = 0
    to_port        = 65535
  }

  egress {
    protocol       = "ANY"
    description    = "Allow all ports"
    from_port      = 0
    to_port        = 65535
  }
}

resource "yandex_kubernetes_cluster" "k8s_zonal_cluster" {
  name        = "uralintern-k8s"
  description = "K8s cluster for uralintern project"

  network_id = "${yandex_vpc_network.default.id}"

  master {
    version = "1.29"
    zonal {
      zone      = "ru-central1-d"
      subnet_id = "${yandex_vpc_subnet.default-central1-d.id}"
    }

    public_ip = true

    security_group_ids = ["${yandex_vpc_security_group.group1.id}"]

    maintenance_policy {
      auto_upgrade = true

      maintenance_window {
        start_time = "15:00"
        duration   = "3h"
      }
    }

    master_logging {
      enabled = false
    }
  }

  service_account_id      = "${yandex_iam_service_account.sa.id}"
  node_service_account_id = "${yandex_iam_service_account.sa.id}"

  release_channel = "REGULAR"
}

resource "yandex_kubernetes_node_group" "my_node_group" {
  cluster_id  = "${yandex_kubernetes_cluster.k8s_zonal_cluster.id}"
  name        = "uralintern-vm-group"
  description = "VM group for uralintern project"
  version     = "1.29"

  instance_template {
    platform_id = "standard-v2"

    network_interface {
      nat                = true
      subnet_ids         = ["${yandex_vpc_subnet.default-central1-d.id}"]
    }

    resources {
      memory = 2
      cores  = 2
    }

    boot_disk {
      type = "network-hdd"
      size = 64
    }

    scheduling_policy {
      preemptible = false
    }

    container_runtime {
      type = "containerd"
    }
  }

  scale_policy {
    auto_scale {
      min = 1
      max = 2
      initial = 1
    }
  }

  allocation_policy {
    location {
      zone = "ru-central1-d"
    }
  }

  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true

    maintenance_window {
      day        = "monday"
      start_time = "15:00"
      duration   = "3h"
    }

    maintenance_window {
      day        = "friday"
      start_time = "10:00"
      duration   = "4h30m"
    }
  }
}

resource "yandex_container_registry" "container_registry" {
  name      = "uralintern-registry"
  folder_id = local.folder_id
}

resource "yandex_mdb_postgresql_cluster" "db" {
  name        = "uralintern-db"
  environment = "PRESTABLE"
  network_id  = "${yandex_vpc_network.default.id}"

  config {
    version = 15
    resources {
      resource_preset_id = "c3-c2-m4"
      disk_type_id       = "network-hdd"
      disk_size          = 10
    }
  }

  maintenance_window {
    type = "ANYTIME"
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = "${yandex_vpc_subnet.default-central1-a.id}"
  }

  host {
    zone      = "ru-central1-d"
    subnet_id = "${yandex_vpc_subnet.default-central1-d.id}"
  }
}