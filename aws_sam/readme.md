### AWS SAM

- La gran ventaja que tiene utilizar aws SAM que cloudformation es que utilizando el Type: AWS::Serverless::Function nos ahorramos tener que estar enlazando los servicios de lambda api gateway como podemos ver en otro template de este repositorio.
- Al parecer cuando la maquina del trabajo se reinicio se perdio todo el trabajo que habia armado explicando a detalle todo sobre SAM :( en un futuro se tratara de completar este bache
- Para levantar un template utilizando SAM debemos hacer el Build y Deploy, tenemos la opción de deploy --guided que nos permite ir indicando los parametros que queremos modificar, ejemplo delpoy_in: dev.

[PENDIENTE]
- ¿Que hace? !Sub !GetAtt
- Exportar un template y levantar servicios como Step Function, S3 y Api Gateway.
- Paso a paso de ejecutar AWS SAM y curiosidades que lo hacen distinto a la metodologia de uso de Cloudfront.
- Como invokar lambdas etc.
