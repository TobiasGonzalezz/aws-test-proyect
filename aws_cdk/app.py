#!/usr/bin/env python3

from aws_cdk import App
from stacks.lambda_functions_stack import LambdaFunctionsStack
from tools import generate_template_lambda

print("Iniciando la aplicación CDK...")
app = App()

# Crear el stack
stack_name = "LambdaFunctionsStack"
LambdaFunctionsStack(app, stack_name)
print("Stack creado:", stack_name)

# Generar el template
generate_template_lambda(app, stack_name)