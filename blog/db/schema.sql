drop table if exists posts;
create table posts (
    id integer primary key autoincrement,
    title text not null,
    preview text not null,
    content text not null,
    created timestamp not null,
    archived integer
    );