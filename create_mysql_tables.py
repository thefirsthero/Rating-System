import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import pytz
from dotenv import load_dotenv

load_dotenv() # load environment variables form .env

#######################################################################################################
#######################################################################################################

# create database
myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'))

cur = myconn.cursor()

try:
    cur.execute("CREATE DATABASE rating_system")
except:
    myconn.rollback()

myconn.close()

#######################################################################################################
#######################################################################################################

myconn = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWD'), database=os.getenv('DATABASE'))

cur = myconn.cursor()

try:
    # create all tables
    dbs = cur.execute('create table coach (coach_id int not null auto_increment,coach_name varchar(100) not null,coach_surname varchar(100) not null,coach_password varchar(500) not null,user_type varchar(10),coach_email varchar(100) not null,coach_avg_rating float,register_date DATETIME,primary key (coach_id));')
    dbs = cur.execute('create table coachee (coachee_id int not null auto_increment,coachee_name varchar(100) not null,coachee_surname varchar(100) not null,coachee_password varchar(500) not null,user_type varchar(10),coachee_email varchar(100) not null,coachee_avg_rating float,register_date DATETIME,primary key (coachee_id));')
    dbs = cur.execute('create table rating(rating_id int not null auto_increment,coach_id_fk int,coachee_id_fk int,star_rating int,rating_comment varchar(1000),coach_rated bool,coachee_rated bool,register_date DATETIME,primary key(rating_id));')

    # add foreign key constraints to rating table
    dbs = cur.execute('Alter table rating add constraint coach_fk foreign key (coach_id_fk) references coach(coach_id);')
    dbs = cur.execute('Alter table rating add constraint coachee_fk foreign key (coachee_id_fk) references coachee(coachee_id);')

    # add triggers to compute and update average rating for coach/coachee from rated table entry
    dbs = cur.execute('CREATE TRIGGER compute_avg_coach_rating AFTER INSERT ON rating FOR EACH ROW UPDATE coach SET coach_avg_rating = (SELECT AVG(star_rating) FROM rating WHERE coach.coach_id = rating.coach_id_fk AND rating.coach_rated = True) WHERE coach_id = NEW.coach_id_fk;')
    dbs = cur.execute('CREATE TRIGGER compute_avg_coachee_rating AFTER INSERT ON rating FOR EACH ROW UPDATE coachee SET coachee_avg_rating = (SELECT AVG(star_rating) FROM rating WHERE coachee.coachee_id = rating.coachee_id_fk AND rating.coachee_rated = True)  WHERE coachee_id = NEW.coachee_id_fk;')

    print("==============> ALL TABLES CREATED SUCCESSFULLY <==============")
except:
    myconn.rollback()

myconn.close()
