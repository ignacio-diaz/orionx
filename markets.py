import json
import time
import requests
from new_position import hmac_sha512 

def get_markets(api_key, secret_key):
    query_str = '''
    query {
        markets {
            code
            isMaintenance
            name
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
    data = data['data']
    markets = data['markets']
    final_markets = []
    for market in markets:
        if market['isMaintenance'] == False:
            final_markets.append(market['code'])

    return final_markets
