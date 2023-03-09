create database rating_system;

use rating_system;
create table coach (
coach_id int not null auto_increment,
coach_name varchar(100) not null,
coach_surname varchar(100) not null,
coach_password varchar(500) not null,
coach_email varchar(100) not null,
register_date DATETIME,
primary key (coach_id)
);

create table coachee (
coachee_id int not null auto_increment,
coachee_name varchar(100) not null,
coachee_surname varchar(100) not null,
coachee_password varchar(500) not null,
coachee_email varchar(100) not null,
register_date DATETIME,
primary key (coachee_id)
);


# NB: Only create the table 'rating' after you have inserted dummy data
# into the 'coach' and 'coachee' tables.

# FYI:
# You can't add a NOT NULL column to a table 
# that has more than zero rows, 
# when the column is constrained to values that match those in the parent table,
# and yet has only NULL values because it's a new, unpopulated column with no DEFAULT.

create table rating(
rating_id int not null auto_increment,
foreign key(coach_id) references coach(coach_id),
foreign key(coachee_id) references coachee(coachee_id),
avg_rating float not null,
coach_rated bool
);

