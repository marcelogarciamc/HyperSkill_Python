import requests

starting_currency_code = input().lower()
r = requests.get(f'http://www.floatrates.com/daily/{starting_currency_code.lower()}.json').json()
cache = {}
if starting_currency_code != 'usd':
    cache['usd'] = float(r['usd']['rate'])
if starting_currency_code != 'eur':
    cache['eur'] = float(r['eur']['rate'])

while True:
    target_currency_code = input().lower()
    if target_currency_code == "":
        break
    starting_quantity = float(input())
    print("Checking the cache...")
    xchange_rate = float(r[target_currency_code]['rate'])
    if target_currency_code in cache.keys():
        print('Oh! It is in the cache!')
    else:
        print('Sorry, but it is not in the cache!')
        cache[target_currency_code] = xchange_rate
    xchange_quantity = round(starting_quantity * xchange_rate, 2)
    print(f'You received {xchange_quantity} {target_currency_code.upper()}.')
