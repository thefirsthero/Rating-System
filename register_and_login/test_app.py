'''The main function in which to run our application'''
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
from dotenv import load_dotenv

load_dotenv() # load environment variables form .env

# create Flask app
app = Flask(__name__)
app.secret_key = "REDACTED"

# user credentials
# credentials = {'john':'123', 'amy': '123', 'admin':'admin'}


'''
CREATE DATABASE university;
CREATE TABLE users(
id INT AUTO_INCREMENT,
   username VARCHAR(100),
   password VARCHAR(500),
   register_date DATETIME,
   PRIMARY KEY(id);
'''

# read first name and password from table into tuple
# register method does not allow for two people with the same username
# therefore this method returns a tuple containing information from one row of a table
def get_credentials_tuple(uname):
    '''This function returns the credentials of the user'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    try:
        query = "select coach_name, coach_password from coach where coach_name = '" + uname +"';"
        cur.execute(query)

        myresult = cur.fetchone()
        # dic = { t[0] : t[1] for t in myresult}

    except mysql.connector.DatabaseError:
        myconn.rollback()

    myconn.close()

    return myresult

# dic = get_credentials_dict()

@app.route('/', methods=["GET", "POST"])
def index():
    '''This function returns the index page'''
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    '''This function is responsible for validating a users loging credentials'''
    # retrieve info from login form
    if request.method == 'POST':
        login_un = request.form["lUN"]
        login_pass = request.form["lPass"]

        my_tuple = get_credentials_tuple(login_un)
        # check if the username entered is registered in the database
        if my_tuple is not None:

            # check if the password entered matches up to the hashed password in the database
            if check_password_hash(my_tuple[1], login_pass):
                print(f"Login of {login_un} is valid!")

                # store login information on a cookie
                session['username'] = login_un
                return render_template('home.html')
            else:

                # failed login
                print(f'Login of {login_un} is invalid!')
                return redirect('/')
        else:

            # failed login
            print('User has not registered yet!')
            return redirect('/')


    return render_template('login.html')

# code to log user out
@app.route('/logout', methods=["GET", "POST"])
def logout():
    '''This function is responsible for logging a user out'''
    try:
        # check if user is logged in
        if session['username']:

            #log user out
            session.pop('username', default=None)
            session.pop('email', default=None)
        return redirect('/')
    except mysql.connector.DatabaseError:
        return redirect('/')

# recieve information from html form
@app.route('/register', methods=["GET", "POST"])
def register():
    '''This function registers a user is our database'''
    session['register'] = 'registered'
    # global dic

    if request.method == 'POST':
        text_password = request.form["txtPswd"]
        text_username = request.form["txtUN"]

        my_tuple = get_credentials_tuple(text_username)
        # check if the username exists in the db yet
        if my_tuple is None:

            # hash password
            password_hash = generate_password_hash(text_password)

            # commit info to mysql
            # dic[text_username] = password_hash

            myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

            cur = myconn.cursor()

            query = 'INSERT INTO coach (coach_name, coach_password, register_date) VALUES (%s, %s, %s)'
            val = [(text_username, password_hash, datetime.now(pytz.utc))]
            cur.executemany(query, val)

            myconn.commit()

            # return to index form
            #dic = get_credentials_dict()
            return redirect('/')
        else:
            print('Username is taken!')
            session.pop('register', default=None)

    return render_template('register.html')



# generic Flask app guard
if __name__ == '__main__':
    app.run(debug=True)
