import time, sys
import markets
from currency import currency

"""cómo funciona este bot?
Se le entregan las configuraciones
market
is_selling
amount
api_key
secret_key"""

def balance_in_wallets(market_1):
    #balance_in_wallet_1 = float(balance_wallet(market_1, api_key, secret_key))
    wallet = currency(market_1, api_key, secret_key)
    for x in range(wallet[0]):
        wallet[1] /= 10
    wallet[1] = round(wallet[1], wallet[0])
    return wallet[1]

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
    api_key = input("Ingresa tu API_KEY : ")
    secret_key = input("Ingresa tu SECRET_KEY : ")

try:
    configs = open("configs.txt")
    market = configs.readline().strip()
    config_selling = configs.readline().strip()
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
    wallet_1 = balance_in_wallets(market_1)
    wallet_2 = balance_in_wallets(market_2)
    print(f"Tienes un monto de {wallet_1} en {market_1}, y {wallet_2} en {market_2}")
    config_selling = input(f"Deseas partir comprando[C] o vendiendo[V] {market_1}? : ")
    amount = float(input("Con qué monto deseas empezar? : "))
    decition = input("comenzar? s/N : ")
    if not(decition == "s" or decition == "S"):
        print("Cerrando el bot")
        sys.exit(1)

#comprobation 
if config_selling == "v" or config_selling == "V":
    if amount > wallet_1:
        print("monto superior a lo que hay en la billetera. cerrando bot.")
        sys.exit(1)
elif config_selling == "c" or config_selling == "C":
    if amount > wallet_2:
        print("monto superior a lo que hay en la billetera. cerrando bot.")
        sys.exit(1)
else:
    print("bot mal configurado (V o C). Cerrando el bot")
    sys.exit(1)


