import markets
import time

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
    │            me invitas un café?                 │
    │ DAI:0x4df0b2b46368be952517eab612944688c11e288d │
    │                                                │
    └────────────────────────────────────────────────┘"""

print(signature)
time.sleep(5)
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
    print(f"En qué mercado te interesa tranzar? mercados disponibles: \n{market_list}\n\n")
    market = input("(Escribe el mercado sin las '' y en MAYUSCULAS): ")

print("lalala")

