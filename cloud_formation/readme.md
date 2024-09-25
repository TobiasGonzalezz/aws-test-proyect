# Cloud formation

Si no recordamos todos los campos podemos utilizar los templates ya generados por aws

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-snippets.html 

Ejemplo practico: vamos a levantar un ec2 por ende necesitamos leer que puede contener nuestro template que es requerido y que no. 

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-instance.html 

Si buscamos cloudfromation template "nuestro servicio a buscar" podemos encontrar esta guia de que puede contener nuestro template y que es cada uno de los valores. Tambien contiene examples que podemos generar.

Todo lo que no se especifica AWS va a darle un valor por defecto, tener mucho cuidado a la hora de levantar hay que saber que lo que levantamos nos lo pueden cobrar directamente, ejemplo EC2 si lo levantamos sin especificarle la instacia levantaria m1.small la cual no esta incluida en la capa gratuita de 12 meses.

¿Que es ami? Amazon Machine Image es la imagen que va a utilizar para levantar un servicio de EC2 esto tiene que ver directamente con el almacenamiento que va a utilizar.

## EC2 Cloudformation

1. Primero debemos ver todo lo anterior para entender en grandes rasgos que es lo que vamos a hacer.
2. Recordar que todo lo que no especifiquemos AWS le va a dar una valor por defecto es decir que NOS VAN A COBRAR si no prestamos atencion!!
3. ImageId: debemos buscar en aws la ami que vamos a utilizar en mi caso busque la de ubuntu que contiene capa gratuita la seleccionamos y asi tendremos la ami la cual debemos copiarla.
4. KeyName: es nuestro par de llaves si alguna vez creamos un EC2 habremos generado un par de llaves, recomiendo primero visualizar como seria generar un EC2 desde la UI de AWS antes de seguir con los otros pasos.
5. BlockDeviceMappings el root de almacenamiento que vamos a usar, deberiamos chequear cual es que tenemos libre, DeltedOnTermination significa si queremos cuando se borre el EC2 tambien se borre el disco de almacenamiento. Lo mismo para VolumeType hay que buscarlo en la UI para saber cual es el gratuito.
6. Nos dirigimos a cloudFormation para la creacion de nuestro stack pero recordar que hay que estar en la misma region que nuestra llave, en mi caso us-east-1.
7. https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create creamos nuestro stack subiendo nuestro archivo yaml.
8. Recordar que si tenemos permisos limitados en el apartado de dar un rol debemos seleccionar el correcto.
9. Stack failure options, tenemos dos opciones o hacer un roll back si algun recurso falla o solo mantener los que esten funcionando. Si estamos escribiendo un template grande y alguno recurso falla tenemos esas 2 opciones, yo recomiendo que directamente se utilice el segundo si estamos en desarrollo para que no este volviendo para atras cada vez que nos equivocamos.
10. Recordar el timeout para evitar que si alguien sube cambios y estos fallan que tenga un tiempo limite para tratar de actualizarlo.
11. Tenemos un panel derecho en cual podemos ver los eventos, resources etc.
12. Recordar que si estamos creando una instancia y esta falla si queremos utilizar el mismo nombre debemos eliminar la instancia que hizo rollback para poder utilizar ese nombre.
13. Debemos especificar los security groups haciendo lo mismo que antes https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-securitygroup.html
14. Copiamos alguna de example y recordar que si no queremos especificar al VPC podemos simplemente borrarlo que AWS nos va a devolver una por default.
15. Recordar hacer la referencia de nuestro security group que va a ser creado desde la VPC que creera por defecto AWS, si nosotros tenemos VPC propias creados por afuera del security groups podemos utilizar el SecurityGroupsId que simplemente especificariamos el ID.
16. Ahora que aplicamos el SecurityGroups debemos actualizarlo en este caso utilizando remplazando el Stack actual, luego de cargar el archivo y ir a la parte de publicar recordar ver el Change set preview
17. Recordar SecurityGoups en su documentacion nos indica que el recurso debe ser remplazo, en mi caso al primero crear el EC2 y luego añadirle los SecurityGroups se actualizo.
