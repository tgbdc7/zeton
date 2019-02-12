# ZETON

Python 3.6

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
