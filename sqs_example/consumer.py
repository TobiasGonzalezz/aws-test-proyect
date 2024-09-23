import boto3
import sys
from config import AWS_URL_QUEUE

client = boto3.client(
    'sqs',
)
queue_url = AWS_URL_QUEUE
 
response = client.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10, # Cantidad de mensajes a recibir
    #VisibilityTimeout=60,
    WaitTimeSeconds=20, # Tiempo de espera long polling, tiene la ventaja de poder procesar algun mensaje en cuanto llegue a la cola y no ejecutar el script sin datos. 
)
if "Messages" not in response:
    print("La cola esta vacia!")
    sys.exit(0)
 
for message in response["Messages"]:
    # print(message)
    # break
 
    print(message["Body"], message["ReceiptHandle"])
    response = client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message["ReceiptHandle"]
    )