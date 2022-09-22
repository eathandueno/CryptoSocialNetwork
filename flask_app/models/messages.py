from flask import flash
from flask_app.models.users import User
from flask_app.config.mysqlconnection import connectToMySQL
db = 'socialnetwork'
class Messages(User):
    def __init__( self , data ):
            self.id = data['id']
            self.messages = data['messages']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.sender = data['sender']
            self.particpants = data['particpants']

    @staticmethod
    def validate_message(form):
        is_valid = True
        if len(form['messages']) < 0:
            flash("Messages must not be blank")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * from messages WHERE sender =  %(self)s and particpants = %(id)s or sender = %(id)s and particpants = %(self)s  order by  created_at;"
        results = connectToMySQL(db).query_db(query, data)
        messages = []
        for message in results:
            print(message['sender'])
            messages.append(cls(message)) 
        return messages
        

    @classmethod
    def add_one(cls, data):
        query = "INSERT INTO messages ( messages, sender, particpants) VALUES ( %(messages)s , %(sender)s , %(particpants)s);" 
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE messages Set messages = %(message)s WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from messages WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)
