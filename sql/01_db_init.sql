PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS bans;
DROP TABLE IF EXISTS users;


create table users
(
  id                      integer primary key autoincrement,
  username                text not null,
  password                text not null,
  firstname               text,
  lastname                text,
  points                  integer default 0,
  school_weekly_highscore integer default 0
);

create table bans
(
  id              INTEGER primary key autoincrement,
  user_id         INTEGER,
  start_timestamp text,
  end_timestamp   text,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
