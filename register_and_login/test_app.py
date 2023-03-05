from datetime import datetime
from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
 
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
    myconn = mysql.connector.connect(host='localhost', user='root', passwd='Kyle123', database='rating')
    cur = myconn.cursor()
    try:
        query = "select coach_name, coach_password from coach where coach_name = '" + uname +"';"
        cur.execute(query)

        myresult = cur.fetchone()
        # dic = { t[0] : t[1] for t in myresult}

    except:
        myconn.rollback()

    myconn.close()

    return myresult

# dic = get_credentials_dict()

# index page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
 
#login page
@app.route('/login', methods=["GET", "POST"])
def login():
 
    # retrieve info from login form
    if request.method == 'POST':
        loginUN = request.form["lUN"]
        loginPass = request.form["lPass"]

        my_tuple = get_credentials_tuple(loginUN)
        # check if the username entered is registered in the database
        if my_tuple != None:

            # check if the password entered matches up to the hashed password in the database
            if check_password_hash(my_tuple[1], loginPass):
                print(f"Login of {loginUN} is valid!")
 
                # store login information on a cookie
                session['username'] = loginUN
                return redirect('/')
            else:
 
                # failed login
                print(f'Login of {loginUN} is invalid!')
                return redirect('/')
        else:
 
            # failed login
            print('User has not registered yet!')
            return redirect('/')
        

    return render_template('login.html')
 
# code to log user out
@app.route('/logout', methods=["GET", "POST"])
def logout():
    try:
        # check if user is logged in
        if session['username']:
    
            #log user out
            session.pop('username', default=None)
            session.pop('email', default=None)
        return redirect('/')
    except:
        return redirect('/')
 
# recieve information from html form
@app.route('/register', methods=["GET", "POST"])
def register():
    session['register'] = 'registered'
    # global dic
    
    if request.method == 'POST':
        textPassword = request.form["txtPswd"]
        textUsername = request.form["txtUN"]

        my_tuple = get_credentials_tuple(textUsername)
        # check if the username exists in the db yet
        if my_tuple == None:

                # hash password
                passwordHash = generate_password_hash(textPassword)

                # commit info to mysql
                # dic[textUsername] = passwordHash
                myconn = mysql.connector.connect(host='localhost', user='root', passwd='Kyle123', database='rating')
                cur = myconn.cursor()

                query = 'INSERT INTO coach (coach_name, coach_password, register_date) VALUES (%s, %s, %s)'
                val = [(textUsername, passwordHash, datetime.now(pytz.utc))]
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
