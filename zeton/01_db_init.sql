PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;


create table users
(
  id       integer primary key autoincrement,
  username text not null,
  password text not null
);

DROP TABLE IF EXISTS points_;

create table points_
(
  id                   INTEGER primary key,
  points               INTEGER NOT NULL,
  school_weekly_record integer not null,
  FOREIGN KEY (id) REFERENCES users (id)
);

-- TODO: punkty powinny być przechowywane w tabeli "users", natomiast bany powinny mieć oddzielną tabelę
