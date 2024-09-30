import json
 
base_de_pokedatos = {
    "charmander":{
        "no.": 4,
        "tipo": "fuego",
        "color": "rojo"
 
    },
    "squirtle":{
        "no.": 7,
        "tipo": "agua",
        "color": "azul"
    },
    "bulbasaur":{
        "no.": 1,
        "tipo": "planta",
        "color": "verde"
    }
}
 
def handler(event, context):
    print(event)
    if "queryStringParameters" not in event or  "pokemon" not in event["queryStringParameters"]:
        return {
            'statusCode': 400,
            'body': json.dumps("No se mando ningun pokemon")
        }
 
    pokemon_solicitado = event["queryStringParameters"]["pokemon"]
    if pokemon_solicitado in base_de_pokedatos:
        return {
            'statusCode': 200,
            'body': json.dumps(base_de_pokedatos[pokemon_solicitado])
        }
    return {
            'statusCode': 404,
            'body': json.dumps("No hay records para ese pokemon")
        }
 