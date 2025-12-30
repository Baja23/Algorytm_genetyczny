import random
from klasy import Przedmiot, Plecak

def inicjalizuj_przedmioty() -> list:
    przedmioty = []
    liczba_przedmiotow = int(input("Podaj liczbę przedmiotów: "))
    for i in range(liczba_przedmiotow):
        nazwa = f"Przedmiot_{i+1}"
        wybor = input('Czy chcesz podać wartość i wagę przedmiotu ręcznie? (t/n)').lower()
        if wybor == 't':
            print(f'Podaj wartość przedmiotu {nazwa}: ')
            wartosc = int(input())
            print(f'Podaj wagę przedmiotu {nazwa}: ')
            waga = int(input())
        else:
            wartosc = random.randint(5, 350)
            waga = random.randint(1, 40)
        przedmiot = Przedmiot(nazwa, wartosc, waga)
        przedmioty.append(przedmiot)
    return przedmioty

def poczatkowy_osobnik(losowe_przedmioty: list, plecak: object) -> object:
    for przedmiot in losowe_przedmioty:
        plecak.dodaj_przedmiot(przedmiot)
    return plecak

def stworz_populacje_startowa(rozmiar_populacji: int, przedmioty: list) -> list:
    populacja = []
    maksymalna_waga = int(input("Podaj maksymalną wagę plecaka: "))
    wybor = input('Czy chcesz wybrać ilość losowanych przedmiotów do plecaka? (t/n)').lower()
    if wybor == 't':
        k = int(input(f'Podaj ilość losowanych przedmiotów (maksymalna ilość to {len(przedmioty)}): '))
        k = min(k, len(przedmioty))
    else:
        k = random.randint(1, len(przedmioty))
    losowe_przedmioty = random.sample(przedmioty, k)
    for _ in range(rozmiar_populacji):
        plecak = Plecak(maksymalna_waga)
        osobnik = poczatkowy_osobnik(losowe_przedmioty, plecak)
        populacja.append(osobnik)
    return populacja

def funkcja_przystosowania(osobnik: object, ilosc_wszystkich_przedmiotow: int, max_wartosc_przedmiotu: int) -> float:
    #jak największa wartość przedmiotów w plecaku
    max_wartosc = ilosc_wszystkich_przedmiotow*max_wartosc_przedmiotu # Maksymalna możliwa wartość (50 przedmiotów po 350 każdy)
    wartosc_osobnika = osobnik.oblicz_calkowita_wartosc
    if osobnik.oblicz_calkowita_wage > osobnik.maksymalna_waga:
        return 0
    return (wartosc_osobnika / max_wartosc) * 100

def selekcja(populacja: list, ilosc_przedmiotow: int, max_wartosc_przedmiotu: int) -> list:
    #zsumować wszystkie wartości przystosowania
    wartosci_przystosowania = [funkcja_przystosowania(osobnik, ilosc_przedmiotow, max_wartosc_przedmiotu) for osobnik in populacja]
    suma_wartosci = sum(wartosci_przystosowania)
    if suma_wartosci == 0:
        # wszyscy mają 0 – wybieraj jednolicie losowo
        return random.choices(populacja, k=len(populacja))
    prawdopodobienstwa = [wartosc / suma_wartosci for wartosc in wartosci_przystosowania]
    wybrani_osobnicy = random.choices(populacja, weights=prawdopodobienstwa, k=len(populacja))
    return wybrani_osobnicy

#prawdopodobienstwo krzyzowania = 0,8
'''
    x wybranych osobników 
    podzielić osobników w pary
    dla każdej pary:
        wylosować liczbę z przedziału [0,1]
        jeśli liczba <= prawdopodobienstwo_krzyzowania:
            losujemy locus krzyżowania
            wykonać krzyżowanie (wymiana części przedmiotów między plecakami)
        inaczej:
            pozostawić parę bez zmian
'''

def krzyzowanie(osobnik1: object, osobnik2: object) -> tuple:
    prawdopodobienstwo_krzyzowania = 0.8
    if random.random() <= prawdopodobienstwo_krzyzowania: 
        locus = random.randint(1, min(len(osobnik1.dodane_przedmioty), len(osobnik2.dodane_przedmioty)) - 1)
        dziecko1_przedmioty = osobnik1.dodane_przedmioty[:locus] + osobnik2.dodane_przedmioty[locus:]
        dziecko2_przedmioty = osobnik2.dodane_przedmioty[:locus] + osobnik1.dodane_przedmioty[locus:]

        dziecko1 = Plecak(osobnik1.maksymalna_waga)
        for przedmiot in dziecko1_przedmioty:
            dziecko1.dodaj_przedmiot(przedmiot)

        dziecko2 = Plecak(osobnik2.maksymalna_waga)
        for przedmiot in dziecko2_przedmioty:
            dziecko2.dodaj_przedmiot(przedmiot)
        dziecka = [dziecko1, dziecko2]
        return dziecka
    else:
        return osobnik1, osobnik2
    
#prawdopodobienstwo_mutacji = 0,2
def mutacja(osobnik: object, przedmioty: list) -> object:
    prawdopodobienstwo_mutacji = 0.2
    if random.random() <= prawdopodobienstwo_mutacji:
        indeks_do_usuniecia = random.randint(0, len(osobnik.dodane_przedmioty) - 1)
        przedmiot_do_usuniecia = osobnik.dodane_przedmioty[indeks_do_usuniecia]
        osobnik.przedmioty.remove(przedmiot_do_usuniecia)
        przedmioty.remove(przedmiot_do_usuniecia)
        dostepne_przedmioty = [przedmiot for przedmiot in przedmioty if przedmiot not in osobnik.dodane_przedmioty]
        if dostepne_przedmioty:
            nowy_przedmiot = random.choice(dostepne_przedmioty)
            osobnik.dodaj_przedmiot(nowy_przedmiot)
    return osobnik

