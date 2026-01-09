from old.metody import stworz_populacje_startowa, inicjalizuj_przedmioty, selekcja, krzyzowanie, mutacja, funkcja_przystosowania
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    maksymalna_waga = float(input("Podaj maksymalną wagę plecaka: "))
    przedmioty = inicjalizuj_przedmioty(maksymalna_waga)
    rozmiar_populacji = int(input("Podaj rozmiar populacji początkowej: "))
    populacja_startowa = stworz_populacje_startowa(rozmiar_populacji, przedmioty, maksymalna_waga)
    wybrani_osobnicy = selekcja(populacja_startowa, len(przedmioty), max(przedmiot.wartosc for przedmiot in przedmioty))
    data_for_visualization = []
    counter = 0
    for generacja in range(20):  # Przykładowa liczba generacji
        counter =+1
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
        data_for_visualization.append(najlepszy_osobnik)
        print(f'Przedmioty w plecaku w generacji{generacja}: {najlepszy_osobnik.dodane_przedmioty}\n')
    print(f'Najlepszy osobnik po ewolucji:\nPrzedmioty w plecaku: {najlepszy_osobnik.dodane_przedmioty}\n')

    #wizualizacja
    wartosci_y = [osobnik.oblicz_calkowita_wartosc for osobnik in data_for_visualization]
    generacje_x = range(len(data_for_visualization))

    plt.figure(figsize=(10, 6)) 
    sns.lineplot(x=generacje_x, y=wartosci_y, marker='o')
    plt.title("Postęp algorytmu genetycznego")
    plt.xlabel("Numer generacji")
    plt.ylabel("Wartość najlepszego plecaka")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
          
'''Całkowita wartość: {najlepszy_osobnik.oblicz_calkowita_wartosc}\nCałkowita waga: {najlepszy_osobnik.oblicz_calkowita_wage}'''