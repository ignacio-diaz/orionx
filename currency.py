import json, time, requests
from new_position import hmac_sha512 

def currency(market, api_key, secret_key):
    query_str = '''
    query($code: ID){
        currency(code: $code) {
            units
            myWallet {
                availableBalance
            }
        }
    }
    '''
    variables = {'code': market}
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

    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    data = json.loads(response.text)
    data = data['data']
    units = data['currency']['units']
    balance = data['currency']['myWallet']['availableBalance']
    
    return [units, balance]

"""
{
  "data": {
    "currency": {
      "units": 8,
      "myWallet": {
        "availableBalance": 659833
      }
    }
  }
}
"""