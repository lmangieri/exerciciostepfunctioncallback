import boto3
import json

def lambda_handler(event, context):
    # Extrai o valor do argumento fruit_name do evento
    fruit_name = event['fruit_name']

    # Configura o cliente do AWS Step Functions
    stepfunctions_client = boto3.client('stepfunctions')

    # Define o nome ou ARN da sua Step Function
    state_machine_arn = 'arn:aws:states:us-east-1:157351054870:stateMachine:LeandroStepFunctionTest'

    # Define os dados de entrada da Step Function
    input_data = {
        'fruit_name': fruit_name
    }

    try:
        # Inicia a execução da Step Function
        response = stepfunctions_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)
        )
        
        # Obtém o ID da execução da Step Function
        execution_arn = response['executionArn'].split(':')[-1]

        return {
            'statusCode': 200,
            'body': f'Step Function execution started. Execution ARN: {execution_arn}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
