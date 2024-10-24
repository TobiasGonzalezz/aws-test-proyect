import json
import random

def lambda_handler(event, context):
    status_code = random.choice([200, 500])    
    print(status_code)
    if status_code == 200:
        body = "salio todo bien"
    else:
        body = "no funciono correctamente"
    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": body,
        }),
    }
