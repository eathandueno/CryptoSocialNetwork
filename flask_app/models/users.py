from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db = 'socialnetwork'
class User:
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
        
# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        friends = []
        # Iterate over the db results and create instances of friends with cls.
        for friend in results:
            friends.append( cls(friend) )
        return friends
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