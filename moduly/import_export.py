import json
import tkinter as tk
from tkinter import filedialog
from moduly.dodaj_zakladke import aktualizuj_drzewo_zakladek


def importuj(tree, drzewo_zakladek):
    plik_nazwa = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if plik_nazwa:
        with open(plik_nazwa, 'r', encoding='utf-8') as plik:
            zakladki_lista = json.load(plik)
            for zakladka in zakladki_lista:
                # Dodanie zakładek do drzewa w GUI
                tree.insert('', 'end', values=(zakladka["Nazwa"], zakladka["Kategoria"], zakladka["URL"], zakladka["Przeglądarka"], zakladka["Opis"], "Otwórz", "Edytuj","Usuń"))
                # Aktualizacja drzewka zakładek
                aktualizuj_drzewo_zakladek(zakladka["Nazwa"], zakladka["Kategoria"], zakladka["URL"], zakladka["Przeglądarka"], zakladka["Opis"], drzewo_zakladek)

def eksportuj(tree):
    zakladki_lista = []
    for zakladka in tree.get_children():
        zakladka_info = tree.item(zakladka)['values']
        zakladki_lista.append({
            "Nazwa": zakladka_info[0],
            "Kategoria": zakladka_info[1],
            "URL": zakladka_info[2],
            "Przeglądarka": zakladka_info[3],
            "Opis": zakladka_info[4]
        })

    # Umożliwienie użytkownikowi wybrania lokalizacji zapisu pliku
    plik_nazwa = filedialog.asksaveasfilename(defaultextension=".json",
                                              filetypes=[("JSON files", "*.json")])
    if plik_nazwa:
        with open(plik_nazwa, 'w', encoding='utf-8') as plik:
            json.dump(zakladki_lista, plik, ensure_ascii=False, indent=4)
