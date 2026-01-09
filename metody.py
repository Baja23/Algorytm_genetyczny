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

def poczatkowy_osobnik(losowe_przedmioty: list, plecak: object) -> dict:
    for przedmiot in losowe_przedmioty:
        plecak.dodaj_przedmiot(przedmiot)
        losowe_przedmioty = losowe_przedmioty-przedmiot
    return plecak

def stworz_populacje_startowa(rozmiar_populacji: int, przedmioty: list, maksymalna_waga: float) -> list:
    populacja = []
    for _ in range(rozmiar_populacji):
        while True:
            plecak = Plecak(maksymalna_waga, przedmioty)
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
    return (wartosc_osobnika / max_wartosc) * 100

def selekcja(populacja: list, ilosc_przedmiotow: int, max_wartosc_przedmiotu: int) -> list:
    #zsumować wszystkie wartości przystosowania
    wartosci_przystosowania = [funkcja_przystosowania(osobnik, ilosc_przedmiotow, max_wartosc_przedmiotu) for osobnik in populacja]
    suma_wartosci = sum(wartosci_przystosowania)
    prawdopodobienstwa = [wartosc / suma_wartosci for wartosc in wartosci_przystosowania]
    wybrani_osobnicy = random.choices(populacja, weights=prawdopodobienstwa, k=len(populacja))
    return wybrani_osobnicy

#prawdopodobienstwo krzyzowania = 0,8
def krzyzowanie(osobnik1: object, osobnik2: object) -> tuple:
    prawdopodobienstwo_krzyzowania = 0.8
    if random.random() <= prawdopodobienstwo_krzyzowania: 
        wszystkie_przedmioty = osobnik1.wszystkie_przedmioty 
        dlugosc_genotypu = len(wszystkie_przedmioty)

        if dlugosc_genotypu < 2:
             return osobnik1, osobnik2

        locus = random.randint(1, dlugosc_genotypu - 1)

        gen1 = list(osobnik1.osobnik.values())
        gen2 = list(osobnik2.osobnik.values())

        dziecko1_genotyp = gen1[:locus] + gen2[locus:]
        dziecko2_genotyp = gen2[:locus] + gen1[locus:]

        dziecko1 = Plecak(osobnik1.maksymalna_waga, wszystkie_przedmioty)
        for i, bit in enumerate(dziecko1_genotyp):
            if bit == 1:
                przedmiot = wszystkie_przedmioty[i]
                dziecko1.dodaj_przedmiot(przedmiot)

        dziecko2 = Plecak(osobnik2.maksymalna_waga, wszystkie_przedmioty)
        for i, bit in enumerate(dziecko2_genotyp):
            if bit == 1:
                przedmiot = wszystkie_przedmioty[i]
                dziecko2.dodaj_przedmiot(przedmiot)
        
        dziecka = [dziecko1, dziecko2]
        return dziecka
    else:
        return osobnik1, osobnik2
    
#prawdopodobienstwo_mutacji = 0,2
def mutacja(osobnik: object, przedmioty: list) -> object:
    prawdopodobienstwo_mutacji = 0.2
    if random.random() <= prawdopodobienstwo_mutacji:
        indeks_do_zmiany = random.randint(0, len(przedmioty) - 1)
        if osobnik.wszystkie_przedmioty[indeks_do_zmiany] not in osobnik.dodane_przedmioty:
            osobnik.dodaj_przedmiot(osobnik.wszystkie_przedmioty[indeks_do_zmiany])
        else: 
            osobnik.dodane_przedmioty.remove(osobnik.wszystkie_przedmioty[indeks_do_zmiany])
    return osobnik