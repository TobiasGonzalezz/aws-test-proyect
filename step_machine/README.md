# sam-app-stepfunction

## Como ejecutar localmente un step machine

1. Tener AWSCLI y SAM correctamente instalado

   ```
   sudo apt  install awscli
   ```

   ```
   sudo pip3 install aws-sam-cli
   ```
2. Generar un Step Machine utilizando un archivo asl.json
3. Armar correctamente el template
4. Tener la carpeta events y un evento vacio para poder hacer la prueba: asi debe estar armado:
   ├── README.md
   ├── __init__.py
   ├── events
   │   └── step_event.json
   ├── functions
   │   ├── __init__.py
   │   ├── lambda_1
   │   │   ├── __init__.py
   │   │   ├── app.py
   │   │   └── requirements.txt
   │   └── lambda_2
   │       ├── __init__.py
   │       ├── app.py
   │       └── requirements.txt
   ├── samconfig.toml
   ├── statemachine
   │   └── stepmachine.asl.json
   └── template.yaml
5. Inicializar la engine de docker
6. Darles permisos de ejecución al sh enviando

   ```
   chmod +x init_local.sh
   ```
7. Ejecutar el siguiente comando

   ```
   ./init_local.sh
   ```

   para poder exponer nuestros lambdas a: http://localhost:8083 esto nos va a permitir interactuar con nuestro step machine o api gateway, esto lo hace via docker
8. En otra terminal ejecutar

   ```
   aws stepfunctions start-execution \
     --state-machine-arn "arn:aws:states:us-east-1:123456789012:stateMachine:ParallelStateMachine" \
     --input file://events/step_event.json \
     --endpoint http://localhost:8083
   ```

La respuesta debe ser esta:

```
{
    "executionArn": "arn:aws:states:us-east-1:123456789012:execution:ParallelStateMachine:f9470433-5691-4229-af9e-a261bddc21fd",
    "startDate": 1746559793.577
}
```

Y con ese excutionArn podremos ver las distintas respuestag:

▶️ Ejecutar la state machine:

```
aws stepfunctions --endpoint http://localhost:8083   --no-sign-request --region us-east-1   start-execution   --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:ParallelStateMachine   --input '{}'
```

🔎 Ver estado de la ejecución:

```
aws stepfunctions --endpoint http://localhost:8083   --no-sign-request --region us-east-1   describe-execution   --execution-arn "
```

📜 Ver historia completa de eventos:

```
aws stepfunctions --endpoint http://localhost:8083
  --no-sign-request --region us-east-1
  get-execution-history
  --execution-arn "
```
