import json
import hmac
import requests
import time
from hashlib import sha512

def hmac_sha512(secret_key, timestamp, body):
    # para usar hmac es necesario convertir el secret key 
    # de string utf-8 a bytearray
    key = bytearray(secret_key, 'utf-8')
    msg = str(timestamp) + str(body)

    # ademas sha512 requiere de strings codificados
    msg = msg.encode('utf-8')

    return hmac.HMAC(key, msg, sha512).hexdigest()

def new_position(api_key, secret_key, marketCode, amount, limitPrice, sell):

    #print(f"comienzo meter {time.time()}") 

    #se crea el mensaje para poner posiciones
    query_str = '''
        mutation ($marketCode: ID, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean){
            placeLimitOrder(marketCode: $marketCode, amount: $amount, limitPrice: $limitPrice, sell: $sell){
                _id
                trades {
                    amount
                    price
                    totalCost
                }
            }
        }
    '''

    variables = {
        'marketCode': marketCode,
        'amount': int(amount),
        'limitPrice': limitPrice,
        'sell': sell
    }

    # se junta en una sola variable
    query = {
        'query': query_str,
        'variables': variables
    }

    # Contenido total de la consulta en JSON
    body = json.dumps(query)  

    # Marca de tiempo en segundos convertido a string
    # (el header solo acepta strings)
    timestamp = str(time.time())

    # Llenar con la Api Key

    # Llenar con el secret key

    # String del codigo HMAC
    signature = str(hmac_sha512(secret_key, timestamp, body))

    headers = {
        'Content-Type': 'application/json',
        'X-ORIONX-TIMESTAMP': timestamp, # Marca de tiempo actual
        'X-ORIONX-APIKEY': api_key, # API Key
        'X-ORIONX-SIGNATURE': signature, #  Firma
    }

    # url del servidor
    url = 'https://api2.orionx.com/graphql'

    # Se envia usando POST y 
    # se usa el parametro data para enviar los datos del body
    response = requests.post(url=url, headers=headers, data=body)
    # levanta un error si la peticion fue rechazada
    response.raise_for_status()
    # se decodifican los datos desde json
    data = json.loads(response.text)
    data = data['data']['placeLimitOrder']

    return data

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    marketCode = input("Ingresa el mercado de tu interés : ")
    amount = input("Ingresa el monto que deseas ver (en notación máquina) : ")
    limitPrice = input("Ingresa el precio al que quieres comprar/vender : ")
    sell = input("Comprar(C) o Vender(V)? : ")
    if sell == "C" or sell == "c":
        sell = False
    elif sell == "V" or sell == "v":
        sell = True
    else:
        raise ValueError("no se puso v o c")
    print(new_position(api_key, secret_key, marketCode, amount, limitPrice, sell))