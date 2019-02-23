PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS bans;
DROP TABLE IF EXISTS caregiver_to_child;
DROP TABLE IF EXISTS users;


create table users
(
  id                      integer UNIQUE primary key autoincrement,
  username                text not null,
  password                text not null,
  role                    text not NULL check ( role in ('caregiver', 'child') ),
  firstname               text,
  lastname                text,
  points                  integer default 0,
  school_weekly_highscore integer default 0
);

create table caregiver_to_child
(
  id           INTEGER UNIQUE primary key autoincrement,
  caregiver_id INTEGER,
  child_id     INTEGER,
  FOREIGN KEY (caregiver_id) REFERENCES users (id),
  FOREIGN KEY (child_id) REFERENCES users (id)
);

create table bans
(
  id              INTEGER UNIQUE primary key autoincrement,
  user_id         INTEGER,
  start_timestamp text,
  end_timestamp   text,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
