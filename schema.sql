drop table if exists posts;
create table posts (
        id integer primary key autoincrement,
        author text not null,
        date date,
        title text not null,
        text text not null
        );

drop table if exists users;
create table users (
        id integer primary key autoincrement,
        nick text,
        name text,
        surname text,
        email text,
        password text,
        country text
        );

drop table if exists widgets;
create table widgets (
        id integer primary key autoincrement,
        position integer,
        body text
        );
