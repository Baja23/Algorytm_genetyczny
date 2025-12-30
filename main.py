from metody import stworz_populacje_startowa, inicjalizuj_przedmioty, selekcja, krzyzowanie, mutacja, funkcja_przystosowania
import random

def main():
    przedmioty = inicjalizuj_przedmioty()
    rozmiar_populacji = int(input("Podaj rozmiar populacji początkowej: "))
    populacja_startowa = stworz_populacje_startowa(rozmiar_populacji, przedmioty)
    wybrani_osobnicy = selekcja(populacja_startowa, len(przedmioty), max(przedmiot.wartosc for przedmiot in przedmioty))
    for generacja in range(10):  # Przykładowa liczba generacji
        nowa_populacja = []
        for i in range(0, len(wybrani_osobnicy), 2):
            if i + 1 < len(wybrani_osobnicy):
                dziecka = krzyzowanie(wybrani_osobnicy[i], wybrani_osobnicy[i + 1])
                dziecko1 = mutacja(dziecka[0], przedmioty)
                dziecko2 = mutacja(dziecka[1], przedmioty)
                nowa_populacja.append(dziecko1)
                nowa_populacja.append(dziecko2)
        wybrani_osobnicy = selekcja(nowa_populacja, len(przedmioty), max(przedmiot.wartosc for przedmiot in przedmioty))
    najlepszy_osobnik = max(wybrani_osobnicy, key=lambda osobnik: funkcja_przystosowania(osobnik, len(przedmioty), max(przedmiot.wartosc for przedmiot in przedmioty)))
    
    print(f"Najlepszy osobnik po ewolucji:\nPrzedmioty w plecaku: {najlepszy_osobnik.dodane_przedmioty}\nCałkowita wartość: {najlepszy_osobnik.oblicz_calkowita_wartosc}\nCałkowita waga: {najlepszy_osobnik.oblicz_calkowita_wage}")

if __name__ == "__main__":
    main()