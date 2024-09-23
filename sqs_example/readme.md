# Que es Amazon SQS?

Es muy útil para desacoplar componentes, permitir el procesamiento asíncrono y mejorar la escalabilidad de aplicaciones distribuidas. Te permite gestionar picos de carga, realizar reintentos automáticos y construir arquitecturas robustas y resilien.

## Sobre el proyecto

Tenemos 2 py ejecutables consumer y producer.

Producer es simplemente un for que va a enviar 20 mensajes con una enumeración

Consumer simplemente va a recibirlos con el numero maximo de mensajes que le indiquemos, el polling para volver a intentar a buscar y el timeout.

por mas que le pedi 10 mensajes me devolvio un unico mensaje y fuera de orden y cada vez que pidamos vamos a recibir 

recordar que hay que eliminar los mensajes una veez los procesamos correctamente. 

recordar que al crear el queue si nosotros le damos un tiempo de retecion de mensajes luego de ese tiempo se iran en mi caso al ser una prueba puse 6 minutos.

recordar que en mi caso el tiempo de espera de visibilidad es de 30 segundos si nosotros luego de verlos queremos disponibilizarlos para otro consumidor este tendra 30 segundos hasta que nosotros lo eliminiemos en el consumidor final. 

example de contenido de un mensaje:

`{'MessageId': '9c5c929f-887d-44eb-b002-de3395fb842a', 'ReceiptHandle': 'AQEBJ86A2R1Y/wOwSnGyCjbFO9pV/TkSnGB8m8JeZqpshq9NsB8uQ2EAJ1t6aWYoKK5sylqN92Egvv8JLAQDDxVWj0bKIiA/vLrUn4p4HZOijfzth0iQkbVzsdo0mch+w+/Ot6EMUIkvBliFNC0hyuAAOvCBTnr8zjO5aF8ZHgHc4TiaZGxPKEkRbS/WBmsLgoGcCcH/ilN2Thge6DwuvT+2oNysDgMmpQNzf6poXoRPLwa8843wQb2Gd2VhZMnrZNXi+rsDJlqmcoEIYvXFjCtntBO85oaVB9qmO3sPcV9DsVRfwlGVtZf3uifw+wZHVqIZupKYYUtFFXhOySBqxUkTk58jzU2OKh7kOByRSmgr5VPTToNtd0Cq+w89kyQHy4sMLdEWTgZDJglQ2fnOeAd5Jg==', 'MD5OfBody': '9825900f155b730e92b820f0aa052f6f', 'Body': '{"Numero de mensaje": 2}'}`

le debemos enviar el recibeHandle para que sqs entienda que ya lo procesamos.
