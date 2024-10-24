import json
import boto3
import os 

def lambda_handler(event, context):
    try:
        client = boto3.client('sqs')
        queue_url = os.environ['QUEUE_URL']
        
        # Recibir mensajes desde la cola SQS
        response = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # Recibe hasta 10 mensajes
            WaitTimeSeconds=20       # Long polling para reducir costos
        )
        
        # Verificar si la cola está vacía
        if "Messages" not in response:
            print("La cola está vacía!")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "No hay mensajes en la cola"
                })
            }
        
        # Procesar y eliminar mensajes
        message_list = []
        entries_to_delete = []
        for message in response["Messages"]:
            print(message["Body"], message["ReceiptHandle"])
            message_list.append(message["Body"])
            
            # Añadir mensaje a la lista de eliminaciones
            entries_to_delete.append({
                'Id': message['MessageId'],
                'ReceiptHandle': message['ReceiptHandle']
            })
        
        # Eliminar todos los mensajes procesados en un solo batch
        if entries_to_delete:
            client.delete_message_batch(
                QueueUrl=queue_url,
                Entries=entries_to_delete
            )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Finalizó el Lambda consumer correctamente",
                "messages": message_list  # Devolver mensajes procesados (opcional)
            }),
        }
    
    except client.exceptions.QueueDoesNotExist as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"La cola no existe: {str(e)}"
            })
        }
    
    except Exception as error:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Hubo un error en el Lambda consumer: {str(error)}"
            })
        }
