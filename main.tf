# Simple AWS Lambda Terraform Example
# requires 'index.js' in the same directory
# to test: run `terraform plan`
# to deploy: run `terraform apply`

variable "aws_region" {
  default = "us-east-1"
}

provider "aws" {
  region          = "${var.aws_region}"
}

// data "archive_file" "lambda_zip" {
//     type          = "zip"
//     source_dir   = "./"
//     output_path   = "lambda_function.zip"
// }

resource "aws_lambda_permission" "with_alexa" {
  statement_id  = "AllowExecutionFromAlexa"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.get_bus_lambda.function_name}"
  principal     = "alexa-appkit.amazon.com"
}

resource "aws_lambda_function" "get_bus_lambda" {
  filename         = "lambda_handler.zip"
  function_name    = "get_bus_lambda"
  role             = "arn:aws:iam::750090735300:role/executionrole"
  handler          = "next_bus.handler"
  source_code_hash = "${base64sha256(file("lambda_handler.zip"))}"
  runtime          = "python3.6"
}

// resource "aws_iam_role" "iam_for_lambda_tf" {
//   name = "iam_for_lambda_tf"

//   assume_role_policy = <<EOF
// {
//   "Version": "2012-10-17",
//   "Statement": [
//     {
//       "Action": "sts:AssumeRole",
//       "Principal": {
//         "Service": "lambda.amazonaws.com"
//       },
//       "Effect": "Allow",
//       "Sid": ""
//     }
//   ]
// }
// EOF
// }