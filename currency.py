import json, time, requests
from new_position import hmac_sha512 

def currency(market, api_key, secret_key):
    query_str = f'''
    query{{
        currency(code: "{market}") {{
            units
            myWallet {{
                availableBalance
            }}
        }}
    }}
    '''
    query = {
    'query': query_str
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

    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    data = json.loads(response.text)
    data = data['data']
    units = data['currency']['units']
    balance = data['currency']['myWallet']['availableBalance']
    
    return [units, balance]

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    market = input("Ingresa la moneda de tu interés : ")
    print(currency(market, api_key, secret_key))