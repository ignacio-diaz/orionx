import json, hmac, requests, time
import string
from hashlib import sha512

def hmac_sha512(secret_key, timestamp, body):
    # para usar hmac es necesario convertir el secret key 
    # de string utf-8 a bytearray
    key = bytearray(secret_key, 'utf-8')
    msg = str(timestamp) + str(body)

    # ademas sha512 requiere de strings codificados
    msg = msg.encode('utf-8')

    return hmac.HMAC(key, msg, sha512).hexdigest()

def currencies(api_key, secret_key):
    query_str = """query {currencies(crypto:true) {
        code
        name
        units
        myWallet {
            _id
            availableBalance
        }
        networks {
            code
            label
        }
        metadataByNetwork {
            code
            withdrawalFee
            limitWithdrawal {
                minAmount
                currencyCode
            }
        }
    }
    }"""

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
    data = data['data']['currencies']

    return data



def withdraw(api_key, secret_key, wallet, amount, network, address):

    #se crea el mensaje para poner posiciones
    query_str = f"""mutation {{
                        sendCrypto(fromWalletId: "{wallet}", toAddressCode: "{address}", amount: {amount}, network: "{network}") {{
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
    api_key = input("Ingresa tu API_KEY (debe tener permiso de 'send'"): ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    print("""----------
    
    """)
    total_currencies = currencies(api_key, secret_key)
    print("listado de assets que puedes enviar:")
    for currency in total_currencies:
        print(currency["code"])
    print("""----------
    
    """)
    asset = input("Ingresa el asset que deseas enviar : ")
    units = int
    networks = []
    wallet = string
    for currency in total_currencies:
        if currency["code"] == asset:
            units = currency["units"]
            networks = currency["networks"]
            wallet = currency["myWallet"]["_id"]

    print("""----------
    
    """)
    amount = float(input("Ingresa el monto que deseas enviar (sin considerar el fee): "))
    amount = int(amount * 10 ** units)
    print("""----------
    
    """)
    print("redes disponibles:")
    for network in networks:
        ntw = network["code"]

        print(f"{ntw}: costo de envio: ")
    print("""----------
    
    """)
    network = input("Ingresa la red por la que deseas enviar : ")
    print("""----------
    
    """)
    print("a que direccion deseas enviar? (si necesitas memo, ocupa el siguiente formato: direccion#memo")
    address = input("escribir direccion: ")
    print(withdraw(api_key, secret_key, wallet, amount, network, address))
