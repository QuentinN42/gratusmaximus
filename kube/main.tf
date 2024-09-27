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

module "gratus" {
  depends_on = [module.ns, module.db]
  source     = "./modules/gratus"

  image        = "quentinn42/gratusmaximus:maximus-${var.hash}"
  ns           = module.ns.name
  database_url = module.db.database_url

  host = "gratusmaximus.tools.escape.tech"
}
