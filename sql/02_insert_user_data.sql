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

INSERT INTO bans_name VALUES(1,2,1,'1 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(2,2,2,'2 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(3,2,3,'KICK Przerwanie obecnej aktywności i udanie się do pokoju');
INSERT INTO bans_name VALUES(4,2,4,'BAN 2 stopnia na 30 min - brak komputera i telefonu');
INSERT INTO bans_name VALUES(5,2,5,'BAN 1 stopnia na 24h - brak telefonu');
INSERT INTO bans_name VALUES(6,2,6,'BAN 2 stopnia na 24h - brak komputera i telefonu');

INSERT INTO bans_name VALUES(7,3,1,'1 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(8,3,2,'2 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(9,3,3,'KICK Przerwanie obecnej aktywności i udanie się do pokoju');
INSERT INTO bans_name VALUES(10,3,4,'BAN 2 stopnia na 30 min - brak tableta i telefonu');
INSERT INTO bans_name VALUES(11,3,5,'BAN 1 stopnia na 24h - brak telefonu');
INSERT INTO bans_name VALUES(12,3,6,'BAN 2 stopnia na 24h - brak tableta i telefonu');

INSERT INTO bans_name VALUES(13,5,1,'1 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(14,5,2,'2 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(15,5,3,'KICK Przerwanie obecnej aktywności i udanie się do pokoju');
INSERT INTO bans_name VALUES(16,5,4,'BAN 2 stopnia na 30 min - brak telewizji i tableta');
INSERT INTO bans_name VALUES(17,5,5,'BAN 1 stopnia na 24h - brak tableta');
INSERT INTO bans_name VALUES(18,5,6,'BAN 2 stopnia na 24h - brak telewizji i tableta');

INSERT INTO bans_name VALUES(19,6,1,'1 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(20,6,2,'2 ustne ostrzeżenie');
INSERT INTO bans_name VALUES(21,6,3,'KICK Przerwanie obecnej aktywności i udanie się do pokoju');
INSERT INTO bans_name VALUES(22,6,4,'BAN 2 stopnia na 30 min - brak bajek i gier');
INSERT INTO bans_name VALUES(23,6,5,'BAN 1 stopnia na 24h - brak gier');
INSERT INTO bans_name VALUES(24,6,6,'BAN 2 stopnia na 24h - brak bajek i gier');

INSERT INTO home_points VALUES(1,2,"sprzątanie pokoju",20,1,7);
INSERT INTO home_points VALUES(2,2,"wykonanie polecenia bez zwłoki",20,1,7);
INSERT INTO home_points VALUES(3,2,"odrobienie lekcji",20,1,5);
INSERT INTO home_points VALUES(4,2,"spakowanie plecaka",20,1,5);
INSERT INTO home_points VALUES(5,2,"spakowanie plecaka z rodzicem",20,1,5);
INSERT INTO home_points VALUES(6,2,"pomoc rodzicom",10,3,35);
INSERT INTO home_points VALUES(7,2,"podlanie kwiatów",5,1,7);
INSERT INTO home_points VALUES(8,2,"pomoc ślepej sąsiadce",20,1,7);

INSERT INTO home_points VALUES(9,3,"granie na instrumencie",20,1,7);
INSERT INTO home_points VALUES(10,3,"wyprowadzanie psa",5,3,35);
INSERT INTO home_points VALUES(11,3,"sprawdzanie skrzynki na listy",20,1,7);

INSERT INTO home_points VALUES(12,5,"ścieranie kurzy",10,1,3);
INSERT INTO home_points VALUES(13,5,"czytanie książki",10,1,7);
INSERT INTO home_points VALUES(14,5,"trening na basenie",20,1,2);
INSERT INTO home_points VALUES(15,5,"mycie okien",100,1,1);

INSERT INTO home_points VALUES(16,6,"karmienie rybek",5,1,7);
INSERT INTO home_points VALUES(17,6,"naprawianie motocyklu - 20 min",20,1,2);
INSERT INTO home_points VALUES(18,6,"powrót do domu przed 20",10,1,7);

INSERT INTO prizes VALUES(1,2,"1 min komputer", 1, 30, 180, 720);
INSERT INTO prizes VALUES(2,2,"cola (200ml)", 20, 1, 1, 4);
INSERT INTO prizes VALUES(3,2,"zakupy w żabce (bez chipsów i Coca Coli)", 60, 1, 1, 4);
INSERT INTO prizes VALUES(4,2,"kino domowe", 100, 1, 2, 8);
INSERT INTO prizes VALUES(5,2,"piżama party", 100, 1, 2, 8);

INSERT INTO prizes VALUES(6,3, "6zł do wydania na mc.skyblock.pl", 200, 1, 1, 4);
INSERT INTO prizes VALUES(7,3, "jump city", 600, 1, 1, 3);
INSERT INTO prizes VALUES(8,3, "kino", 250, 1, 1, 2);

INSERT INTO prizes VALUES(9,5, "Aquapark reda", 250, 1, 1, 1);
INSERT INTO prizes VALUES(10,5, "piżama party", 250, 1, 1, 1);
INSERT INTO prizes VALUES(11,5, "kino domowe", 250, 1, 1, 1);

INSERT INTO prizes VALUES(12,6, "nowe części do motocykla", 600, 1, 1, 1);
INSERT INTO prizes VALUES(13,6, "nowa książka", 100, 1, 1, 4);
INSERT INTO prizes VALUES(14,6, "nowa rybka", 20, 1, 1, 1);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',7);
INSERT INTO sqlite_sequence VALUES('caregiver_to_child',8);
INSERT INTO sqlite_sequence VALUES('bans_name',24);
COMMIT;
