from dotenv import load_dotenv
import os

load_dotenv()
# Acceder a la URL segura
AWS_URL_QUEUE = os.getenv('AWS_QUEUE_URL')