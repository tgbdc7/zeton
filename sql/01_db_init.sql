PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS home_points;
DROP TABLE IF EXISTS prizes;
DROP TABLE IF EXISTS points_history;
DROP TABLE IF EXISTS bans_name;
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
  last_insert_id          integer default 0,
  last_insert_firstname   text default null,
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

create table points_history
(
  id                        INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
  child_id                  INTEGER NOT NULL,
  points_change             INTEGER NOT NULL,
  id_changing_user          INTEGER NOT NULL,
  points_name               TEXT NOT NULL DEFAULT 'points_name',
  change_timestamp          TEXT NOT NULL,
  firstname_changing_user   TEXT,
  FOREIGN KEY (child_id) REFERENCES users (id),
  FOREIGN KEY (id_changing_user) REFERENCES users (id),
  FOREIGN KEY (firstname_changing_user) REFERENCES users (last_insert_firstname)
);

CREATE TRIGGER points_log  AFTER UPDATE ON users for each row when new.points <> old.points
    begin
        INSERT INTO points_history  (child_id,points_change, id_changing_user, change_timestamp, firstname_changing_user)
        VALUES ( new.id, new.points - old.points, new.last_insert_id, CURRENT_TIMESTAMP, new.last_insert_firstname);
    END;