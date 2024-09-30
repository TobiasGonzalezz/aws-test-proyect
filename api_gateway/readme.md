# API Gateway

Generamos un api gateway utilizando cloudformation

En esta prueba utilice https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#aws-resource-apigateway-restapi--examples y chatGPT para que me ayude a la creacion de un template que conecte un lambda cargado adentro del yaml en vez de subirlo a s3.

Este template necesita persmisos de rol porque al crear un lambda necesita poder generar un rol el cual luego utilizaremos para enlazarlo con nuestro api gateway.

***aws cloudformation deploy --stack-name "mi-pokedex-tobias" --template-file pokedex.yaml --capabilities CAPABILITY_IAM --disable-rollback***
