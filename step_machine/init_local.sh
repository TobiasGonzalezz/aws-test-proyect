#!/bin/bash

# Configuración
STATE_MACHINE_NAME="ParallelStateMachine"
STATE_MACHINE_FILE="statemachine/stepmachine.asl.json"
LAMBDA_PORT=3001
STEPFUNCTIONS_PORT=8083

# 1. Verificar Docker
echo "Verificando Docker..."
docker ps > /dev/null 2>&1 || {
    echo "ERROR: Docker no está corriendo. Por favor inicia Docker primero."
    exit 1
}

# 2. Iniciar Step Functions Local
echo "Iniciando Step Functions Local en puerto $STEPFUNCTIONS_PORT..."
docker rm -f stepfunctions-local 2>/dev/null || true
docker run -d -p $STEPFUNCTIONS_PORT:8083 --name stepfunctions-local \
  -e LAMBDA_ENDPOINT=http://host.docker.internal:$LAMBDA_PORT \
  amazon/aws-stepfunctions-local

# 3. Construir e iniciar Lambdas
echo "Construyendo e iniciando Lambdas en puerto $LAMBDA_PORT..."
sam build
sam local start-lambda --port $LAMBDA_PORT --host 0.0.0.0 > lambda-output.log 2>&1 &

# Esperar inicialización
echo "Esperando inicialización de servicios..."
sleep 8

# 4. Registrar State Machine
echo "Registrando State Machine..."

STATE_MACHINE_DEF=$(cat "$STATE_MACHINE_FILE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

CREATE_OUTPUT=$(curl -s -X POST \
  http://localhost:$STEPFUNCTIONS_PORT \
  -H "X-Amz-Target: AWSStepFunctions.CreateStateMachine" \
  -H "Content-Type: application/x-amz-json-1.0" \
  -d '{
    "name": "'"$STATE_MACHINE_NAME"'",
    "definition": '"$STATE_MACHINE_DEF"',
    "roleArn": "arn:aws:iam::123456789012:role/dummy-role"
  }')

STATE_MACHINE_ARN=$(echo "$CREATE_OUTPUT" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("stateMachineArn", ""))')

if [[ -z "$STATE_MACHINE_ARN" ]]; then
    echo "ERROR: No se pudo crear el state machine."
    echo "Respuesta: $CREATE_OUTPUT"
    exit 1
fi

echo "State Machine creado con ARN: $STATE_MACHINE_ARN"

# 5. Mostrar información de configuración
echo -e "\n\033[1m✅ Configuración lista:\033[0m"
echo "Step Functions Local: http://localhost:$STEPFUNCTIONS_PORT"
echo "Lambda Local:         http://localhost:$LAMBDA_PORT"

# IMPORTANTE: obtené el ARN de tu state machine del JSON devuelto al crearla
echo -e "\n\033[1m📌 Reemplazá <ARN_DE_TU_STATE_MACHINE> con el ARN devuelto al crearla.\033[0m"

# 6. Comando para ejecutar la state machine
echo -e "\n\033[1m▶️ Ejecutar la state machine:\033[0m"
echo "aws stepfunctions --endpoint http://localhost:$STEPFUNCTIONS_PORT \\"
echo "  --no-sign-request --region us-east-1 \\"
echo "  start-execution \\"
echo "  --state-machine-arn $STATE_MACHINE_ARN \\"
echo "  --input '{}'"

# 7. Ver ejecución (estado y resultado)
echo -e "\n\033[1m🔎 Ver estado de la ejecución:\033[0m"
echo "aws stepfunctions --endpoint http://localhost:$STEPFUNCTIONS_PORT \\"
echo "  --no-sign-request --region us-east-1 \\"
echo "  describe-execution \\"
echo "  --execution-arn \"<ARN_DE_LA_EJECUCIÓN>\""

echo -e "\n\033[1m📜 Ver historia completa de eventos:\033[0m"
echo "aws stepfunctions --endpoint http://localhost:$STEPFUNCTIONS_PORT \\"
echo "  --no-sign-request --region us-east-1 \\"
echo "  get-execution-history \\"
echo "  --execution-arn \"<ARN_DE_LA_EJECUCIÓN>\" \\"
echo "  --include-execution-data"
