import time


def odliczaj_czas_warna(t):
    """
    Funkcja odliczajaca czas warna (minuty:sekundy)
    Dziala, ale nie dodalam jeszcze przekazania liczby sekund do funkcji
    """
    while t:
        minuty, sekundy = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(minuty, sekundy)
        print(timeformat, end="\r")
        time.sleep(1)
        t -= 1
    print("Koniec warna")
