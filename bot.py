import time, sys
import markets
from currency import currency
from fees import limit_fee

"""cómo funciona este bot?
Se le entregan las configuraciones
market
is_selling
amount
api_key
secret_key"""

def balance_in_wallets(market):
    wallet = currency(market, api_key, secret_key)
    for x in range(wallet[0]):
        wallet[1] /= 10
    wallet[1] = round(wallet[1], wallet[0])
    return wallet[1]

def market_splitter(market_list):
    for market_ in market_list:
        if market == market_['code']:
            market_name = market_['name']
    markets_names = market_name.split("/")
    market_1 = markets_names[0]
    market_2 = markets_names[1]
    return [market_1, market_2]

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

print(signature+"\n\n")
time.sleep(2)
print("calentando los motores")
time.sleep(1)
print("abrochando cinturones")
time.sleep(1)
print("dando ignición principal")
time.sleep(1)
print("despegando!\n\nnos vamos hasta Orion!")
time.sleep(1)
signature_2="""
✦ 　   　　　 　　　,　　　　　　　　　　　     　　　　 　　,　　　🌜 ‍ ‍ ‍ ‍ 　 　　　　　　　　　
　 　　　　🌞
.　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　　　　　　　　　☀　　.              

. 　 　　　　　.　　　　  　　　　　   　🚀　　　　.　　　　　　　　　　　.

　　　.　　　　　　　　　　. 　　　　　　　　　　.　　　　　　　　　　　　　.

.　　　　　　　　　　　🌎 ‍　　　　. 　　　　　　　　　　　 ,　 　　　"""
print(signature_2+"\n\n")
time.sleep(1)

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
    amount = float(configs.readline().strip())
    utility = float(configs.readline().strip())
except:
    try:
        market_list = markets.get_markets(api_key, secret_key)
    except Exception as error:
        print(f"se produjo un error ({error})")
        print("cerrando el bot.")
        sys.exit(1)
    final_markets = []
    for market in market_list:
        if market['isMaintenance'] == False:
            final_markets.append(market['code'])
    print(f"En qué mercado te interesa tranzar? mercados disponibles: \n{final_markets}\n\n")
    market = input("(Escribe el mercado sin las '' y en MAYUSCULAS): ")
    market_splitted = market_splitter(market)
    wallet_1 = balance_in_wallets(market_splitted[0])
    wallet_2 = balance_in_wallets(market_splitted[1])
    print(f"Tienes un monto de {wallet_1} en {market_splitted[0]}, y {wallet_2} en {market_splitted[1]}")
    config_selling = input(f"Deseas partir comprando[C] o vendiendo[V] {market_splitted[0]}? : ")
    amount = float(input("Con qué monto deseas empezar? : "))
    utility = float(input("Cuál es el margen de utilidad que deseas? (en %) : "))
    decition = input("comenzar? s/N : ")
    if not(decition == "s" or decition == "S"):
        print("Cerrando el bot")
        sys.exit(1)

#comprobation
market_list = markets.get_markets(api_key, secret_key)
market_splitted = market_splitter(market_list)
if config_selling == "v" or config_selling == "V":
    sell = True
    wallet_1 = balance_in_wallets(market_splitted[0])
    if amount > wallet_1:
        print("monto superior a lo que hay en la billetera. cerrando bot.")
        sys.exit(1)
elif config_selling == "c" or config_selling == "C":
    sell = False
    wallet_2 = balance_in_wallets(market_splitted[1])
    if amount > wallet_2:
        print("monto superior a lo que hay en la billetera. cerrando bot.")
        sys.exit(1)
else:
    print("bot mal configurado (V o C). Cerrando el bot")
    sys.exit(1)

fee_limit = limit_fee(api_key, secret_key)
