class Przedmiot:
    def __init__(self, nazwa, wartosc, waga):
        self.nazwa = nazwa
        self.wartosc = wartosc
        self.waga = waga

class Plecak:
    def __init__(self, maksymalna_waga, funkcja_przystosowania=None):
        self.maksymalna_waga = maksymalna_waga
        self.przedmioty = []
        self.funkcja_przystosowania = funkcja_przystosowania
        
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
    





    '''
        osobnik1 -> plecak(20): przedmiot1, przedmiot2, ...
        osobnik2 -> plecak(20): przedmiot3, przedmiot4, ...
        osobnik_dziecko1 -> plecak(20): przedmiot1, przedmiot4, ...
        osobnik_dziecko2 -> plecak(20): przedmiot3, przedmiot2, ...

    '''