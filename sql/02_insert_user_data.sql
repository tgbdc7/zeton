BEGIN TRANSACTION;

INSERT INTO users VALUES(1,'opiekun1','pbkdf2:sha256:50000$Cg0Lvo4Z$8c2301855e36015cd9e40d5983431029641ee5f96f281eacb0b863f64c495a0e','caregiver','Antoni',NULL,0,0);
INSERT INTO users VALUES(2,'dziecko1','pbkdf2:sha256:50000$cnZ5hmIP$288b45f6adfaf99f1ce60560d44c8a34e2b73df87c6ed3e2f96f686a40d0a4cd','child','Bazyli',NULL,0,0);
INSERT INTO users VALUES(3,'dziecko2','pbkdf2:sha256:50000$F4RzVb3Z$e39c6ffd2f78f8a435c4b62c38d1d06be26d3fc4dd77d5d5ecd7e8156432eb3b','child','Celina',NULL,0,0);
INSERT INTO users VALUES(4,'opiekun2','pbkdf2:sha256:50000$UXPZgrr8$0981537e8e9d8c8fdbbd1672244d6fda81513bdcd432cc2f91606686d9775e86','caregiver','Dominika',NULL,0,0);
INSERT INTO users VALUES(5,'dziecko3','pbkdf2:sha256:50000$plsLYnx2$db59410c22b1e5a9bda5e1ee1a74a8f3ff219bb83e7f7ce2de00930006e9673c','child','Ewelina',NULL,0,0);
INSERT INTO users VALUES(6,'dziecko4','pbkdf2:sha256:50000$qYXjlGbk$ffbb4b0157f254d360dd80ebef8895462d3b569362e45108728be2c4672fcd0b','child','Filip',NULL,0,0);
INSERT INTO users VALUES(7,'dyrektor','pbkdf2:sha256:50000$uqVtNvPR$345a77790d4315661830b14f1545528a518722273952cc06c3a4b810454d24e8','caregiver','Zbigniew',NULL,0,0);

INSERT INTO caregiver_to_child VALUES(1,1,2);
INSERT INTO caregiver_to_child VALUES(2,1,3);
INSERT INTO caregiver_to_child VALUES(3,4,5);
INSERT INTO caregiver_to_child VALUES(4,4,6);
INSERT INTO caregiver_to_child VALUES(5,7,2);
INSERT INTO caregiver_to_child VALUES(6,7,3);
INSERT INTO caregiver_to_child VALUES(7,7,5);
INSERT INTO caregiver_to_child VALUES(8,7,6);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',7);
INSERT INTO sqlite_sequence VALUES('caregiver_to_child',8);
COMMIT;
