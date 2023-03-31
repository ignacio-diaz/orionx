import json, time, requests
from new_position import hmac_sha512 

def get_balance(api_key, secret_key):

    query_str = '''
    query{
        me {
            wallets {
                currency {
                    code
                    isCrypto
                    units
                }
                balance
                availableBalance
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

    new_balance = {}

    for asset in data:
        if asset["availableBalance"] == asset["balance"]:
            free = None
            used = None
        else:
            free = asset["availableBalance"] / 10 ** asset["currency"]["units"]
            used = (asset["balance"] - asset["availableBalance"]) / 10 ** asset["currency"]["units"]
        total = asset["balance"] / 10 ** asset["currency"]["units"]
        new_balance[asset["currency"]["code"]] = {
            "free": free,
            "used": used,
            "total": total
            }

    return new_balance


if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    
    balance = get_balance(api_key, secret_key)
    print(balance)

