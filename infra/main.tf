# billing-service infrastructure, applied from main by the platform pipeline.
# Sandbox note: the stack in agent-scope/phase1/terraform creates these resources; this file
# is the service's own declaration of them (evidence for the map builder), not applied alone.
provider "aws" {
  region = "us-east-2"
}

resource "aws_cloudwatch_log_group" "staging" {
  name = "billing-staging-logs"
}

resource "aws_cloudwatch_log_group" "prod" {
  name = "billing-prod-logs"
}

resource "aws_dynamodb_table" "ledger" {
  name         = "billing-db"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  tags         = { service = "billing", data = "customer-pii" }
}

resource "aws_dynamodb_table" "ledger_staging" {
  name         = "billing-staging-db"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  tags         = { service = "billing", data = "synthetic" }
}

resource "aws_secretsmanager_secret" "stripe" {
  name = "billing-stripe-key"
}

resource "aws_secretsmanager_secret" "webhook" {
  name = "billing-signing-key"
}

# Payment events fan out to notifications through this queue.
resource "aws_sqs_queue" "events" {
  name = "payments-events"
}

data "aws_iam_role" "task" {
  name = "agentscope-task-billing"
}

data "aws_iam_role" "events" {
  name = "payments-shared-role"
}
