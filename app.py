from flask import Flask, render_template,request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST': 
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter((User.Username==username) | (User.email==email)).first()
        if existing_user:
            flash('Username or email already exists')
        else:
            # hashed_password = generate_password_hash(password)
            new_user = User(username=username,email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')    

if __name__ == "__main__":
    app.run(debug=True)