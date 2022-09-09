from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.CryptoPairs import CryptoPair
from flask_app.models.crypto_assets import CryptoAsset
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db = 'socialnetwork'
class User(CryptoAsset):
    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['first_name']) < 1:
            flash("First name must be longer than 2 characters")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be longer than 2 characters")
            is_valid = False
        if form['password'] != form['ConfirmPassword']:
            flash("Passwords must be the same")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid

    
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_online = data['is_online']
        self.wallet_items = None
        self.percent = None
# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * from users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def add_one(cls,data):
        query = "INSERT INTO users ( first_name , last_name , email, password ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s);" 
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def edit(cls,data):
        query = "UPDATE users Set first_name = %(fname)s, last_name = %(lname)s, email = %(email)s WHERE id = %(ID)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from users WHERE id = %(ID)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_friends(cls):
        query = "SELECT * from users left join user_has_friends as friend on users.id = users_id;"
        result = connectToMySQL(db).query_db(query)

        friends = []
        for friend in result:
            friends.append( cls(friend) )
        return friends

    @classmethod
    def get_user_wallets(cls):
        query = "SELECT * from users left join crypto_assets on users.id = crypto_assets.wallet_owner left join crypto_pairs on crypto_assets.asset_name = crypto_pairs.crypto_base where crypto_quote = 'USD';"
        results = connectToMySQL(db).query_db(query)
        wallets = []
        for result in results:
            result1 = cls(result)
            asset_info = {
                'id' : result['id'],
                'crypto_base' : result['crypto_base'],
                'crypto_quote': result['crypto_quote'],
                'search_base' : result['search_base'],
                'search_quote' : result['search_quote'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'temp_base' : result['temp_base'],
                'temp_quote' : result['temp_quote']
            }
            assetItem = CryptoPair(asset_info)
            wallet_data = {
                'id' : result['id'],
                'asset_name' : result['asset_name'],
                'asset_amount' : result['asset_amount'],
                'wallet_owner' : result['wallet_owner'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'buy_price' : result['buy_price']
            }
            
            CryptoPair.fetch_price(assetItem)
            
            assetItem.wallet_owner = CryptoAsset(wallet_data)
            result1.wallet_items = assetItem
            print(result1.wallet_items.wallet_owner.buy_price)
            if assetItem.price > result1.wallet_items.wallet_owner.buy_price:
                win = assetItem.price / result1.wallet_items.wallet_owner.buy_price 
                result1.percent = (win -1)*100
            elif assetItem.price < result1.wallet_items.wallet_owner.buy_price:
                loss = assetItem.price / result1.wallet_items.wallet_owner.buy_price
                result1.percent = -(loss*100)
            wallets.append(result1)
            
        return wallets