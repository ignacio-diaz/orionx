import json, hmac, requests, time
from hashlib import sha512

def hmac_sha512(secret_key, timestamp, body):
    # para usar hmac es necesario convertir el secret key 
    # de string utf-8 a bytearray
    key = bytearray(secret_key, 'utf-8')
    msg = str(timestamp) + str(body)

    # ademas sha512 requiere de strings codificados
    msg = msg.encode('utf-8')

    return hmac.HMAC(key, msg, sha512).hexdigest()

def fetch_my_trades(api_key, secret_key, page, date):
    query_str = f"""query{{
        transactions (page:{page}, initPeriod:{date}, sortBy:"date"){{
            page
            totalCount
            totalPages
            hasNextPage
            hasPreviousPage
            items{{
                _id
                amount
                price
                cost
                commission
                date
                type
                hash
                description
                market {{
                    name
                }}
                currency {{
                    code
                    units
                }}
                pairCurrency {{
                    code
                    units
                }}
                explorerURL
                isInside
            }}
	    }}
    }}
"""

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
    data = json.loads(response.text)["data"]["transactions"]

    return data

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY: ")
    secret_key = input("Ingresa tu SECRET_KEY: ")
    page = input("Ingresa que numero de pagina quieres analizar: ")
    date = int(input("Ingresa el tiempo en timestamp desde qué fecha deseas que traiga la data (finalmente trae desde el comienzo de ese día): "))
    a = fetch_my_trades(api_key, secret_key, page, date)

