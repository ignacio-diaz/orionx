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

def ox_query(query_str):
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
    return json.loads(response.text)

def get_orders(asset):
    query_str = f"""
    query {{
        orders (onlyOpen:true, currencyCode:"{asset}"){{
            items{{
                _id
                market{{
                    name
                }}
                sell
            }}
        }}
    }}"""

    data = ox_query(query_str)
    orders_to_cancel = []
    for order in data['data']['orders']['items']:
        if order['sell'] == True and order['market']['name'].split(asset)[0] == "":
            orders_to_cancel.append(order['_id'])
        elif order['sell'] == False and order['market']['name'].split(asset)[1] == "":
            orders_to_cancel.append(order['_id'])

    return orders_to_cancel

def cancel_orders(orders_to_cancel):

    query_str = f"""
    mutation {{
        cancelMultipleOrders (ordersIds:{json.dumps(orders_to_cancel)}){{
		    _id
            status
        }}
    }}"""

    data = ox_query(query_str)
    if data.get('errors'):
        return data['errors'][0]['details']['code']
    return True

def withdraw(
        api_key, secret_key, code, amount:float, address:str, network:str, tag=None, params=None
    ):
        
        while True:
            orders = get_orders(code)
            cancel = cancel_orders(orders)
            if cancel == True:
                print()
                break
            else:
                if cancel == "no-orders":
                    break
                print(f"error: {cancel}")
                time.sleep(5)
        time.sleep(1)


        query_str = f"""query {{
                me {{
                    wallets {{
                        _id
                        currency {{
                            code
                            units
                        }}
                    }}
                }}
            }} """

            # se junta en una sola variable
        data = ox_query(query_str)
        data = data["data"]["me"]["wallets"]

        for wallet in data:
            if wallet['currency']['code'] == code:
                wallet_id =  wallet['_id']
                asset_units = wallet['currency']['units']
    

        # se crea el mensaje para poner posiciones
        query_str = f"""mutation {{sendCrypto(clientId:"{address}", amount:{amount * 10 ** asset_units}, fromWalletId:"{wallet_id}", network:"{network}" ) {{
                        _id
                        amount
                        commission
                        }}
                    }}"""

        # se junta en una sola variable
        data = ox_query(query_str)
        if data.get("errors"):
            return data['errors'][0]['message']
        data = data["data"]["sendCrypto"]["_id"]

        return data

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY (debe tener permiso de 'send': ")
    secret_key = input("Ingresa tu SECRET_KEY: ")
    asset = input("Ingresa el asset que deseas enviar: ")
    amount = float(input("escribe el monto que deseas enviar: "))
    address = input("a que direccion deseas enviar?: ")
    network = input("escribe la red que deseas ocupar: ")
    print(withdraw(api_key, secret_key, asset, amount, address, network="ORX"))
    print()