
from flask import flash
import requests
from flask_app.models.crypto_assets import CryptoAsset
from flask_app.config.mysqlconnection import connectToMySQL
db = 'socialnetwork'
class CryptoPair:
    def __init__(self, data):
        self.id = data['id']
        self.crypto_base = data['crypto_base']
        self.crypto_quote = data['crypto_quote']
        self.search_base = data['search_base']
        self.search_quote = data['search_quote']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.temp_base = data['temp_base']
        self.temp_quote = data['temp_quote']
        self.price = 0.0
        self.wallet_owner = None
        

    @classmethod
    def get_all_cryptos(cls):
        query = "SELECT * from crypto_pairs;"
        results = connectToMySQL(db).query_db(query)
        cryptos = []
        for crypto in results:
            cryptos.append(cls(crypto))
        return cryptos
    
    @classmethod
    def get_crypto_pair(cls, data):
        query = "SELECT * from crypto_pairs where crypto_base = %(base)s and crypto_quote = %(quote)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    def fetch_price(crypto):
        try:
            livePrice = float((requests.get("https://api.kraken.com/0/public/Depth?pair=" + crypto.search_base + crypto.search_quote)).json()['result'][crypto.search_base + crypto.search_quote]['asks'][0][0])
            crypto.price = livePrice
        except:
            livePrice = float((requests.get("https://api.kraken.com/0/public/Depth?pair=" + crypto.search_base + crypto.search_quote)).json()['result'][crypto.temp_base + crypto.temp_quote]['asks'][0][0])
            crypto.price = livePrice
        return crypto

    @classmethod
    def get_wallet_percent(cls):
        query = "SELECT * from crypto_assets left join crypto_pairs as cryptos on asset_name = crypto_base WHERE crypto_quote = 'USD';"
        results = connectToMySQL(db).query_db(query)
        assets = []
        for asset in results:
            assetShow = cls(asset)
            asset_owner = {
                'id' : asset['id'],
                'asset_name' : asset['asset_name'],
                'asset_amount' : asset['asset_amount'],
                'wallet_owner' : asset['wallet_owner'],
                'created_at' : asset['created_at'],
                'updated_at' : asset['updated_at'],
                'buy_price' : asset['buy_price']
            }
            assetShow.wallet_owner = CryptoAsset(asset_owner)
            assets.append(assetShow)
        CryptoPair.fetch_price(assets)
        
        return assets

    
