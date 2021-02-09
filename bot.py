import time, sys
import markets
from currency import currency
from fees import fee_limit
from market_estimate_amount_to_spend import query_market_amount_to_spend
from new_position import new_position
from order import order
from marketOrderBook import orderBook

def human_to_machine(decimals, amount):
    if decimals == 0:
        return amount
    for x in range(decimals):
        amount *= 10
    amount = int(round(amount, decimals))
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
                  ¡¡¡AÚN NO TERMINADO!!!
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

.　　　　　　　　　　　🌎 ‍　　　　. 　　　　　　　　　　　 ,　 　　　　　　　


"""
print(signature_2)
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

order_book = orderBook(api_key, secret_key, market)

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
    order_book = order_book['buy']
    #for pos in order_book:
        #if pos['accumulated'] > amount_first_currency_in_machine:
            #price_to_trade = pos['limitPrice']
            #break
elif config_selling == "c" or config_selling == "C":
    sell = False
    wallet = balance_in_wallets(market_splitted[1])
    units_amount_second_currency = currency(market_splitted[1], api_key, secret_key)
    units_amount_first_currency = currency(market_splitted[0], api_key, secret_key)
    amount_first_currency_in_machine = human_to_machine(units_amount_first_currency[0], amount)
    amount_to_buy = query_market_amount_to_spend(market, amount_first_currency_in_machine, sell, api_key, secret_key)
    if amount_to_buy > wallet:
        print("monto superior a lo que hay en la billetera. cerrando")
        sys.exit(1)
    order_book = order_book['sell']
    for pos in order_book:
        if pos['accumulated'] > amount_first_currency_in_machine:
            price_to_trade = pos['limitPrice']
            break

else:
    print("bot mal configurado (V o C). Cerrando el bot")
    sys.exit(1)


limit_fee = fee_limit(api_key, secret_key)

"""next step:
buy/sell the config amount. 
if buy, then add the (%) from what we bought and put a sell position with a price of buyed + x%.
if sell, then add the (%) from what we sold and put a buy position  with a price of selled - x%.

then every 60 secs, see if the position has been filled. If was filled, then start  the process in the other direction."""

filled = 0
cicles = 0

position = new_position(api_key, secret_key, market, (amount_first_currency_in_machine / (1 - limit_fee)), price_to_trade, sell)
if position['trades'] == []:
    trades = order(api_key, secret_key, position['_id'])
    position['trades'] = trades['trades']

total_cost = 0
total_amount = 0
PPP_price = 0
#if len(position['trades']) > 1:
for x in range(len(position['trades'])):
    if x == 0:
        PPP_price = position['trades'][x]['price'] * (position['trades'][x]['amount'] * (1 - limit_fee)) / (position['trades'][x]['amount'] * (1 - limit_fee))
        PPP_amount = position['trades'][x]['amount'] * (1 - limit_fee)
    else:
        PPP_price = ((PPP_price * PPP_amount) + (position['trades'][x]['price'] * position['trades'][x]['amount'])) / ((position['trades'][x]['amount'] + PPP_amount) * (1 - limit_fee))
        PPP_amount += (position['trades'][x]['amount'] * (1 - limit_fee))

"""now that we know at what price we really buy/sell, que put a new order with a delta %. """
print(f"Realizamos la orden en el precio {PPP_price}.")
if sell == True:
    print(f"Ahora vendemos en {( PPP_price * ( 1 + utility / 100 ) / ( 1 - limit_fee ))}")
    position = new_position(api_key, secret_key, market, PPP_amount, ( PPP_price * ( 1 + utility / 100 ) / ( 1 - limit_fee )), sell)
    if position['trades'] == []:
        try:
            trades = order(api_key, secret_key, position['_id'])
            total_amount = trades['trades']
        except:
            "no se han hecho trades aún"
    else:
        for x in range(len(position['trades'])):
            if x == 0:
                total_amount = position['trades'][x]['amount'] * (1 - limit_fee)
            else:
                total_amount += (position['trades'][x]['amount'] * (1 - limit_fee))

else:
    print(f"ahora compramos en {( PPP_price * ( 1 - utility / 100) )}")
    position = new_position(api_key, secret_key, market, (PPP_amount / ( 1 - limit_fee )), ( PPP_price * ( 1 - utility / 100) ), sell )
    if position['trades'] == []:
        try:
            trades = order(api_key, secret_key, position['_id'])
            total_amount = trades['trades']
        except:
            "no se han hecho trades aún"
    else:
        for x in range(len(position['trades'])):
            if x == 0:
                total_amount = position['trades'][x]['amount']
            else:
                total_amount += position['trades'][x]['amount']





print("holi")
