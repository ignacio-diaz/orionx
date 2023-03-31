import json, time, requests
from new_position import hmac_sha512 

def fetch_currencies(api_key, secret_key):

    query_str = '''
    query{
        currencies {
            code
            networks{
                code
            }
            metadataByNetwork {
                code
                units
                withdrawalFee
            }
        }
    }
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
    data = data['data']['currencies']

    currencies = {}

    for asset in data:
        if len(asset["networks"]) == 0:
            continue
        else:
            net = {}
            for networks in asset["networks"]:
                for metadata in asset["metadataByNetwork"]:
                    if metadata["code"] == networks["code"]:
                        net = {"fees" : {}}
                        net["fees"][networks["code"]] = metadata["withdrawalFee"] / 10 ** metadata["units"]
            currencies[asset["code"]] = net

    return currencies


if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    
    withdrawal_fees = fetch_currencies(api_key, secret_key)
    print(withdrawal_fees)