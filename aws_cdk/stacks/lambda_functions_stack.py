import os
import yaml
from aws_cdk import (
    Stack,
    Duration,
)
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
from constructs import Construct

class LambdaFunctionsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Leer config
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "lambda_config.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Registrar los layers por nombre
        layer_map = {}
        for layer_cfg in config.get("layers", []):
            name = layer_cfg["name"]
            arn_prefix = layer_cfg["arn_prefix"]
            # Usar la última versión disponible
            version = layer_cfg["version"]
            layer_arn = f"{arn_prefix}:{version}"
            layer_version = _lambda.LayerVersion.from_layer_version_arn(
                self, f"{name}-layer",
                layer_version_arn=layer_arn
            )

            layer_map[name] = layer_version

        # Crear funciones
        for function_name, settings in config.get("lambdas", {}).items():
            function_path = os.path.join(os.path.dirname(__file__), "..", "functions", function_name)
            app_file = os.path.join(function_path, "app.py")

            if not os.path.isdir(function_path) or not os.path.isfile(app_file):
                continue

            # Layers específicos de la función
            function_layers = []
            for layer_ref in settings.get("layers", []):
                lname = layer_ref["name"]
                if lname in layer_map:
                    function_layers.append(layer_map[lname])

            fn = _lambda.Function(
                self,
                id=function_name,
                function_name=function_name,
                runtime=_lambda.Runtime.PYTHON_3_12,
                handler="app.lambda_handler",
                code=_lambda.Code.from_asset(function_path),
                timeout=Duration.seconds(settings.get("timeout", 10)),
                memory_size=settings.get("memory", 128),
                layers=function_layers,
            )

            # Agregar regla cron si está configurado
            if "cron" in settings:
                cron_cfg = settings["cron"]
                rule = events.Rule(
                    self,
                    id=f"{function_name}-ScheduleRule",
                    rule_name=cron_cfg["name"],
                    schedule=events.Schedule.expression(cron_cfg["schedule"]),
                    enabled=cron_cfg.get("enabled", True)
                )
                rule.add_target(targets.LambdaFunction(fn))