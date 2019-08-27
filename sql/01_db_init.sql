PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS prizes;
DROP TABLE IF EXISTS home_points;
DROP TABLE IF EXISTS bans_name;
DROP TABLE IF EXISTS bans;
DROP TABLE IF EXISTS caregiver_to_child;
DROP TABLE IF EXISTS users;


create table users
(
  id                      integer UNIQUE primary key autoincrement,
  username                text UNIQUE not null,
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
  child_id         INTEGER not null,
  ban_id            INTEGER not null,
  start_timestamp text,
  end_timestamp   text,
  FOREIGN KEY (child_id) REFERENCES users (id)
);

create table bans_name
(
  id               INTEGER UNIQUE primary key autoincrement,
  child_id         INTEGER not null,
  ban_id           INTEGER not null,
  ban_name         text not null,
  FOREIGN KEY (child_id) REFERENCES users (id)
);

create table home_points
(
  id              INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
  user_id         INTEGER,
  name            TEXT NOT NULL,
  points          INTEGER NOT NULL,
  max_day         INTEGER NOT NULL,
  max_week        INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

create table prizes
(
  id              INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
  user_id         INTEGER,
  name            TEXT NOT NULL,
  points          INTEGER NOT NULL,
  max_day         INTEGER NOT NULL,
  max_week        INTEGER NOT NULL,
  max_month       INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
