from datetime import datetime
from flask import Flask, request, render_template, redirect, session, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # load environment variables form .env

'''
NB: Chossing a logging levels logs that level and all subsequent levels
logging levels:
logging.DEBUG
logging.INFO
logging.WARNING
logging.ERROR
logging.CRITICAL
'''

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='log/record.log', filemode='w',format=FORMAT)
logger.setLevel(logging.WARNING)

# create Flask app
app = Flask(__name__)
app.secret_key = "REDACTED"

# user credentials
# credentials = {'john':'123', 'amy': '123', 'admin':'admin'}

# read first name and password from table into tuple
# register method does not allow for two people with the same username
# therefore this method returns a tuple containing information from one row of a table


def get_credentials_tuple(email):
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv(
        'USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    try:
        
        query = 'SELECT coach_name, coach_password FROM coach WHERE coach_email = "' + email + '";'
        cur.execute(query)
        myresult1 = cur.fetchone()

        query = 'SELECT coachee_name, coachee_password FROM coachee WHERE coachee_email = "' + email + '";'
        cur.execute(query)
        myresult2 = cur.fetchone()

    except:
        myresult1 = None
        myresult2 = None
        myconn.rollback()

    myconn.close()

    # They have not registered
    if ((myresult1 == None) and (myresult2 == None)):
        return myresult1
    # They are a coach
    elif ((myresult1 != None) and (myresult2 == None)):
        # store user type in a cookie
        session['user_type'] = 'coach'
        return myresult1
    # They are a coachee
    elif ((myresult1 == None) and (myresult2 != None)):
        # store user type in a cookie
        session['user_type'] = 'coachee'
        return myresult2

def ifEmailExists(email):
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv(
        'USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()
    try:
        query = 'SELECT coach_email FROM coach WHERE coach.coach_email = "' + email + '" UNION SELECT coachee_email FROM coachee WHERE coachee_email = "' + email + '";'
        cur.execute(query)
        myresult = cur.fetchone()

    except:
        myresult = None
        myconn.rollback()

    myconn.close()

    if myresult is None:
        return False
    else:
        return True
    

# index page


@app.route('/', methods=["GET", "POST"])
def landingPage():
    return render_template('welcome.html')

# login page


@app.route('/home')
def success():
    # create_rating(5, 'test@gmail.com')
    return render_template('home.html')

# TODO: Change how you pass the email in when making the dropdown

@app.route('/login', methods=["GET", "POST"])
def login():

    # retrieve info from login form
    if request.method == 'POST':
        login_email = request.form.get("email")
        login_password = request.form.get('user_password')

        my_tuple = get_credentials_tuple(login_email)
        # check if the email entered is registered in the database
        if my_tuple != None:
            # check if the password entered matches up to the hashed password in the database
            if check_password_hash(my_tuple[1], login_password):

                # store login information on a cookie
                session['email'] = login_email

                logger.warning('Logged in Succesfully!')
                return redirect(url_for('success'))
            else:
                # failed login
                logger.warning('Incorrect password, try again!')
                return render_template('login.html', error_msg = "Incorrect password, try again.")
        else:
            # failed login
            logger.warning('User has not registered yet!')
            return render_template("login.html", error_msg = "User has not registered yet")
            

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
            session.pop('user_type', default=None)
            
        return redirect('/')
    except:
        return redirect('/')

# recieve information from html form


@app.route('/register', methods=["GET", "POST"])
def register():
    session['register'] = 'registered'

    if request.method == 'POST':
        textName = request.form.get('first-name')
        textLName = request.form.get('last-name')
        textEmail = request.form.get('email')
        textPassword = request.form.get('new-password')
        userType = ''

        if 'coach1' in request.form:
            userType = 'coach'
        else:
            userType = 'coachee'

        emailExists = ifEmailExists(textEmail)
        # print(emailExists)

        # check if the username exists in the db yet
        if emailExists == False:

            # hash password
            passwordHash = generate_password_hash(textPassword)

            # commit info to mysql
            myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv(
                'USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

            cur = myconn.cursor()

            query = 'INSERT INTO ' + userType + ' (' + userType + '_name,' + userType + '_surname,' + userType + '_email,' + userType + '_password, user_type, register_date) VALUES (%s, %s, %s, %s, %s ,%s)'
            val = [(textName, textLName, textEmail, passwordHash,
                    userType,  datetime.now(pytz.utc))]
            cur.executemany(query, val)

            myconn.commit()

            # return to index form
            logger.warning('Successfully registered!')
            return redirect('/')
        else:
            flash('Email already registered, please log in!')
            logger.warning('Email already registered, please log in!')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/go_to_create_rating')
def go_to_create_rating():
    return render_template('rating.html')

@app.route('/go_to_view_ratings_recieved')
def go_to_view_ratings_recieved():
    return render_template('home.html')

@app.route('/go_to_view_ratings_given')
def go_to_view_ratings_given():
    return render_template('home.html')

@app.route('/create_rating')
def create_rating():
    print('I am called')
    # TODO: REMOVE THESE HARDCODED VALUES
    rating = 2
    email = 'test@gmail.com'
    # email = request.form['email']
    # rating_num = request.form['reviewStars']
    # print(rating_num)

    print('I am called')
    # Initialise mysql
    myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv(
                'USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

    cur = myconn.cursor()

    # getting coachID or coacheeID for rater
    raterID = None
    if session['user_type'] == 'coach':
        query = 'SELECT coach_id FROM coach WHERE coach_email = "' + session['email'] + '";'
        cur.execute(query)
        raterID = cur.fetchone()[0]

        # get ratee id
        query = 'SELECT coachee_id FROM coachee WHERE coachee_email = "' + email + '";'
        cur.execute(query)
        rateeID = cur.fetchone()[0]
    else:
        query = 'SELECT coachee_id FROM coachee WHERE coachee_email = "' + session['email'] + '";'
        cur.execute(query)
        raterID = cur.fetchone()[0]

        # get ratee id
        query = 'SELECT coach_id FROM coach WHERE coach_email = "' + email + '";'
        cur.execute(query)
        rateeID = cur.fetchone()[0]

    # Populate table
    try:
            
        query = 'INSERT INTO rating (coach_id_fk, coachee_id_fk, rating, register_date) VALUES (%s, %s, %s, %s)'
        val = [(raterID, rateeID, rating, datetime.now(pytz.utc))]
        cur.executemany(query, val)

        myconn.commit()

        
    except:
        # print(query)
        # print(type(raterID))
        # print(type(rateeID))
        # print(type(rating))
        myconn.rollback()

    myconn.close()

    return render_template('home.html')
'''
function closeForm() {
        // Getting user inputted values from form
        document.getElementById("myForm").style.display = "none";
        star1 = document.getElementById("star1")
        star2 = document.getElementById("star2")
        star3 = document.getElementById("star3")
        star4 = document.getElementById("star4")
        star5 = document.getElementById("star5")
        email = document.getElementById("text2").value
        comment = document.getElementById("text1").value

        // Checking which star rating was given
        rating_number = 0
        if(star1.checked) {
            rating_number = 1
        }else if(star2.checked) {
            rating_number = 2
        }else if(star3.checked) {
            rating_number = 3
        }else if(star4.checked) {
            rating_number = 4
        }else if(star5.checked) {
            rating_number = 5
        }

        // Rating button logic
        if(email != ""){
            // If there is a comment and a rating entered : pass
            if((comment != "") && (rating_number != 0)){
                // Capture rating logic here
                create_rating(rating_number, email)
                alert("Rating captured succesfully")

            }
            // If there is something missing
            else{
                // if there is nothing entered or there is a comment wiht no rating : fail
                if((comment == "") && (rating_number == 0) || ((comment != "") && (rating_number == 0))){
                    alert("Please enter a rating.")
                }
                // If there is rating but no comment
                else{
                    // Function to see if if they want to add a comment or not
                    const confirmAction = () => {
                    const response = confirm("Are you sure you don't want to add any additonal information?");
                    // If they don't want to capture a comment
                    if (response) {
                        // Capture rating logic here
                        create_rating(rating_number, email)
                        alert("Rating captured succesfully")
                    // If they do want to add a comment
                    } else {
                        alert("Rating cancelled.");
                    }
                    }
                    // Run the function
                    confirmAction()
                    
                }
            }
        }
        else{
            alert("Please enter an email to be rated.")
        }
    }
'''


# generic Flask app guard
if __name__ == '__main__':
    app.run(debug=True)
