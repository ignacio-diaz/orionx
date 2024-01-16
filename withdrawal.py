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



def withdraw(
        self, api_key, secret_key, code, amount:float, address:str, tag=None, params=None
    ):
        wallet = self.currency(api_key, secret_key, code)
        if "network" in params:
            network = params.get("network")

        query_str_wallet_id = f"""query {{
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
        query = {
            "query": query_str_wallet_id,
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
            if wallet['currency']['code'] == code:
                wallet_id =  wallet['_id']
                asset_units = wallet['currency']['units']
    

        # se crea el mensaje para poner posiciones
        query_str = f"""mutation {{sendCrypto(clientId:{address}, amount:{amount * 10 ** asset_units}, network:{network}, fromWalletId:{wallet_id}) {{
                        _id
                        amount
                        commission
                        }}
                    }}"""

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
        data = data["data"]["sendCrypto"]["_id"]

        return data