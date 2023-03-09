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


create table rating(
rating_id int not null auto_increment,
coach_id_fk int,
coachee_id_fk int,
avg_rating float not null,
coach_rated bool,
primary key(rating_id)
);

# add coach_id as foreign key to rating table
Alter table rating
add constraint coach_fk
foreign key (coach_id_fk)
references coach(coach_id);

# add coachee_id as foreign key to rating table
Alter table rating
add constraint coachee_fk
foreign key (coachee_id_fk)
references coachee(coachee_id);
