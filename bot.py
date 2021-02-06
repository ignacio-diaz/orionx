import time, sys
import markets
from currency import currency
from fees import fee_limit
from market_estimate_amount_to_spend import query_market_amount_to_spend

"""cómo funciona este bot?
Se le entregan las configuraciones
market
is_selling
amount
api_key
secret_key"""
def human_to_machine(decimals, amount):
    if decimals == 0:
        return amount
    for x in range(decimals):
        amount *= 10
    amount = round(amount, decimals)
    return amount

def machine_to_human(decimals, amount):
    if decimals == 0:
        return amount
    for x in range(decimals):
        amount /= 10
    amount = round(amount, decimals)
    return amount

def balance_in_wallets(market):
    wallet = currency(market, api_key, secret_key)
    wallet = human_to_machine(wallet[0], wallet[1])
    return wallet

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
    wallet = balance_in_wallets(market_splitted[0])
    units_amount_first_currency = currency(market_splitted[0], api_key, secret_key)
    units_amount_second_currency = currency(market_splitted[1], api_key, secret_key)
    amount_in_human = machine_to_human(units_amount_first_currency[0], units_amount_first_currency[1])
    if amount > amount_in_human:
        print("monto superior a lo que hay en la billetera. cerrando bot.")
        sys.exit(1)
elif config_selling == "c" or config_selling == "C":
    sell = False
    wallet = balance_in_wallets(market_splitted[1])
    units_amount_second_currency = currency(market_splitted[1], api_key, secret_key)
    units_amount_first_currency = currency(market_splitted[0], api_key, secret_key)
    amount_in_machine = human_to_machine(units_amount_first_currency[0], units_amount_first_currency[1])
    amount_to_buy = query_market_amount_to_spend(market, amount_in_machine, sell, api_key, secret_key)
    if amount > amount_in_human:
        print("monto superior a lo que hay en la billetera. cerrando")
        sys.exit(1)
else:
    print("bot mal configurado (V o C). Cerrando el bot")
    sys.exit(1)

#amount_in_human = machine_to_human(units[0], amount)
units_2 = currency(market_splitted[0], api_key, secret_key)
amount_in_human = machine_to_human(units_2[0], amount)
amount_to_spend = query_market_amount_to_spend(market, amount_in_human, sell, api_key, secret_key)

print("holi")
limit_fee = fee_limit(api_key, secret_key)


