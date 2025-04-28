Poder levantar y bajar lambdas de manera rapida e eficiente utilizando SDK. Cómo Usarlo

# Como levantar localmente el CDK:
## Dar permisos de ejecución al script:
`chmod +x local_deploy.sh`

## Ejecuta el script:
`./local_deploy.sh`

## Como ver directorio de carpetas en ubuntu
sudo apt install tree  # Para sistemas basados en Debian/Ubuntu
`tree -L 2`

tobias@LN95111422:~/lanacion/aws-test-proyect/aws_cdk$ tree -L 2
├── app.py
├── cdk.json
├── functions
│   ├── horariosMundialFunction
│   └── usuariosRolesFunction
├── layers
├── local_deploy.sh
├── pipelines
├── readme.md
├── requirements.txt
└── stacks
    └── lambda_functions_stack.py

# Como utilizar CDK
Si utilizamos Ubuntu debemos tener correctamente la version mas reciende de node.js ya que para utilizar CDK necesitamos instalarlo con nodejs.

Tener los permisos suficientes: cdk boostrap para que nuestro usuario tenga todo lo necesario para trabajar.

Instalar las librerias necesarias que ya estan armadas en el requirements.txt

Utilizar un entorno virtual en este caso de python 3.12

# Como eliminar todo de CDK 
`cdk destroy`
Esto elimina el stack que generamos, recordar que genera un ECR de nuestro usuario en S3 eliminar si no lo deseamos. 