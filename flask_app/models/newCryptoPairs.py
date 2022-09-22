import requests
tokens = {}




tokens['ETH/USD'] = requests.get('https://api.kraken.com/0/public/Depth?pair=ETHUSD').json()['result']['XETHZUSD']['bids'][0][0]
tokens['CRV/USD'] = requests.get('https://api.kraken.com/0/public/Depth?pair=CRVUSD').json()['result']['CRVUSD']['bids'][0][0]
tokens['SOL/USD'] = requests.get('https://api.kraken.com/0/public/Depth?pair=SOLUSD').json()['result']['SOLUSD']['bids'][0][0]
tokens['SHIB/USD'] = requests.get('https://api.kraken.com/0/public/Depth?pair=SHIBUSD').json()['result']['SHIBUSD']['bids'][0][0]
print(tokens['ETH/USD'])


resp = requests.get('https://api.kraken.com/0/public/AssetPairs')

json = resp.json()['result']
print(json)