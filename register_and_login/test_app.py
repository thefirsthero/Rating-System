from datetime import datetime
from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables form .env

# create Flask app
app = Flask(__name__)
app.secret_key = "REDACTED"

# user credentials
# credentials = {'john':'123', 'amy': '123', 'admin':'admin'}

# read first name and password from table into tuple
# register method does not allow for two people with the same username
# therefore this method returns a tuple containing information from one row of a table

def get_credentials_tuple(user_email, userType):
    '''This function returns the credentials of the user'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    try:
        query = "select " + userType + "_name,"  + userType + "_password from " + userType + " where "  + userType + "_email = '" + user_email +"';"
        cur.execute(query)

        myresult = cur.fetchone()
        # dic = { t[0] : t[1] for t in myresult}

    except:
        myresult = None
        myconn.rollback()

    myconn.close()

    return myresult

def checkIfEmailExists():
    '''check if email exists'''
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    try:
        query = "SELECT coach_email FROM coach UNION SELECT coachee_email FROM coachee;"
        cur.execute(query)

        myresult = cur.fetchone()
        # dic = { t[0] : t[1] for t in myresult}

    except:
        myresult = None
        myconn.rollback()

    myconn.close()
    print(myresult)

    if myresult == None:
        return True
    else:
        return False
    

# index page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

# login page


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    # checkIfEmailExists()


    # retrieve info from login form
    if request.method == 'POST':

        login_email = request.form.get("email")
        login_password = request.form.get('user_password')
        # TODO: FIX THIS AS IT IS HARDCODED
        my_tuple = get_credentials_tuple(login_email, 'coach')
        # check if the email entered is registered in the database
        if my_tuple != None:
            # check if the password entered matches up to the hashed password in the database

            if check_password_hash(my_tuple[1], login_password):
                print(f"Login of {login_email} is valid!")

                # store login information on a cookie
                session['email'] = login_email
                return redirect(url_for('success'))
            else:

                # failed login
                
                print(f'Login of {login_email} is invalid!')
                return render_template('login.html', error_msg = "Incorrect password, try again.")

        else:
            return render_template("login.html", error_msg = "User has not registered yet")
            # failed login
            # print('User has not registered yet!')

    return render_template('login.html')

# code to log user out


@app.route('/logout', methods=["GET", "POST"])
def logout():
    try:
        # check if user is logged in
        if session['username']:

            # log user out
            session.pop('username', default=None)
            session.pop('email', default=None)
        return redirect('/')
    except:
        return redirect('/')

# recieve information from html form


@app.route('/register', methods=["GET", "POST"])
def register():
    #cookie
    session['register'] = 'registered'
    # global dic

    if request.method == 'POST':

        textName = request.form.get('first-name')
        textLName = request.form.get('last-name')
        textEmail = request.form.get('email')
        textPassword = request.form.get('new-password')
        userType = ''

        # Checking if coach was selected
        if 'coach1' in request.form:
            userType = 'coach'
        else:
            userType = 'coachee'

        my_tuple = get_credentials_tuple(textEmail, userType)
        emailExists = checkIfEmailExists()

        # check if the username exists in the db yet
        if emailExists is True:

            # hash password
            passwordHash = generate_password_hash(textPassword)

            # commit info to mysql
            # dic[textUsername] = passwordHash
#sess
            myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv(
                'USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

            cur = myconn.cursor()

            query = 'INSERT INTO ' + userType + ' (' + userType + '_name,'  + userType + '_surname,'  + userType + '_email,'  + userType + '_password, user_type, register_date) VALUES (%s, %s, %s, %s, %s ,%s)'
            val = [(textName, textLName, textEmail, passwordHash,
                    userType,  datetime.now(pytz.utc))]

            cur.executemany(query, val)

            myconn.commit()

            # return to index form
            return redirect('/')
        else:
            print('Email already registered, please log in!')
            return redirect(url_for('login'))

    return render_template('register.html')


# generic Flask app guard
if __name__ == '__main__':
    app.run(debug=True)
