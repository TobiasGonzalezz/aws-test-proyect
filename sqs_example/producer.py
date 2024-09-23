import boto3
import json
from config import AWS_URL_QUEUE

queue_url = AWS_URL_QUEUE # URL_QUEUE es la URL de la cola de mensajes
 
client = boto3.client(
    'sqs',
)
 
for i in range(20):
 
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({"Numero de mensaje":i})
    )
 
print(response)