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

def order(api_key, secret_key, orderId):

    query_str = '''
        query ($orderId: ID!){
            order(orderId: $orderId) {
                filled
                status
                trades {
                    amount
                    price
                    totalCost
                }
            }
        }
    '''

    variables = {
        'orderId': orderId,
    }
    query = {
        'query': query_str,
        'variables': variables
    }
    body = json.dumps(query)  
    timestamp = str(time.time())
    signature = str(hmac_sha512(secret_key, timestamp, body))

    headers = {
        'Content-Type': 'application/json',
        'X-ORIONX-TIMESTAMP': timestamp, # Marca de tiempo actual
        'X-ORIONX-APIKEY': api_key, # API Key
        'X-ORIONX-SIGNATURE': signature, #  Firma
    }
    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    response.raise_for_status()
    data = json.loads(response.text)
    data = data['data']['order']

    return data

if __name__ == "__main__" :
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    orderId = input("Ingresa una orderid : ")
    print(order(api_key,secret_key,orderId))