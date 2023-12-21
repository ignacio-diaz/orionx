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

def wallets_id(api_key:str, secret_key:str, wallet_market:str):

    query_str = f"""query {{
                me {{
                    wallets {{
                        _id
                        currency {{
                            code
                        }}
                    }}
                }}
            }} """

        # se junta en una sola variable
    query = {
        "query": query_str,
    }

    # Contenido total de la consulta en JSON
    body = json.dumps(query)

    # Marca de tiempo en segundos convertido a string
    # (el header solo acepta strings)
    timestamp = str(time.time())

    # String del codigo HMAC
    signature = str(hmac_sha512(secret_key, timestamp, body))

    headers = {
        "Content-Type": "application/json",
        "X-ORIONX-TIMESTAMP": timestamp,  # Marca de tiempo actual
        "X-ORIONX-APIKEY": api_key,  # API Key
        "X-ORIONX-SIGNATURE": signature,  #  Firma
    }

    # Se envia usando POST y
    # se usa el parametro data para enviar los datos del body
    response = requests.post(
        "https://api2.orionx.com/graphql", headers=headers, data=body
    )
    # levanta un error si la peticion fue rechazada
    response.raise_for_status()
    # se decodifican los datos desde json
    data = json.loads(response.text)
    data = data["data"]["me"]["wallets"]

    for wallet in data:
        if wallet['currency']['code'] == wallet_market:
            return wallet['_id']
    
    return "error! walletId not found."

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    wallet_market = input("Ingresa el mercado que deseas saber su walletId : ")
    wallet_id = wallets_id(api_key, secret_key, wallet_market)
    print(wallet_id)