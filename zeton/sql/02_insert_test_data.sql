INSERT INTO users VALUES(1,'admin','pbkdf2:sha256:50000$hYByObtL$ac5c33398f809197e4b7ebb42e256993fdddf048ab2a029ae87f6b1c96d606b0','Admin',NULL,0,0);

INSERT INTO users VALUES(2,'testowy','pbkdf2:sha256:50000$NGYfLYhY$6b57387f50ec496d0942f07dd4e19b173c56e43317ba4abfd4283cf61cf8d8ed','Testowy',NULL,0,0);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',2);
