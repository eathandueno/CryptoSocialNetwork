from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.CryptoPairs import CryptoPair
from flask_app.models.crypto_assets import CryptoAsset
from flask import flash
from flask_app.models.LinkedList import siphon
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
        self.wallet_items = []
        self.percent = 0.0
        self.totalCash = 0
# Now we use class methods to query our database
    @classmethod
    def get_all(cls, data):
        query = "SELECT * from users where id != %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query, data)
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

    def matchWalletToAsset(self, cryptos):
        for item in self.wallet_items:
            for crypto in cryptos:
                if not siphon(item.asset_name, crypto.search):
                    pass
                else:
                    item.price = float(crypto.fetch_price())


    def walletPercent(lists, cryptos):
        for user in lists:

            user.matchWalletToAsset(cryptos)
            for asset in user.wallet_items:
                    buy = float(asset.buy_price)
                    price = float(asset.price)
                    
                    if buy < price:
                        asset.percent = float("{:.2F}".format(((asset.price / asset.buy_price)-1) * 100))
                    elif buy > price:
                        asset.percent = float("{:.2F}".format(((asset.price / asset.buy_price )-1)*100))
                    else:
                        asset.percent = int(0)
    
    def totalPercent(lists):
        for user in lists:
            currentValue = 0
            purchaseValue = 0
            for asset in user.wallet_items:
                purchaseValue += asset.buy_price * asset.asset_amount
                if asset.price == None:
                    currentValue += asset.buy_price * asset.asset_amount
                else:
                    currentValue +=asset.price * asset.asset_amount
            user.totalCash = currentValue
            if currentValue > purchaseValue:
                user.percent = float("{:.2F}".format((currentValue / purchaseValue) *100))
            elif currentValue < purchaseValue:
                user.percent = float("{:.2F}".format(((currentValue/purchaseValue)-1)*100))
            else:
                user.percent = 0.0

    def sortPercent(lists):
        return lists.percent