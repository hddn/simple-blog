drop table if exists posts;
create table posts (
    id integer primary key autoincrement,
    title text not null,
    content text not null,
    created text not null
    );