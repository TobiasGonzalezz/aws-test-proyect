import os
from aws_cdk import (
    Stack,
    Duration,
)
import aws_cdk.aws_lambda as _lambda
from constructs import Construct

class LambdaFunctionsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        functions_root = os.path.join(os.path.dirname(__file__), "..", "functions")

        for function_dir in os.listdir(functions_root):
            function_path = os.path.join(functions_root, function_dir)
            app_file = os.path.join(function_path, "app.py")

            if os.path.isdir(function_path) and os.path.isfile(app_file):
                requirements_path = os.path.join(function_path, "requirements.txt")
                # TODO UTILIZAR EL REQUIREMENTS
                _lambda.Function(
                    self,
                    id=function_dir,
                    function_name=function_dir,
                    runtime=_lambda.Runtime.PYTHON_3_12,
                    handler="app.lambda_handler",
                    code=_lambda.Code.from_asset(function_path),
                    timeout=Duration.seconds(10),
                )