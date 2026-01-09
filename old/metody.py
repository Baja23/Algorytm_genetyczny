import random
from old.klasy import Przedmiot, Plecak

def inicjalizuj_przedmioty(maksymalna_waga: float) -> list:
    przedmioty = []
    liczba_przedmiotow = int(input("Podaj liczbę przedmiotów: "))
    for i in range(liczba_przedmiotow):
            nazwa = f'Przedmiot{i+1}'
            wartosc = float(input(f'Podaj wartość przedmiotu {nazwa}: '))
            while True: 
                waga = float(input(f'Podaj wagę przedmiotu {nazwa}: '))
                if waga <= maksymalna_waga:
                    break
            przedmiot = Przedmiot(nazwa, wartosc, waga)
            przedmioty.append(przedmiot)
    return przedmioty

def poczatkowy_osobnik(losowe_przedmioty: list, plecak: object) -> object:
    for przedmiot in losowe_przedmioty:
        plecak.dodaj_przedmiot(przedmiot)
    return plecak

def stworz_populacje_startowa(rozmiar_populacji: int, przedmioty: list, maksymalna_waga: float) -> list:
    populacja = []
    for _ in range(rozmiar_populacji):
        while True:
            plecak = Plecak(maksymalna_waga)
            k = random.randint(2, len(przedmioty))
            losowe_przedmioty = random.sample(przedmioty, k)
            osobnik = poczatkowy_osobnik(losowe_przedmioty, plecak)
            if osobnik.oblicz_calkowita_wage <= maksymalna_waga: 
                break
            
        populacja.append(osobnik)
    return populacja

def funkcja_przystosowania(osobnik: object, ilosc_wszystkich_przedmiotow: int, max_wartosc_przedmiotu: int) -> float:
    #jak największa wartość przedmiotów w plecaku
    max_wartosc = ilosc_wszystkich_przedmiotow*max_wartosc_przedmiotu # Maksymalna możliwa wartość (50 przedmiotów po 350 każdy)
    wartosc_osobnika = osobnik.oblicz_calkowita_wartosc
    if osobnik.oblicz_calkowita_wage > osobnik.maksymalna_waga:
        osobnik.wartosc_funkcji_przystosowania = 0
    else: 
        osobnik.wartosc_funkcji_przystosowania = (wartosc_osobnika / max_wartosc) * 100
    return osobnik.wartosc_funkcji_przystosowania

def selekcja(populacja: list, ilosc_przedmiotow: int, max_wartosc_przedmiotu: int) -> list:
    #zsumować wszystkie wartości przystosowania
    wartosci_przystosowania = [funkcja_przystosowania(osobnik, ilosc_przedmiotow, max_wartosc_przedmiotu) for osobnik in populacja]
    suma_wartosci = sum(wartosci_przystosowania)
    if suma_wartosci == 0:
        return []
    prawdopodobienstwa = [wartosc / suma_wartosci for wartosc in wartosci_przystosowania]
    wybrani_osobnicy = random.choices(populacja, weights=prawdopodobienstwa, k=len(populacja))
    return wybrani_osobnicy

#prawdopodobienstwo krzyzowania = 0,8
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
        przedmioty_lokalnie = [przedmiot for przedmiot in przedmioty]
        przedmioty_lokalnie.remove(przedmiot_do_usuniecia)
        dostepne_przedmioty = [przedmiot for przedmiot in przedmioty if przedmiot not in osobnik.dodane_przedmioty]
        if dostepne_przedmioty:
            nowy_przedmiot = random.choice(dostepne_przedmioty)
            osobnik.dodaj_przedmiot(nowy_przedmiot)
    return osobnik

