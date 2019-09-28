BEGIN TRANSACTION;

INSERT INTO users
VALUES (1,
        'caregiver_login',
        'pbkdf2:sha256:150000$3YLzOKDd$2e1d50b8fc485efa0ee45fb20d15158712aab90538d3577e31b3dadf0fa0cf7d',
        'caregiver',
        'Pafnucy',
        NULL);
INSERT INTO users
VALUES (2,
        'child_login',
        'pbkdf2:sha256:150000$nbHPlxsT$5cad215cd4d5f0a5da6af2ebf3df8102decfe8e34fb0c651a34c69819e2e7cb5',
        'child',
        'Bonifacy',
        NULL);


INSERT INTO main_points
VALUES(1,
       2,
       0,
       0,
       0,
       0);

INSERT INTO caregiver_to_child
VALUES (1, 1, 2);

INSERT INTO bans_name
VALUES (1, 2, 1, '1 ustne ostrzeżenie');
INSERT INTO bans_name
VALUES (2, 2, 2, '2 ustne ostrzeżenie');
INSERT INTO bans_name
VALUES (3, 2, 3, 'KICK Przerwanie obecnej aktywności i udanie się do pokoju');
INSERT INTO bans_name
VALUES (4, 2, 4, 'BAN 2 stopnia na 30 min - brak komputera i telefonu');
INSERT INTO bans_name
VALUES (5, 2, 5, 'BAN 1 stopnia na 24h - brak telefonu');
INSERT INTO bans_name
VALUES (6, 2, 6, 'BAN 2 stopnia na 24h - brak komputera i telefonu');

INSERT INTO home_points
VALUES (1, 2, 'sprzątanie pokoju', 20, 1, 7, 1);
INSERT INTO home_points
VALUES (2, 2, 'wykonanie polecenia bez zwłoki', 20, 1, 7, 0);
INSERT INTO home_points
VALUES (3, 2, 'odrobienie lekcji', 20, 1, 5, 1);
INSERT INTO home_points
VALUES (4, 2, 'spakowanie plecaka', 20, 1, 5, 1);
INSERT INTO home_points
VALUES (5, 2, 'spakowanie plecaka z rodzicem', 20, 1, 5, 1);
INSERT INTO home_points
VALUES (6, 2, 'pomoc rodzicom', 10, 3, 35 ,0);
INSERT INTO home_points
VALUES (7, 2, 'podlanie kwiatów', 5, 1, 7, 1);
INSERT INTO home_points
VALUES (8, 2, 'pomoc ślepej sąsiadce', 20, 1, 7, 0);

INSERT INTO prizes
VALUES (1, 2, '1 min komputer', 1, 30, 180, 720);
INSERT INTO prizes
VALUES (2, 2, 'cola (200ml)', 20, 1, 1, 4);
INSERT INTO prizes
VALUES (3, 2, 'zakupy w żabce (bez chipsów i Coca Coli)', 60, 1, 1, 4);
INSERT INTO prizes
VALUES (4, 2, 'kino domowe', 100, 1, 2, 8);
INSERT INTO prizes
VALUES (5, 2, 'piżama party', 100, 1, 2, 8);

CREATE TRIGGER add_new_child_main_points  AFTER INSERT ON users for each row when new.role = 'child'
    begin
        INSERT INTO main_points  (child_id)
        VALUES ( new.id);
    END;


COMMIT;
