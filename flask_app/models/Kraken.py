from unittest import result
import requests
from LinkedList import LinkedList
from LinkedList import Cryptos
resp = requests.get('https://api.kraken.com/0/public/AssetPairs')

json = resp.json()['result']

# def siphon(request, string):
    
#     for i in range(0,len(string)):
#         if string[i:i + len(request):] == request:
#             return True

# print(json)

# def fetch_pairs(ticker):
#     results = []
#     for value in json:
#         if not siphon(ticker, value):
#             pass
#         else:
#             results.append(Cryptos(json[value]))
            
#     return results



def get_all():
    linkedTest = LinkedList()
    for value in json:
        
        altname = json[value]['altname']
        base = json[value]['base']
        quote = json[value]['quote']
        linkedTest.appendList(Cryptos(altname,base,quote))
        
    return linkedTest
all = get_all()
print(all.getByContent('SOLUSD'))
print(all.get(566).fetch_price())
