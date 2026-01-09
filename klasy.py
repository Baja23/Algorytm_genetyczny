class Przedmiot:
    def __init__(self, nazwa, wartosc, waga):
        self.nazwa = nazwa
        self.wartosc = wartosc
        self.waga = waga

    def __repr__(self):
        # Ta metoda mówi Pythonowi, co ma pokazać, gdy obiekt jest w liście
        return f"{self.nazwa}(w:{self.wartosc}, kg:{self.waga})"

class Plecak:
    def __init__(self, maksymalna_waga: float, wszystkie_przedmioty: list, genotyp: list = None):
        self.maksymalna_waga = maksymalna_waga
        self.przedmioty = []
        self.wszystkie_przedmioty = wszystkie_przedmioty
        if genotyp is None:
            self.genotyp = [0] * len(wszystkie_przedmioty)
        else: 
            self.genotyp = genotyp

    def dodaj_przedmiot(self, nazwa):
        index = self.wszystkie_przedmioty.index(nazwa)
        self.genotyp[index] = self.genotyp[index] ^ 1
        self.przedmioty.append(nazwa)

    @property
    def dodane_przedmioty(self):
        return self.przedmioty
    @property
    def oblicz_calkowita_wage(self):
        return sum(p.waga for p in self.przedmioty)
    @property
    def oblicz_calkowita_wartosc(self):
        return sum(p.wartosc for p in self.przedmioty)