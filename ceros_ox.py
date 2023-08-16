import json, time, requests
from new_position import hmac_sha512 

def get_ceros(api_key, secret_key):

    query_str = '''
    query{
        me {
            wallets {
                currency {
                    code
                    units
                }
            }
        }
    }'''
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
    data = data['data']["me"]["wallets"]

    ceros = {}

    for asset in data:

        asset_name = asset["currency"]["code"]
        asset_ceros = asset["currency"]["units"]

        ceros[asset_name] = asset_ceros

    return ceros


if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    ceros = get_ceros(api_key, secret_key)
    print(ceros)
