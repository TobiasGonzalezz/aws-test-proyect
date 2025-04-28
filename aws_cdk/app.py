#!/usr/bin/env python3

from aws_cdk import App
from stacks.lambda_functions_stack import LambdaFunctionsStack

app = App()

LambdaFunctionsStack(app, "LambdaFunctionsStack")

app.synth()