from datetime import datetime

def lambda_handler(event, context):
    hora_arg = datetime.now()
    print(f'Son las {hora_arg}')
    return str(hora_arg)
