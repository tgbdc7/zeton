# ZETON
Aplikacja wspomagająca terapię behawioralną. System żetonowy przeznaczony dla 
dziecka/ucznia. Pozwala na zdobywanie punktów za wykonywane czynności 
oraz wymienianie ich na nagrody.

## Cele aplikacji
- Rozwijanie zachowań deficytowych (pożądanych)
- Redukowanie zachowań niepożądanych
- Generalizowanie i utrzymywanie efektów terapii w czasie 



## Wymagania
- Python 3.6

## Uruchomienie:
- `pip install -r requirements.txt` - instalacja zależności
- `python recreate_db.py` - stworzenie tabeli w bazie
- `python run.py` - uruchomienie serwera


### Testowi użytkownicy:
- login: admin, password: admin
- login: testowy, password: testowy


### Triki (Linux)
- W przypadku serwera Flaskowego, który odłączył się od PyCharma i nie da się go wyłączyć:
    1. `netstat -tnlp` wypisuje wszystkie używane porty
    2. `fuser -k 5000/tcp` ubija proces działający na porcie `5000`
