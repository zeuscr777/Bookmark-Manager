import tkinter as tk
from tkinter import Toplevel, ttk

def zmien_motyw():
    # Logika zmiany motywu
    pass

def zmien_jezyk(main_window, reload_texts):
    def apply_language():
        # Używamy pełnej ścieżki do pliku językowego w mapowaniu
        selected_language_path = language_map[language_var.get()]
        reload_texts(selected_language_path)
        language_window.destroy()

    language_window = Toplevel(main_window)
    language_window.title("Zmień język")
    language_window.geometry("200x100")

    # Mapowanie nazw języków do ścieżek plików
    languages = ["polski", "angielski", "niemiecki"]
    language_map = {
        "polski": "jezyki/polski/pl_language.json",
        "angielski": "jezyki/angielski/en_language.json",
        "niemiecki": "jezyki/niemiecki/de_language.json"
    }
    language_var = tk.StringVar(language_window)
    language_var.set("polski")  # wartość domyślna

    tk.OptionMenu(language_window, language_var, *languages).pack()
    tk.Button(language_window, text="Zastosuj", command=apply_language).pack()

