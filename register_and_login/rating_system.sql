create database rating;

use rating;
create table coach (
coach_id int not null auto_increment,
coach_name varchar(100) not null,
coach_password varchar(500) not null,
coach_avg_rating float,
register_date DATETIME,
primary key (coach_id)
);

create table coachee (
coachee_id int not null auto_increment,
coachee_name varchar(100) not null,
coachee_password varchar(500) not null,
coachee_avg_rating float,
register_date DATETIME,
primary key (coachee_id)
);

insert into coach (coach_name, coach_password, coach_avg_rating) values ('admin', 'admin', 5);

select coach_name, coach_password from coach where coach_name='admin';

drop table coach;
drop table coachee;

select * from coach;