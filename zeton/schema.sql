
drop table if exists punkty_uczniow;
create table punkty_uczniow (
    id_ucznia integer primary key autoincrement,
    suma_punktow integer not null,
    szkolny_rekord_tygodnia integer not null
);

drop table if exists uzytkownicy;
    create table uzytkownicy (
    id_uzytkownika integer primary key autoincrement,
    login text not null,
    haslo text not null
);