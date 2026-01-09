class Przedmiot:
    def __init__(self, nazwa, wartosc, waga):
        self.nazwa = nazwa
        self.wartosc = wartosc
        self.waga = waga

    def __repr__(self):
        # Ta metoda mówi Pythonowi, co ma pokazać, gdy obiekt jest w liście
        return f"{self.nazwa}(w:{self.wartosc}, kg:{self.waga})"

class Plecak:
    def __init__(self, maksymalna_waga, wartosc_funkcji_przystosowania=None):
        self.maksymalna_waga = maksymalna_waga
        self.przedmioty = []
        self.wartosc_funkcji_przystosowania = wartosc_funkcji_przystosowania
        
    def dodaj_przedmiot(self, przedmiot):
        self.przedmioty.append(przedmiot)

    @property
    def dodane_przedmioty(self):
        return self.przedmioty
    @property
    def oblicz_calkowita_wage(self):
        return sum(przedmiot.waga for przedmiot in self.przedmioty)
    @property
    def oblicz_calkowita_wartosc(self):
        return sum(przedmiot.wartosc for przedmiot in self.przedmioty)