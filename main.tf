provider "aws" {
  region = "us-east-1"  # Replace with your desired region
}

resource "aws_dynamodb_table" "control_step_functions_example" {
  name           = "control_step_functions_example"
  billing_mode   = "PAY_PER_REQUEST"  # You can change the billing mode as per your requirements
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES"  

  attribute {
    name = "task_identifier"
    type = "S"  # String data type for the primary key
  }

  hash_key = "task_identifier"
  
}

# Create an event source mapping to connect the DynamoDB Stream to the Lambda function
resource "aws_lambda_event_source_mapping" "example_event_source_mapping" {
  event_source_arn  = aws_dynamodb_table.control_step_functions_example.stream_arn
  function_name     = "RegistroAlteradoLbd"
  starting_position = "LATEST"  # You can choose either "LATEST" or "TRIM_HORIZON"
  batch_size        = 1
}

resource "aws_sfn_state_machine" "step_function" {
  name     = "LeandroStepFunctionTest"
  role_arn = aws_iam_role.step_functions_role.arn
  definition = <<DEFINITION
{
  "Comment": "Um exemplo de step functions com dois passos",
  "StartAt": "Passo1",
  "States": {
    "Passo1": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken", 
      "TimeoutSeconds" : 86400,
      "Parameters": {
        "FunctionName": "SalvaRegistrosLbd",
        "Payload": {
          "TaskToken.$": "$$.Task.Token",
          "fruit_name.$": "$.fruit_name"
        }
      },
      "End": true
    }
  }
}
DEFINITION
}

resource "aws_iam_role" "step_functions_role" {
  name = "StepFunctionsRole"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "permitechamadadelambdaspolicy" {
  name        = "permitechamadadelambdaspolicy"
  description = "Policy to allow calling Lambda functions"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "*"
    }
  ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.step_functions_role.name
  policy_arn = aws_iam_policy.permitechamadadelambdaspolicy.arn
}