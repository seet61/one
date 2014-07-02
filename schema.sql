drop table if exists tracks;
drop table if exists users;
create table tracks (
	id integer primary key autoincrement,
	artist text not null,
	title text not null
);
create table users (
	id integer primary key autoincrement,
	login text not null,
	password text not null
);