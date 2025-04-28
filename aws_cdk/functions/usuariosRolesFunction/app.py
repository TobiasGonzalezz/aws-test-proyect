import boto3

def lambda_handler(event, context):
    iam = boto3.client('iam')
    response = iam.list_roles()

    roles = [role['RoleName'] for role in response['Roles']]
    
    print(f"Roles encontrados: {roles}")
    return roles
