import json, time, requests
from new_position import hmac_sha512 

def query_market_amount_to_spend(market, amount, sell, api_key, secret_key):
    query_str = f'''
    query{{
        marketEstimateAmountToSpend(marketCode: "{market}", amount: {amount}, sell: {sell})
    }}
    '''

    body = json.dumps({'query': query_str})
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
    amount_to_spend = data['data']["marketEstimateAmountToSpend"]
    
    return amount_to_spend

if __name__ == "__main__":
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")
    market = input("Ingresa el mercado de tu interés : ")
    amount = input("Ingresa el monto que deseas ver (en notación máquina) : ")
    sell = input("Comprar(C) o Vender(V)? : ")
    if sell == "C" or sell == "c":
        sell = "false"
        sell_w = "comprar"
    elif sell == "V" or sell == "v":
        sell = "true"
        sell_w = "vender"
    else:
        raise ValueError("no se puso v o c")
    print(f"para {sell_w} {amount} en el mercado {market}, debes usar {query_market_amount_to_spend(market, amount, sell, api_key, secret_key)} unidades de la moneda secundaria.")