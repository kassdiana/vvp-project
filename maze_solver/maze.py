from math import inf
import random

import numpy as np
import matplotlib.pyplot as plt

# Směry pohybu: nahoru, dolů, doleva, doprava
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Maze:
    """
    Třída reprezentující bludiště, která umožňuje jeho načtení z CSV, vygenerování,
    převod na graf pomocí matice sousednosti, nalezení nejkratší cesty a její vizualizaci.
    """

    def __init__(self):
        """
        Inicializuje prázdnou instanci třídy Maze a připraví vnitřní struktury.
        """
        # Seznam seznamů / numpy pole reprezentující samotné bludiště
        self.matrix = []

        # Slovník, který mapuje souřadnice (x, y)
        self.passable_cells = {}

        # Matice sousednosti
        self.adjacency_matrix = []

    def load_from_csv(self, csv_file: str) -> None:
        """
        Načte bludiště ze souboru formátu CSV.

        :param csv_file: Cesta k souboru s příponou .csv obsahující matici bludiště.
        """
        self.matrix = []
        with open(csv_file, encoding='utf-8') as file:
            self.matrix = np.array(
                [
                    [info.strip() == "1" for info in line.split(",")]
                    for line in file
                ], dtype=bool
            )

    def build_graph(self) -> None:
        """
        Převede 2D mřížku bludiště do podoby grafu.
        Zmapuje všechny průchozí buňky a vytvoří pro ně matici sousednosti.
        """
        self.passable_cells = {}
        index = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if not self.matrix[i][j]:
                    self.passable_cells[(i, j)] = index
                    index += 1

        length = len(self.passable_cells)

        self.adjacency_matrix = np.zeros(
            (length, length),
            dtype=int
        )

        for (x, y), value in self.passable_cells.items():
            for d1, d2 in DIRECTIONS:
                coordinate = self.passable_cells.get((x + d1, y + d2))
                if coordinate is not None:
                    self.adjacency_matrix[value][coordinate] = 1

    def find_shortest_path(self) -> list[int] | None:
        """
        Najde nejkratší cestu z levého horního rohu (0, 0) do pravého dolního rohu (n - 1, m - 1).
        :return: Seznam indexů průchozích vrcholů tvořících nejkratší cestu, nebo None, pokud cesta neexistuje
        """
        if (0, 0) not in self.passable_cells or (len(self.matrix) - 1,
                                                  len(self.matrix[0]) - 1) not in self.passable_cells:
            return None

        count_vertex = len(self.passable_cells)
        # Seznam délek nejkratších cest od počátku
        short_roads = [inf for _ in range(count_vertex)]

        # Seznam indikující, zda byl vrchol již navštíven
        visited_vertex = [False for _ in range(count_vertex)]

        # Seznam pro rekonstrukci cesty
        road = [None for _ in range(count_vertex)]

        # Startovní pozice
        start = self.passable_cells[(0, 0)]
        short_roads[start] = 0
        finish_path = []

        # Dijkstrův algoritmus
        for _ in range(count_vertex):
            min_length = inf
            index_min_length = 0

            for i in range(count_vertex):
                if not visited_vertex[i] and min_length > short_roads[i]:
                    min_length = short_roads[i]
                    index_min_length = i

            visited_vertex[index_min_length] = True

            for j in range(count_vertex):
                if self.adjacency_matrix[index_min_length][j] == 1:
                    new_length = short_roads[index_min_length] + 1
                    if new_length < short_roads[j]:
                        short_roads[j] = new_length
                        road[j] = index_min_length

        last_point = self.passable_cells[
            (len(self.matrix) - 1,
             len(self.matrix[0]) - 1)
        ]

        if short_roads[last_point] == inf:
            return None

        while last_point is not None:
            finish_path.append(last_point)
            last_point = road[last_point]

        return finish_path[::-1]

    def save_image(self, path: list[int], filename: str = 'images/vysledek.png') -> None:
        """
        Vykreslí bludiště s vyznačenou nejkratší cestou a uloží jej jako obrázek.

        :param path: Seznam indexů vrcholů představujících nejkratší cestu.
        :param filename: Cesta a název souboru, kam se má výsledný obrázek uložit (výchozí: 'images/vysledek.png').
        """
        dict_index = {}

        color_matrix = np.full(
            (len(self.matrix),
             len(self.matrix[0]),
             3),
            255
        )

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j]:
                    color_matrix[i][j] = [0, 0, 0]

        for key in self.passable_cells:
            dict_index[self.passable_cells[key]] = key

        for vertex in path:
            i, j = dict_index[vertex]
            color_matrix[i][j] = [255, 0, 0]

        plt.imshow(color_matrix)
        plt.savefig(filename)
        plt.show()

    def generate_maze(self, size: int = 10, wall: float = 0.2, template: str = "random") -> None:
        """
        Vygeneruje náhodné bludiště o dané velikosti a zaručí existenci průchozí cesty.
        :param size: Rozměr bludiště (šířka i výška)
        :param wall: Pravděpodobnost výskytu zdi (překážky) na daném políčku (použito pouze u šablony 'random').
        :param template: Šablona bludiště. Podporované hodnoty: 'random' (náhodné), 'empty' (prázdné), 'slalom' (klikatá cesta).
        """
        self.matrix = np.zeros((size, size), dtype=bool)

        if template == "empty":
            # Prázdné bludiště bez zdí
            pass

        elif template == "slalom":
            # Vytvoření šablony slalomu (střídavé horizontální zdi s průchody)
            for i in range(1, size, 2):
                self.matrix[i] = True
                if (i // 2) % 2 == 0:
                    self.matrix[i][-1] = False
                else:
                    self.matrix[i][0] = False
            self.matrix[-1][-1] = False

        elif template == "random":
            #Generování náhodného bludiště s kontrolou průchodnosti
            cells = [
                (i, j)
                for i in range(size)
                for j in range(size)
                if (i, j) not in [(0, 0), (size - 1, size - 1)]
            ]

            random.shuffle(cells)

            for (i, j) in cells:
                if random.random() < wall:
                    continue

                self.matrix[i][j] = True

                self.build_graph()
                result = self.find_shortest_path()

                if result is None:
                    self.matrix[i][j] = False
        
        else:
            raise ValueError(f"Neznámá šablona bludiště: {template}")