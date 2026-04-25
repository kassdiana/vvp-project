# Hledání nejkratší cesty v bludišti

## Autorství
Tento projekt byl vypracován v rámci předmětu **Vědecké výpočty v Pythonu**.
- **Studentka:** Diana Kassymbekova
- **Osobní číslo:** KAS0301

## Popis projektu
Tento projekt implementuje třídu `Maze`, která umožňuje práci s bludišti v Pythonu. Cílem je načíst bludiště z CSV souboru nebo jej **náhodně vygenerovat**, převést jej na graf, nalézt nejkratší cestu pomocí **Dijkstrova algoritmu** (za využití matice sousednosti) a výsledek vizualizovat jako obrázek.

Vnitřní reprezentace bludiště funguje jako 2D matice, kde:
- `True` = zeď (neprůchozí),
- `False` = volná cesta (průchozí).

Startovací bod je vždy v levém horním rohu `[0, 0]`, cílový bod je v pravém dolním rohu `[n-1, n-1]`.

Výstupem je obrázek uložený ve složce `images/` (standardně `shape.png`), kde:
- **Černá** = zdi  
- **Bílá** = volné průchozí buňky  
- **Červená** = nalezená nejkratší cesta

---

## Funkcionalita

- **Generování bludiště:** Metoda `generate_maze()` dokáže vytvořit náhodné bludiště zvolené velikosti se zadanou pravděpodobností výskytu zdí a garantuje, že do cíle existuje cesta.
- **Načítání z CSV:** Metoda `load_from_csv()` pro načtení externího bludiště ze souboru.
- **Převod na graf:** Metoda `build_graph()` mapuje průchozí souřadnice a sestavuje matici sousednosti.
- **Hledání nejkratší cesty:** Metoda `find_shortest_path()` vyhledá optimální cestu od startu do cíle.
- **Vykreslení cesty:** Metoda `save_image()` pomocí knihovny Matplotlib vykreslí vizualizaci a uloží ji do formátu PNG.

---

## Struktura repozitáře

```text
vvp-project/
├── data/
│   ├── maze_1.csv
│   ├── maze_2.csv
│   ├── maze_3.csv
│   ├── maze_4.csv
│   └── maze_5.csv        # zdrojová data pro testování
├── images/               # složka pro uložené výsledky (obrázky)
├── maze_solver/          # složka s knihovnou
│   ├── __init__.py       # inicializační soubor
│   └── maze.py           # hlavní soubor s třídou Maze
├── examples.ipynb        # ukázky spuštění a vizualizace (Jupyter Notebook)
└── README.md
```

---

## Použité knihovny

- `numpy` (práce s maticemi a efektivní ukládání dat)
- `matplotlib` (vykreslení a uložení výsledného obrázku)
- Standardní knihovny: `math` (nekonečno), `random` (pro generování bludiště)

---

## Rychlá ukázka použití

```python
from maze_solver.maze import Maze

# Vytvoření instance a načtení dat
maze = Maze()
maze.load_from_csv("data/maze_1.csv")

# Hledání cesty
path = maze.find_shortest_path()

# Uložení obrázku
maze.save_image(path, filename="images/vysledek.png")
```

---

## Poznámka k prostředí

Projekt je doporučeno spouštět ve virtuálním prostředí (venv).

### Nastavení prostředí
```bash
# Vytvoření virtuálního prostředí
python -m venv venv

# Aktivace (Windows)
# venv\Scripts\activate

# Aktivace (Linux/macOS)
source venv/bin/activate

# Instalace závislostí
pip install numpy matplotlib jupyter

# Spuštění interaktivního notebooku s ukázkami
jupyter notebook examples.ipynb
```