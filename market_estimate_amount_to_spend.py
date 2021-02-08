import json, time, requests
from new_position import hmac_sha512 

def query_market_amount_to_spend(market, amount, sell, api_key, secret_key):
    query_str = '''
    query($marketCode: ID!, $amount: Float!, $sell: Boolean!){
        marketEstimateAmountToSpend(marketCode: $marketCode, amount: $amount, sell: $sell)
    }
    '''
    variables = {
        'marketCode': market,
        'amount': amount,
        'sell': sell
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

    response = requests.post('https://api2.orionx.com/graphql', headers=headers, data=body)
    data = json.loads(response.text)
    data = data['data']
    amount_to_spend = data["marketEstimateAmountToSpend"]
    
    return amount_to_spend

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    market = input("Ingresa el mercado de tu interés : ")
    amount = input("Ingresa el monto que deseas ver (en notación máquina) : ")
    sell = input("Comprar(C) o Vender(V)? : ")
    if sell == "C" or sell == "c":
        sell = False
    elif sell == "V" or sell == "v":
        sell = True
    else:
        raise ValueError("no se puso v o c")
    print(query_market_amount_to_spend(market, amount, sell, api_key, secret_key))