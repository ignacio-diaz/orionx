import json, hmac, requests, time
import string
from hashlib import sha512
import ccxt

bnb = ccxt.binance

#bnb.withdraw(code=code, amount= amount, address= address, tag=tag)

def hmac_sha512(secret_key, timestamp, body):
    # para usar hmac es necesario convertir el secret key 
    # de string utf-8 a bytearray
    key = bytearray(secret_key, 'utf-8')
    msg = str(timestamp) + str(body)

    # ademas sha512 requiere de strings codificados
    msg = msg.encode('utf-8')

    return hmac.HMAC(key, msg, sha512).hexdigest()

def currency(api_key, secret_key, code):
    query_str = f"""
    query {{
        currency(code:"{code}") {{
            units
            myWallet {{
                _id
            }}
        }}
    }}"""

    variables = {}
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

    # String del codigo HMAC
    signature = str(hmac_sha512(secret_key, timestamp, body))

    headers = {
        'Content-Type': 'application/json',
        'X-ORIONX-TIMESTAMP': timestamp, # Marca de tiempo actual
        'X-ORIONX-APIKEY': api_key, # API Key
        'X-ORIONX-SIGNATURE': signature, #  Firma
    }

    # Se envia usando POST y 
    # se usa el parametro data para enviar los datos del body
    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    # levanta un error si la peticion fue rechazada
    response.raise_for_status()
    # se decodifican los datos desde json
    data = json.loads(response.text)
    data = {"units": data['data']['currency']["units"], "walletId": data['data']['currency']["myWallet"]["_id"]}

    return data



def withdraw(api_key, secret_key, code, amount, address=str, tag=None, params=None):
    wallet = currency(api_key, secret_key, code)
    if tag:
        address = address+"#"+tag
    if "network" in params:
        network = params.get("network")

    #se crea el mensaje para poner posiciones
    query_str = f"""mutation {{
                        sendCrypto(fromWalletId: "{wallet['walletId']}", toAddressCode: "{address}", amount: {amount * 10 ** wallet['units']}, network: "{network}") {{
                            _id
                        }}
                    }}"""

    # se junta en una sola variable
    query = {
        'query': query_str,
    }

    # Contenido total de la consulta en JSON
    body = json.dumps(query)  

    # Marca de tiempo en segundos convertido a string
    # (el header solo acepta strings)
    timestamp = str(time.time())

    # String del codigo HMAC
    signature = str(hmac_sha512(secret_key, timestamp, body))

    headers = {
        'Content-Type': 'application/json',
        'X-ORIONX-TIMESTAMP': timestamp, # Marca de tiempo actual
        'X-ORIONX-APIKEY': api_key, # API Key
        'X-ORIONX-SIGNATURE': signature, #  Firma
    }

    # Se envia usando POST y 
    # se usa el parametro data para enviar los datos del body
    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    # levanta un error si la peticion fue rechazada
    response.raise_for_status()
    # se decodifican los datos desde json
    data = json.loads(response.text)
    data = data['data']["sendCrypto"]['_id']

    return data

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY (debe tener permiso de 'send': ")
    secret_key = input("Ingresa tu SECRET_KEY: ")
    asset = input("Ingresa el asset que deseas enviar: ")
    amount = float(input("escribe el monto que deseas enviar: "))
    address = input("a que direccion deseas enviar?: ")
    tag = input("agregar el tag (memo) de ser necesario. de lo contrario, aprieta enter: ")
    network = input("escribe la red que deseas ocupar: ")
    print(withdraw(api_key, secret_key, asset, amount, address, tag, params={"network": network} ))
