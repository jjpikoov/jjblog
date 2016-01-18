drop table if exists posts;
create table posts (
        id integer primary key autoincrement,
        date text not null,
        title text not null,
        text text not null
        );

drop table if exists widgets;
create table widgets (
        id integer primary key autoincrement,
        name text,
        body text
        );
