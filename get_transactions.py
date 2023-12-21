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

def fetch_my_trades(api_key, secret_key, page):
    query_str = f"""query{{
        orders(sortBy: "activatedAt", sortType:DESC, page:{page}, limit:7000){{
            totalCount
            totalPages
            hasNextPage
            hasPreviousPage
            items{{
                _id
                clientId
                sell
                trades{{
                    _id
                    amount
                    price
                    totalCost
                    date
                    market{{
                        name
                        mainCurrency{{
                            units
                        }}
                        secondaryCurrency{{
                            units
                        }}
                    }}
                }}
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
    data = json.loads(response.text)["data"]["orders"]

    return data

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY: ")
    secret_key = input("Ingresa tu SECRET_KEY: ")
    #page = int(input("Ingresa que numero de pagina quieres analizar: "))
    trade_list = []
    page = 1
    last_page = 10000
    while page <= last_page:
        a = fetch_my_trades(api_key, secret_key, page)
        for trades in a["items"]:
            if trades["trades"] != []:
                for inner_trade in trades["trades"]:
                    if trades["sell"] == True:
                        trades["sell"] = "sell"
                    else:
                        trades["sell"] = "buy"
                    trade_list.append({
                        "id": inner_trade["_id"],
                        "order": trades["_id"],
                        "time": inner_trade["date"],
                        "symbol": inner_trade["market"]["name"],
                        "side": trades["sell"],
                        "price": inner_trade["price"] / 10 ** inner_trade["market"]["secondaryCurrency"]["units"],
                        "amount": inner_trade["amount"] / 10 ** inner_trade["market"]["mainCurrency"]["units"],
                        "cost": inner_trade["totalCost"] / 10 ** inner_trade["market"]["secondaryCurrency"]["units"],
                        "client_order_id": trades["clientId"]
                    })
        page += 1
        last_page = a["totalPages"]

