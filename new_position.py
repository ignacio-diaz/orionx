import json
import hmac
import requests
import time
import asyncio
from hashlib import sha512

def hmac_sha512(secret_key, timestamp, body):
    # para usar hmac es necesario convertir el secret key 
    # de string utf-8 a bytearray
    key = bytearray(secret_key, 'utf-8')
    msg = str(timestamp) + str(body)

    # ademas sha512 requiere de strings codificados
    msg = msg.encode('utf-8')

    return hmac.HMAC(key, msg, sha512).hexdigest()

async def new_position(isSelling, api_key, secret_key, variables):

  #print(f"comienzo meter {time.time()}") 
  
  #se crea el mensaje para poner posiciones
  query_str = '''
      mutation ($marketCode: ID, $amount: BigInt, $limitPrice: BigInt, $sell: Boolean ){
          placeLimitOrder(marketCode: $marketCode, amount: $amount, limitPrice: $limitPrice, sell: $sell){
              _id
          }
      }
  '''

  variables = {
      # codigo del mercado:
      # DAI - Pesos Chilenos
      #'marketCode': d['trade'],
      # 'amount' define el monto (de venta o compra) en escala 10e-8
      #'amount': int(d['amount']*100000000),
      # 'limitPrice' es el precio de compra o venta.
      #'limitPrice': d['price'],
      # 'sell' especifica si es compra o venta en booleano (sell=True => venta, sell=False => compra)
      #'sell': d['sell']
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
  data = data['data']
  if data['placeLimitOrder'] == None:
    "no hacer nadita"
    #print(f"fin meter      { time.time() }")
  await asyncio.sleep(0)