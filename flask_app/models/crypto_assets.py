from flask import flash

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
    
    # @staticmethod
    # def validate_asset(form):
        


    @classmethod
    def get_wallet(cls, data):
        query = "SELECT * from crypto_assets WHERE %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_wallets(cls):
        query = "SELECT * from crypto_assets;"
        results = connectToMySQL(db).query_db(query)
        wallets = []
        for wallet in results:
            wallets.append(cls(wallet))
        return wallets

    @classmethod
    def add_wallet_asset(cls, data):
        query = "INSERT into crypto_assets(asset_name, asset_amount, wallet_owner, buy_price) values (%(asset_name)s, %(asset_amount)s, %(wallet_owner)s, %(buy_price)s);"
        return  connectToMySQL(db).query_db(query, data)