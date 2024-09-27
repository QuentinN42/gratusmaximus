variable "hash" {
  type        = string
  description = "tf apply -var \"hash=$(git rev-parse HEAD)\""
}

module "ns" {
  source = "./modules/ns"

  name = "gratusmaximus"
}

module "db" {
  depends_on = [module.ns]
  source     = "./modules/psql"

  ns = module.ns.name
}

module "maximus" {
  depends_on = [module.ns, module.db]
  source     = "./modules/maximus"

  image        = "quentinn42/gratusmaximus:maximus-${var.hash}"
  ns           = module.ns.name
  database_url = module.db.database_url

  host = "gratusmaximus.tools.escape.tech"
}

locals {
  gratters = toset([for s in fileset("${path.module}/../services/gratters", "*/**/*") :
    replace(s, "/\\/.*/", "")
  ])
}

module "api_keys" {
  depends_on = [module.ns, module.maximus]
  source     = "./modules/api_keys"

  ns   = module.ns.name
  reqs = local.gratters
}

module "gratters" {
  depends_on = [module.ns, module.api_keys]
  source     = "./modules/gratters"

  ns          = module.ns.name
  hash        = var.hash
  gratters    = local.gratters
  maximus_url = module.maximus.svc_url
}
