import yaml

def generate_template_lambda(app, stack_name):    
    cloud_assembly = app.synth()
    stack = next((s for s in cloud_assembly.stacks if s.stack_name == stack_name), None)

    if stack:
        cloudformation_template = stack.template
        sam_template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Transform": "AWS::Serverless-2016-10-31",
            "Resources": {}
        }

        for resource_name, resource in cloudformation_template.get("Resources", {}).items():
            if resource["Type"] == "AWS::Lambda::Function":
                properties = resource["Properties"]
                metadata = resource.get("Metadata", {})

                # Obtener ruta del código local desde CDK metadata
                code_path = metadata.get("aws:asset:path", ".")

                # Crear recurso compatible con SAM
                sam_resource = {
                    "Type": "AWS::Serverless::Function",
                    "Properties": {
                        "Handler": properties.get("Handler", "app.lambda_handler"),
                        "Runtime": properties.get("Runtime", "python3.12"),
                        "MemorySize": properties.get("MemorySize", 128),
                        "Timeout": properties.get("Timeout", 30),
                        "CodeUri": f"cdk.out/{code_path}", # Ruta del código local
                        "FunctionName": properties.get("FunctionName", resource_name)
                    }
                }

                # Añadir Layers si existen
                if "Layers" in properties:
                    sam_resource["Properties"]["Layers"] = properties["Layers"]

                sam_template["Resources"][properties.get("FunctionName", resource_name)] = sam_resource

        # Guardar template YAML para SAM
        template_yaml_path = "template.yaml"
        with open(template_yaml_path, "w") as yaml_file:
            yaml.dump(sam_template, yaml_file, default_flow_style=False)

        print(f"Template SAM generado en {template_yaml_path}")
    else:
        print(f"No se encontró el stack con nombre {stack_name}")
