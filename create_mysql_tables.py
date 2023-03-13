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
    dbs = cur.execute('create table rating(rating_id int not null auto_increment,coach_id_fk int,coachee_id_fk int,rating int,rating_comment varchar(1000),coach_rated bool,coachee_rated bool,register_date DATETIME,primary key(rating_id));')
    dbs = cur.execute('Alter table rating add constraint coach_fk foreign key (coach_id_fk) references coach(coach_id);')
    dbs = cur.execute('Alter table rating add constraint coachee_fk foreign key (coachee_id_fk) references coachee(coachee_id);')
    print("==============> ALL TABLES CREATED SUCCESSFULLY <==============")
except:
    myconn.rollback()

myconn.close()