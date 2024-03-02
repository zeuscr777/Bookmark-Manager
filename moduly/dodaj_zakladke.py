import tkinter as tk
from tkinter import Toplevel

def dodaj_zakladke(main_window, tree, drzewo_zakladek):
    def zapisz():
        # Dodawanie zakładki do głównego drzewa
        tree.insert('', 'end', values=(entry_nazwa.get(), entry_kategoria.get(), entry_url.get(), entry_przegladarka.get(), entry_opis.get(), "Otwórz", "Edytuj", "Usuń"))
        
        # Aktualizacja drzewka zakładek z symulowanym checkboxem
        aktualizuj_drzewo_zakladek(entry_nazwa.get(), entry_kategoria.get(), entry_url.get(), entry_przegladarka.get(), entry_opis.get(), drzewo_zakladek)

        okno_dodawania.destroy()
    
    okno_dodawania = Toplevel(main_window)
    okno_dodawania.title("Dodaj nową zakładkę")
    okno_dodawania.geometry("400x200")

    labels = ['Nazwa', 'Kategoria', 'URL', 'Przeglądarka', 'Opis']
    entries = []
    for i, label in enumerate(labels):
        tk.Label(okno_dodawania, text=label).grid(row=i, column=0)
        entry = tk.Entry(okno_dodawania)
        entry.grid(row=i, column=1)
        entries.append(entry)

    entry_nazwa, entry_kategoria, entry_url, entry_przegladarka, entry_opis = entries
    tk.Button(okno_dodawania, text="Zapisz", command=zapisz).grid(row=6, column=0, columnspan=2)

def aktualizuj_drzewo_zakladek(nazwa, kategoria, url, przeglądarka, opis, drzewo_zakladek):
    # Znajdź lub utwórz gałąź dla kategorii
    kategoria_id = None
    for child in drzewo_zakladek.get_children():
        if drzewo_zakladek.item(child)['text'] == kategoria:
            kategoria_id = child
            break
    if not kategoria_id:
        kategoria_id = drzewo_zakladek.insert('', 'end', text=kategoria)

    # Dodaj zakładkę jako dziecko kategorii z symulowanym checkboxem (domyślnie niezaznaczony '☐')
    zakladka_id = drzewo_zakladek.insert(kategoria_id, 'end', text=nazwa, values=('☐',))

    # Dodaj szczegóły zakładki jako dzieci zakładki
    drzewo_zakladek.insert(zakladka_id, 'end', text=f"URL: {url}")
    drzewo_zakladek.insert(zakladka_id, 'end', text=f"Przeglądarka: {przeglądarka}")
    drzewo_zakladek.insert(zakladka_id, 'end', text=f"Opis: {opis}")