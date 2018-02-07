from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from wtforms import Form

app = Flask("__name__")

Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if  __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
