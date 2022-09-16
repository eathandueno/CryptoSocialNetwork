from flask import flash
from flask_app.models.CryptoPairs import CryptoPair

from flask_app.config.mysqlconnection import connectToMySQL
db = 'socialnetwork'
class CryptoAsset():
    def __init__(self, data):
        self.id = data['id']
        self.asset_name = data['asset_name']
        self.asset_amount = data['asset_amount']
        self.wallet_owner = data['wallet_owner']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.buy_price = data['buy_price']
        self.percent = None
        self.price = None
    
    @classmethod
    def add_wallet_asset(cls,data):
        query = "SELECT * from crypto_assets left join users as owner on crypto_assets.wallet_owner = owner.id where owner.id = %(wallet_owner)s and asset_name = %(asset_name)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        if results:
            asset = cls(results[0])
            asset.buy_price == (  (float(asset.buy_price) * float(asset.asset_amount)) + ( float(data['buy_price']) * float(data['asset_amount']))  )  / (float(asset.asset_amount) + float(data['asset_amount']))
            asset.asset_amount += float(data['asset_amount'])
            
            data = {
                'id' : asset.id,
                'asset_name' : asset.asset_name,
                'asset_amount' : asset.asset_amount,
                'wallet_owner' : asset.wallet_owner,
                'buy_price' : asset.buy_price
            }
            query = "UPDATE crypto_assets SET asset_amount = %(asset_amount)s, buy_price = %(buy_price)s where id = %(id)s;"
            return connectToMySQL(db).query_db(query, data)
        else:
            query = "INSERT into crypto_assets(asset_name, asset_amount, wallet_owner, buy_price) values (%(asset_name)s, %(asset_amount)s, %(wallet_owner)s, %(buy_price)s);"
            return connectToMySQL(db).query_db(query, data)



    @classmethod
    def get_wallet(cls, data):
        query = "SELECT * from crypto_assets inner join crypto_pairs as cryptos on crypto_assets.asset_name = cryptos.crypto_base where cryptos.crypto_quote = 'USD' and wallet_owner = {};".format(data)
        results = connectToMySQL(db).query_db(query)
        matchingWallets = []
        for each in results:
            assetCase = cls(each)
            crypto_data = {
                'id' : each['cryptos.id'],
                'crypto_base' : each['crypto_base'],
                'crypto_quote' : each['crypto_quote'],
                'search_base' : each['search_base'],
                'search_quote' : each['search_quote'],
                'created_at' : each['created_at'],
                'updated_at' : each['updated_at'],
                'temp_base' : each['temp_base'],
                'temp_quote' : each['temp_quote']
            }
            assetCase.currency = CryptoPair(crypto_data)
            
            print(CryptoPair.fetch_price(assetCase.currency))

            
        return matchingWallets

    @classmethod
    def get_all_wallets(cls):
        query = "SELECT * from crypto_assets;"
        results = connectToMySQL(db).query_db(query)
        wallets = []
        for wallet in results:
            wallets.append(cls(wallet))
        return wallets

    @classmethod
    def edit_wallet_asset(cls, data):
        query = "UPDATE crypto_assets set asset_name = %(asset_name)s, asset_amount = %(asset_amount)s, buy_price = %(buy_price)s where id = %(id)s;"
        return  connectToMySQL(db).query_db(query, data)

    @classmethod
    def fetch_wallets(cls,users):
        for user in users:
            query = "SELECT * from crypto_assets where wallet_owner = {}".format(user.id)
            results = connectToMySQL(db).query_db(query)
            wallet = []
            for result in results:
                wallet.append(cls(result))
            user.wallet_items = wallet
        return users