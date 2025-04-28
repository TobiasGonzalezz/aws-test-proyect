#!/bin/bash

# Verificar las diferencias antes del despliegue
cdk diff

# Solicitar confirmación para proceder con el despliegue
read -p "¿Deseas proceder con el despliegue? (y/N): " confirm

if [ "$confirm" = "y" ]; then
    # Realizar el despliegue solo de los recursos modificados con aprobación
    cdk deploy --region us-east-1
else
    echo "Despliegue cancelado."
fi
