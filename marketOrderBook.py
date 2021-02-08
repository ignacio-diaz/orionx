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

def orderBook(api_key, secret_key, marketCode):
    query_str = '''
      query marketOrderBook($marketCode: ID!, $limit: Int) {
          marketOrderBook(marketCode: $marketCode, limit: $limit) {
            sell {
              amount
              limitPrice
              accumulated
              accumulatedPrice
            }
            buy {
              amount
              limitPrice
              accumulated
              accumulatedPrice
            }
          }
        }
    '''

    variables = {
      'marketCode': marketCode,
      'limit': 15
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
      'X-ORIONX-TIMESTAMP': timestamp, 
      'X-ORIONX-APIKEY': api_key, 
      'X-ORIONX-SIGNATURE': signature, 
    }
    url = 'https://api2.orionx.com/graphql'
    response = requests.post(url=url, headers=headers, data=body)
    response.raise_for_status()
    data = json.loads(response.text)

    return data['data']['marketOrderBook']


if __name__ == "__main__":
  api_key = input("Ingresa tu API_KEY : ")
  secret_key = input("Ingresa tu SECRET_KEY : ")
  marketCode = input("Mercado a analizar : ")
  print(orderBook(api_key, secret_key, marketCode))