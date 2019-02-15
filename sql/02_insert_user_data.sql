INSERT INTO users VALUES(1,'opiekun1','pbkdf2:sha256:50000$driFDCFh$2b3d2998f3a083ff48b8a9334a3fe2ff8cf248281acb7c7fc30ecc260053ab3e','caregiver','Antoni',NULL,0,0);
INSERT INTO users VALUES(2,'dziecko1','pbkdf2:sha256:50000$x0FWAFqi$a8295723351c54b0b4d5b5bc338ae866ffdcedd5ce6710d357420c50c54da333','child','Bazyli',NULL,0,0);
INSERT INTO users VALUES(3,'dziecko2','pbkdf2:sha256:50000$fhQHHTqh$1f3df7f8519216ea19474c38297e8deb760ea322c418647d52a773031fdf781e','child','Celina',NULL,0,0);
INSERT INTO users VALUES(4,'opiekun2','pbkdf2:sha256:50000$1Yf9UhMN$bfb831c43121c84a2312086319b8bb69e49530e291e9287823c04bf61cf1cedd','caregiver','Dominika',NULL,0,0);
INSERT INTO users VALUES(5,'dziecko3','pbkdf2:sha256:50000$VUyZoCMM$855136314caf1b99df5acde3cd3dcd970f8b0e8e60d072b8b48fcb466e85e62b','child','Ewelina',NULL,0,0);
INSERT INTO users VALUES(6,'dziecko4','pbkdf2:sha256:50000$A5rU4IHO$a4d54ca245043cac79a1d795cd58dc0389174e11f1368da12e2f2d665da02d6c','child','Filip',NULL,0,0);
INSERT INTO users VALUES(7,'dyrektor','pbkdf2:sha256:50000$Qh5wZlfl$4d158f38902fd7e322e3f8f09fcea69ad4f85265856a97b43b8711562603a718','caregiver','Zbigniew',NULL,0,0);


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
INSERT INTO sqlite_sequence VALUES('caregiver_to_child',10);
