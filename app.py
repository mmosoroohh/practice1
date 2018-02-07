from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_sqlalchemy import SQLAlchemy

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps


app = Flask("__name__")

#config MySQL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:test123@localhost:5432/mydb1'


#init MYSQL
db = SQLAlchemy(app)

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

# Single Article
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


     # User Register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        session['show'] = False
        message = None

        if request.method == 'POST':
            if not request.form['password'] or request.form['password'] == "" or request.form['password'].isspace():
                message = "Password is required!"
            elif request.form['name'] == "" or request.form['name'].isspace():
                message ="Name cannot be empty string"
            elif not check_mail(request.form['email']) or request.form['email'] == "":
                message = "Email provided is not valid"
            else:
                for user in user_list:
                    if user.email == request.form['email']:
                        message = 'User with the provided email already exists!'
                        return render_template("register.html", error=message)

                    new_user = user(request.form['name'], request.form['email'], request.form['password'])
                    user_list.append(new_user)

                    if new_user:
                        return redirect(url_for('login'))
                    else:
                        return render_template("register.html", error = message)

            return render_template("register.html", error = message)


    # User login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
       session['show'] = False
       message = None
       if request.method == 'POST':
           if request.form['email'] =='' or request.form['password'] == '' or request.form['email'].isspace() or request.form['password'].isspace():
               message = "Email and Password are required!"
               return render_template("login.html", message = message)
            elif not check_mail(request.form['email']):
                message = "Enter a valid email address"
                return render_template("login.html", message = message)
            else:
                if len(user_list) > 0:
                    for person in user_list:
                        if user.email == request.form['email'] and person.password == request.form['password']:
                            session['logged_in'] = True
                            current_user['email'] = user.email
                            current_user['dashboard'] = user.dashboard
                            current_user['article'] = user.article
                            return redirect(url_for('index'))

                            message = "Username and Password incorrect!"
                        session['logged_in'] = False
                        return render_template("login.html", message = message)
                    else:
                        message = "User not available! Please register"
                        return render_template("register.html", message = message)

                else:
                    session['logged_in'] = False

                return render_template("login.html")



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    session['show'] = True
    if request.method == 'GET':
        

# Check if useer logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'Success')
    return redirect(url_for('login'))


# checks email address
def check_mail(user_email):
     match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', user_email)

    if match == None:
        return False
    else:
        return True

   
   

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html') 

if  __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)