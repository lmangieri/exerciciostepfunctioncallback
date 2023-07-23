import boto3
import uuid

def lambda_handler(event, context):
    # Parâmetro fruit_name
    print(event)
    fruit_name = event["fruit_name"]
    task_token = event['TaskToken']

    # Geração de um identificador UUID exclusivo - obs apenas para identificar unicamente o registro dynamo
    task_identifier = str(uuid.uuid4())

    # Configuração do cliente do DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table_name = 'control_step_functions_example' 
    table = dynamodb.Table(table_name)

    # Salvar dados na tabela DynamoDB
    item = {
        'task_identifier': task_identifier,
        'fruit_name': fruit_name,
        'task_token' : task_token
    }
    table.put_item(Item=item)

    # Retornar a task_id gerada
    return {
        'task_identifier': task_identifier
    }
