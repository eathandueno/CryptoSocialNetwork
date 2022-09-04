
# from flask_app.models.likes import Likes
from wsgiref import validate
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.messages import Messages
from flask import render_template, redirect, session, flash, request
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def register_account():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    
    user = User.add_one(data)
    session['user_id'] = user
    users = User.get_all()
    return redirect('/home')

@app.route('/login', methods=['POST'])
def login():
    
    data = {"email" : request.form['email'],
            "password" : request.form['password']}
    user_db = User.get_by_email(data)
    if not user_db:
        flash("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, data['password']):
        flash("Invalid Email or Password")
        return redirect('/')
    session['user_id'] = user_db.id
    return redirect('/home')

@app.route('/home')
def home_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    
    
    return render_template('dashboard.html', user = User.get_by_id(data), users = User.get_all() )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/message/<int:id>')
def display(id):
    self = {
        'id' : session['user_id']
    }
    data = {
        'self' : self['id'],
        'id' : id
    }   
    
    return render_template('messages.html',messages = Messages.get_all(data), friend = User.get_by_id(data), user = User.get_by_id(self))

@app.route('/submit/<int:id>', methods=['POST'])
def send_message(id):
    if not Messages.validate_message(request.form):
        return redirect('/messages/' + str(id))
    data = {
        'messages' : request.form['messages'],
        'sender' : session['user_id'],
        'particpants' : id
    }
    Messages.add_one(data)
    return redirect('/message/' + str(id))

