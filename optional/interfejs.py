import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from klasa import Przedmiot
# Importujemy zdefiniowaną klasę Przedmiot

class InterfejsPlecakowy:
    """Klasa obsługująca interfejs Tkinter z mechanizmem blokady pojemności."""
    
    # Przechowujemy pojemność jako atrybut instancji, początkowo None
    pojemnosc_plecaka: Optional[float] = None 

    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Algorytm Genetyczny: Problem Plecakowy")
        
        self.przedmioty: List[Przedmiot] = []
        
        self._utworz_widzety()
        self._rozmiesc_widzety()
        
        # Inicjalne ustawienie: pola przedmiotów są nieaktywne, dopóki pojemność nie zostanie ustawiona
        self._ustaw_stan_interfejsu(pojemnosc_ustawiona=False)

    # --- Architektura Interfejsu (Tkinter) ---

    def _utworz_widzety(self):
        # Sekcja Pojemności
        self.ramka_pojemnosc = ttk.LabelFrame(self.master, text="1. Ustal Pojemność Plecaka")
        self.etykieta_pojemnosc = ttk.Label(self.ramka_pojemnosc, text="Maksymalna Waga Plecaka:")
        self.pole_pojemnosc = ttk.Entry(self.ramka_pojemnosc)
        self.przycisk_ustaw_pojemnosc = ttk.Button(self.ramka_pojemnosc, 
                                                   text="Ustaw i Zablokuj", 
                                                   command=self._ustaw_pojemnosc)
        
        # Sekcja Przedmiotów (Zablokowana na początku)
        self.ramka_wprowadzania = ttk.LabelFrame(self.master, text="2. Wprowadź Przedmiot (Blokada do momentu ustalenia pojemności)")
        self.etykieta_nazwa = ttk.Label(self.ramka_wprowadzania, text="Nazwa:")
        self.pole_nazwa = ttk.Entry(self.ramka_wprowadzania)
        self.etykieta_wartosc = ttk.Label(self.ramka_wprowadzania, text="Wartość (float):")
        self.pole_wartosc = ttk.Entry(self.ramka_wprowadzania)
        self.etykieta_waga = ttk.Label(self.ramka_wprowadzania, text="Waga (float):")
        self.pole_waga = ttk.Entry(self.ramka_wprowadzania)
        
        # Przyciski Sterujące
        self.przycisk_dodaj = ttk.Button(self.master, 
                                          text="Kolejny Przedmiot (Dodaj)", 
                                          command=self._dodaj_przedmiot)
        self.przycisk_koniec = ttk.Button(self.master, 
                                           text="Koniec Wprowadzania", 
                                           command=self._koniec_wprowadzania)

    def _rozmiesc_widzety(self):
        # Sekcja Pojemności
        self.ramka_pojemnosc.pack(padx=10, pady=10, fill="x")
        self.etykieta_pojemnosc.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pole_pojemnosc.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.przycisk_ustaw_pojemnosc.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ramka_pojemnosc.columnconfigure(1, weight=1) 
        
        # Sekcja Przedmiotów
        self.ramka_wprowadzania.pack(padx=10, pady=10, fill="x")
        pola = [
            (self.etykieta_nazwa, self.pole_nazwa),
            (self.etykieta_wartosc, self.pole_wartosc),
            (self.etykieta_waga, self.pole_waga),
        ]
        for i, (etykieta, pole) in enumerate(pola):
            etykieta.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            pole.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        self.ramka_wprowadzania.columnconfigure(1, weight=1) 
        
        # Przyciski
        self.przycisk_dodaj.pack(fill="x", padx=10, pady=(0, 5))
        self.przycisk_koniec.pack(fill="x", padx=10, pady=(0, 10))
        
    def _ustaw_stan_interfejsu(self, pojemnosc_ustawiona: bool):
        """
        Ustawia stan aktywności pól formularza dla przedmiotów oraz przycisków.
        
        Args:
            pojemnosc_ustawiona (bool): True jeśli pojemność została już zdefiniowana.
        """
        stan = 'normal' if pojemnosc_ustawiona else 'disabled'
        stan_pojemnosci = 'disabled' if pojemnosc_ustawiona else 'normal'

        # Zablokowanie/Odblokowanie pól przedmiotów
        for pole in [self.pole_nazwa, self.pole_wartosc, self.pole_waga]:
            pole.config(state=stan)
        
        # Zablokowanie przycisków
        self.przycisk_dodaj.config(state=stan)
        self.przycisk_koniec.config(state=stan)

        # Blokada/Odblokowanie sekcji pojemności
        self.pole_pojemnosc.config(state=stan_pojemnosci)
        self.przycisk_ustaw_pojemnosc.config(state=stan_pojemnosci)
        
        # Zmiana tytułu ramki przedmiotów
        if pojemnosc_ustawiona:
            self.ramka_wprowadzania.config(text="2. Wprowadź Przedmiot")
            self.pole_nazwa.focus_set() # Ustawienie fokusu na pierwszym polu dla wygody
        else:
            self.ramka_wprowadzania.config(text="2. Wprowadź Przedmiot (Najpierw ustal pojemność!)")
            self.pole_pojemnosc.focus_set()

    # --- Logika Biznesowa (Walidacja/Ustawianie) ---
    
    def _ustaw_pojemnosc(self):
        """
        Waliduje i ustawia maksymalną pojemność plecaka, a następnie blokuje pole.
        """
        pojemnosc_str = self.pole_pojemnosc.get().strip()
            
        try:
            pojemnosc = float(pojemnosc_str)
            if pojemnosc <= 0:
                raise ValueError("Pojemność musi być dodatnią liczbą.")
                
            self.pojemnosc_plecaka = pojemnosc
            messagebox.showinfo("Ustawiono", f"Pojemność plecaka została ustawiona na {pojemnosc} i zablokowana.")
            
            # --- KLUCZOWA ZMIANA STANU ---
            self._ustaw_stan_interfejsu(pojemnosc_ustawiona=True)
            
        except ValueError as e:
            messagebox.showerror("Błąd Ustawień", f"Nieprawidłowa pojemność: {e}")

    def _dodaj_przedmiot(self):
        """Pobiera dane i tworzy nowy obiekt Przedmiot (możliwe tylko po ustawieniu pojemności)."""
        # Sprawdzanie, czy pojemność została już ustawiona (choć interfejs już to blokuje, 
        # jest to dobra praktyka w logice biznesowej - obrona głęboka)
        if self.pojemnosc_plecaka is None:
            messagebox.showerror("Błąd", "Najpierw musisz ustawić i zablokować pojemność plecaka.")
            return

        nazwa = self.pole_nazwa.get().strip()
        wartosc_str = self.pole_wartosc.get().strip()
        waga_str = self.pole_waga.get().strip()

        try:
            wartosc = float(wartosc_str)
            waga = float(waga_str)
            
            nowy_przedmiot = Przedmiot(nazwa=nazwa, wartosc=wartosc, waga=waga)
            
        except ValueError as e:
            messagebox.showerror("Błąd Walidacji Danych", f"Nieprawidłowe dane: {e}")
            return
        
        # Dodajemy przedmiot (kontynuacja)
        self.przedmioty.append(nowy_przedmiot)
        messagebox.showinfo("Dodano", f"Przedmiot '{nazwa}' dodany. Zebrano już {len(self.przedmioty)} przedmiotów.")
        
        # Czyszczenie pól
        self.pole_nazwa.delete(0, tk.END)
        self.pole_wartosc.delete(0, tk.END)
        self.pole_waga.delete(0, tk.END)
        self.pole_nazwa.focus_set()

    def _koniec_wprowadzania(self):
        """Obsługuje zakończenie wprowadzania danych."""
        if self.pojemnosc_plecaka is None:
            messagebox.showerror("Błąd", "Nie można zakończyć. Musisz ustawić pojemność.")
            return

        if not self.przedmioty:
            if not messagebox.askyesno("Ostrzeżenie", 
                                       "Nie dodano żadnych przedmiotów. Czy na pewno chcesz zakończyć?"):
                return
        
        print("\n--- Zakończenie Wprowadzania Danych ---")
        print(f"Maksymalna Waga Plecaka: {self.pojemnosc_plecaka}")
        print(f"Liczba przedmiotów: {len(self.przedmioty)}")
        
        self.master.quit()
        
    def uruchom(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfejsPlecakowy(root)
    app.uruchom()