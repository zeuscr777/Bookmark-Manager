import json

def wczytaj_teksty(jezyk):
    try:
        with open(f"jezyki/polski/{jezyk}_language.json", "r", encoding="utf-8") as file:
            teksty = json.load(file)
            return teksty
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku languages/{jezyk}_language.json")
        return {}
