import time
import markets
import balance
from currency import currency

"""cómo funciona este bot?
Se le entregan las configuraciones
market
is_selling
amount
api_key
secret_key"""

signature ="""
    ┌────────────────────────────────────────────────┐
    │                                                │
    │            Bot para OrionX (v1.0.0)            │
    │                por Ignacio Díaz                │
    │         https://github.com/ignacio-diaz        │
    │                                                │
    │              me invitas un café?               │
    │ DAI:0x4df0b2b46368be952517eab612944688c11e288d │
    │                                                │
    └────────────────────────────────────────────────┘"""

print(signature)
time.sleep(0)
try:
    api_key = open("api_key.txt").read().strip()
    secret_key = open("secret_key.txt").read().strip()
except:
    api_key = input("Ingresa tu API_KEY: ")
    secret_key = input("Ingresa tu SECRET_KEY: ")

try:
    configs = open("configs.txt")
    market = configs.readline().strip()
    is_selling = configs.readline().strip()
    amount = configs.readline().strip()
except:
    market_list = markets.get_markets(api_key, secret_key)
    final_markets = []
    for market in market_list:
        if market['isMaintenance'] == False:
            final_markets.append(market['code'])
    print(f"En qué mercado te interesa tranzar? mercados disponibles: \n{final_markets}\n\n")
    market = input("(Escribe el mercado sin las '' y en MAYUSCULAS): ")
    for market_ in market_list:
        if market == market_['code']:
            market_name = market_['name']
    markets_names = market_name.split("/")
    market_1 = markets_names[0]
    market_2 = markets_names[1]
    balance_in_wallet_1 = balance.balance_wallet(market_1, api_key, secret_key) 
    wallet_1_units = currency(market_1, api_key, secret_key)

print("lalala")

