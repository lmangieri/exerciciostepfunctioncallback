import boto3
import json

def lambda_handler(event, context):
    # Get the DynamoDB record from the event
    for record in event['Records']:
        if record['eventName'] == 'MODIFY':
            # Access the NewImage attribute
            new_image = record['dynamodb']['NewImage']

            status = new_image.get('status', {}).get('S')
            task_token = new_image.get('task_token', {}).get('S')

            if status == "concluido":
                task_output = {
                    'result': 'success',
                    'data': 'Task completed successfully!',
                }
                send_task_success(
                    task_token,
                    output=json.dumps(task_output)
                )
            else:
                send_task_failure(task_token,"not concluido")

def send_task_success(task_token, output):
    client = boto3.client('stepfunctions')
    response = client.send_task_success(
        taskToken=task_token,
        output=json.dumps(output)
    )


def send_task_failure(task_token, error):
    client = boto3.client('stepfunctions')
    response = client.send_task_failure(
        taskToken=task_token,
        error=error
    )