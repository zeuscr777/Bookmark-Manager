import tkinter as tk
from tkinter import Menu, ttk
from moduly.dodaj_zakladke import dodaj_zakladke
from moduly.import_export import importuj, eksportuj
from moduly.ustawienia import zmien_motyw, zmien_jezyk
from moduly.o_autorze import o_autorze
from moduly.wczytaj_teksty import wczytaj_teksty
from moduly.new import newProject
import webbrowser

# Ustawienie ścieżki do przeglądarki Google Chrome
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# Uzyskanie dostępu do przeglądarki Google Chrome
chrome_browser = webbrowser.get(chrome_path)

def reload_texts(jezyk):
    global teksty
    try:
        with open(path_to_language_file, "r", encoding="utf-8") as file:
            teksty = json.load(file)
            
            # Aktualizacja tekstów w menu
            menu_plik.entryconfig(0, label=teksty["menu"]["import"])
            menu_plik.entryconfig(1, label=teksty["menu"]["export"])
            menu_plik.entryconfig(2, label=teksty["menu"]["new"])
            menu_ustawienia.entryconfig(0, label=teksty["menu"]["change_theme"])
            menu_ustawienia.entryconfig(1, label=teksty["menu"]["change_language"])
            menu_program.entryconfig(0, label=teksty["menu"]["about"])

            # Aktualizacja przycisku dodawania zakładki
            przycisk_dodaj.config(text=teksty["buttons"]["add_bookmark"])

            # Aktualizacja tytułu okna
            okno.title(teksty["window_titles"]["main_window"])
    except Exception as e:
        print(f"Błąd wczytywania pliku językowego: {e}")
    teksty = wczytaj_teksty(jezyk)
    okno.title(teksty["window_titles"]["main_window"])

# Wczytanie tekstów językowych
teksty = wczytaj_teksty("pl")

# Utworzenie głównego okna
okno = tk.Tk()
okno.title(teksty["window_titles"]["main_window"])
okno.geometry("800x600")

# Utworzenie ramki dla drzewa zakładek po lewej stronie
ramka_drzewa = tk.Frame(okno, width=200)
ramka_drzewa.pack(side=tk.LEFT, fill=tk.Y)

# Tworzenie i konfiguracja drzewa zakładek z dodatkową kolumną dla checkboxów
drzewo_zakladek = ttk.Treeview(ramka_drzewa, show='tree')
drzewo_zakladek.pack(fill=tk.BOTH, expand=True)

# Utworzenie menu głównego
menu_glowne = Menu(okno)
okno.config(menu=menu_glowne)

# Dodanie zakładek menu
menu_plik = Menu(menu_glowne, tearoff=0)
menu_plik.add_command(label=teksty["menu"]["new"], command=newProject)
menu_plik.add_command(label=teksty["menu"]["import"], command=lambda: importuj(tree, drzewo_zakladek))
menu_plik.add_command(label=teksty["menu"]["export"], command=lambda: eksportuj(tree))
menu_glowne.add_cascade(label=teksty["menu"]["file"], menu=menu_plik)

menu_ustawienia = Menu(menu_glowne, tearoff=0)
menu_ustawienia.add_command(label=teksty["menu"]["change_theme"], command=zmien_motyw)
menu_ustawienia.add_command(label=teksty["menu"]["change_language"], command=lambda: zmien_jezyk(okno, reload_texts))
menu_glowne.add_cascade(label=teksty["menu"]["settings"], menu=menu_ustawienia)

menu_program = Menu(menu_glowne, tearoff=0)
menu_program.add_command(label=teksty["menu"]["about"], command=o_autorze)
menu_glowne.add_cascade(label=teksty["menu"]["program"], menu=menu_program)

# Dodanie Treeview
kolumny = ('nazwa', 'kategoria', 'url', 'przeglądarka', 'opis', 'otwórz', 'edytuj', 'usuń')
tree = ttk.Treeview(okno, columns=kolumny, show='headings')
for kolumna in kolumny:
    tree.heading(kolumna, text=kolumna.capitalize())
    tree.column(kolumna, width=100)
tree.pack(expand=True, fill='both')

# Dodanie przycisku z tekstem reprezentującym plusik
przycisk_dodaj = tk.Button(okno, text="+", command=lambda: dodaj_zakladke(okno, tree, drzewo_zakladek), font=("Arial", 16))
przycisk_dodaj.pack(side="right", padx=10, pady=10)

# Funkcja do przełączania stanu symulowanego checkboxa
def toggle_checkbox(event):
    region = drzewo_zakladek.identify("region", event.x, event.y)
    if region == "cell":
        rowid = drzewo_zakladek.identify_row(event.y)
        column = drzewo_zakladek.identify_column(event.x)
        if column == '#1':  # Kolumna checkboxów
            current_value = drzewo_zakladek.item(rowid, 'values')[0]
            new_value = '☑' if current_value == '☐' else '☐'
            drzewo_zakladek.item(rowid, values=(new_value,) + drzewo_zakladek.item(rowid, 'values')[1:])

# Powiązanie zdarzenia kliknięcia z funkcją toggle_checkbox
drzewo_zakladek.bind('<Button-1>', toggle_checkbox)

# Funkcja wywoływana, gdy użytkownik kliknie na kolumnę "Edytuj" lub "Usuń"
def on_treeview_click(event):
    item = tree.identify('item', event.x, event.y)
    column = tree.identify_column(event.x)
    if column == '#6':  # Przypuszczając, że kolumna "Otwórz" to szósta kolumna
        # Pobierz URL z wiersza
        url = tree.item(item, 'values')[2]  # Zakładamy, że URL znajduje się w trzeciej kolumnie
        chrome_browser.open_new_tab(url)
    elif column == '#7':  # Przypuszczając, że kolumna "Edytuj" to siódma kolumna
        print(f"Edytuj zakładkę {tree.item(item, 'values')}")
    elif column == '#8':  # Przypuszczając, że kolumna "Usuń" to siódma kolumna
        tree.delete(item)

# Dodanie obsługi zdarzeń kliknięcia
tree.bind("<Button-1>", on_treeview_click)

okno.mainloop()