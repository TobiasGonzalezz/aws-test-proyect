Poder levantar y bajar lambdas de manera rapida e eficiente utilizando SDK. Cómo Usarlo

# Como levantar localmente el CDK:
<!-- ## Dar permisos de ejecución al script:
`chmod +x local_deploy.sh`

## Ejecuta el script:
`./local_deploy.sh` -->
1. Utilizar una versión estable de WSL
2. Realizar un entorno virutal de venv con py 3.12
3. Instalar los requirements.txt
4. Instalar sudo npm install -g aws-cdk

# Como ejecutar los comandos de CDK:
1. `cdk diff` para ver los cambios
2. `cdk deploy --region us-east-1 --profile default` para hacer deploy de los cambios

# Como realizar pruebas locales:
1. `cdk synth` que nos devuelve en consola el contenido que debemos pegar en el archivo template.yml para que podamos trabajar nuestro proyecto como si fuera sam, nos sirve para poder tirar comandos como `sam local invoke`
2. tener SAM correctamente instalado.
3. Utilizar `sam local invoke` y ver las opciones que nos aparece utizar la que necesitemos ejemplo:
`$ sam local invoke`:
Error: You must provide a function logical ID when there are more than one functions in your template. Possible options in your template: ['horariosMundialFunction', 'usuariosRolesFunction']
4. `$ sam local invoke horariosMundialFunction` para invocar la función y ver su respuesta.

# Errores comunes de CDK:
1. This CDK deployment requires bootstrap stack version '6', but during the confirmation via SSM parameter /cdk-bootstrap/hnb659fds/version the following error occurred: AccessDeniedException. Debemos enviar el comando `cdk bootstrap` que va a levantar todos los permisos para que nuestro rol/usuario pueda utilizar esta configuración.
2.  
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