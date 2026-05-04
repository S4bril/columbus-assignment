provider "aws" {
  region = var.aws_region
}

# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Package the Lambda function code
data "archive_file" "weather_temperature_service" {
  type        = "zip"
  source_dir = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

# Lambda function
resource "aws_lambda_function" "weather_temperature_service" {
  filename      = data.archive_file.weather_temperature_service.output_path
  function_name = "weather_temperature_service"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  code_sha256   = data.archive_file.weather_temperature_service.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Environment = "production"
    Application = "weather_temperature_service"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.weather_temperature_service.function_name}"
  retention_in_days = 7
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function_url" "weather_temperature_service" {
  function_name      = aws_lambda_function.weather_temperature_service.function_name
  authorization_type = "NONE"
}

output "lambda_function_url" {
  value = aws_lambda_function_url.weather_temperature_service.function_url
}
