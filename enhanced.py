import os
import csv
import random
import pygame
import time
import re

# Constantes
MAP_BASE_DIR = "/home/jospalram/Descargas/master-ipr"  # Directorio base que contiene las carpetas de mapas
NUM_MAPS = 1  # Número de mapas a seleccionar y procesar aleatoriamente
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40

# Direcciones
DIRECTIONS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
}

# Clase Nodo
class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId

    def dump(self):
        print(f"---------- x {self.x} | y {self.y} | id {self.myId} | parentId {self.parentId}")

# Cargar mapa desde un CSV
def load_map(filename):
    charMap = []
    with open(filename) as f:
        line = f.readline()
        while line:
            charLine = line.strip().split(',')
            charMap.append(charLine)
            line = f.readline()
    return charMap

# Extraer coordenadas del archivo README.md
def extract_coordinates(readme_path):
    with open(readme_path, 'r') as file:
        content = file.read()

    # Extraer las líneas de origen y destino usando expresiones regulares
    origin_match = re.search(r'Origin: Line (\d+), Column (\d+)', content)
    destiny_match = re.search(r'Destiny: Line (\d+), Column (\d+)', content)

    if origin_match and destiny_match:
        origin_line = int(origin_match.group(1))
        origin_column = int(origin_match.group(2))
        destiny_line = int(destiny_match.group(1))
        destiny_column = int(destiny_match.group(2))
        return (origin_line, origin_column), (destiny_line, destiny_column)
    else:
        raise ValueError("No se pudieron extraer las coordenadas de origen o destino del archivo readme.md.")

# Mostrar el mapa en consola
def dump_map(charMap):
    for line in charMap:
        print(line)

# Algoritmo A*
def a_star(charMap, start, goal):
    open_set = []
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set.append(start)
    parent = {start: None}  # Rastrear el nodo padre de cada nodo

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        
        if current == goal:
            return reconstruct_path(parent, current)

        open_set.remove(current)
        closed_set.add(current)

        for direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < len(charMap) and 0 <= neighbor[1] < len(charMap[0]):
                if charMap[neighbor[0]][neighbor[1]] in ['1', '2']:
                    continue  # Pared o visitado

                tentative_g_score = g_score[current] + 1

                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue  # No es un mejor camino

                if neighbor not in open_set:
                    open_set.append(neighbor)

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    parent[neighbor] = current  # Rastrear cómo llegamos a este vecino

    return []  # Devolver una ruta vacía si no se encuentra ninguna ruta

# Reconstruir la ruta desde el algoritmo A*
def reconstruct_path(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]  # Usar el diccionario de padres para rastrear la ruta
    return path[::-1]  # Invertir la ruta

# Heurística para A*
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])  # Distancia Manhattan


# Algoritmo DFS
def dfs(charMap, start, goal):
    stack = [start]
    visited = set()
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return reconstruct_dfs_path(parent, current)

        for direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < len(charMap) and 0 <= neighbor[1] < len(charMap[0]):
                if charMap[neighbor[0]][neighbor[1]] in ['1', '2'] or neighbor in visited:
                    continue
                stack.append(neighbor)
                parent[neighbor] = current

    return []  # Devolver una ruta vacía si no se encuentra ninguna ruta

# Reconstruir la ruta para DFS
def reconstruct_dfs_path(parent, current):
    path = []
    while current:
        path.append(current)
        current = parent[current]
    return path[::-1]

# Conversión de comandos para el robot
def convert_to_commands(path):
    commands = []
    for i in range(1, len(path)):
        x_diff = path[i][0] - path[i - 1][0]
        y_diff = path[i][1] - path[i - 1][1]

        if x_diff == -1:
            commands.append('move up')
        elif x_diff == 1:
            commands.append('move down')
        elif y_diff == -1:
            commands.append('move left')
        elif y_diff == 1:
            commands.append('move right')
    return commands

# Visualización progresiva usando Pygame con título de ventana
def visualize_path_progressive(charMap, path, algorithm_name):
    pygame.init()
    pygame.display.set_caption(f"Pathfinding Visualization - {algorithm_name}")  # Establecer título de la ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    running = True
    current_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Limpiar pantalla

        # Dibujar el mapa
        for y, row in enumerate(charMap):
            for x, cell in enumerate(row):
                color = (255, 255, 255)  # Espacio libre
                if cell == '1':
                    color = (255, 0, 0)  # Pared
                elif cell == '2':
                    color = (0, 255, 0)  # Visitado
                elif cell == '3':
                    color = (0, 0, 255)  # Inicio
                elif cell == '4':
                    color = (255, 255, 0)  # Objetivo

                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dibujar la ruta progresivamente
        if current_index < len(path):
            x, y = path[current_index]
            pygame.draw.rect(screen, (0, 255, 255), (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            current_index += 1

        pygame.display.flip()
        clock.tick(10)  # Ajustar la velocidad según sea necesario

    pygame.quit()
    print(f"Visualización de la ruta {algorithm_name} completa!")

# Actualizar la función principal para leer coordenadas desde readme.md
def main():
    # Listar todas las carpetas de mapas
    map_dirs = [f"map{i}" for i in range(1, 12)]  # ['map1', 'map2', ..., 'map11']

    # Seleccionar aleatoriamente una carpeta de mapa
    selected_map_dir = random.choice(map_dirs)
    full_map_dir_path = os.path.join(MAP_BASE_DIR, selected_map_dir)
    
    # Construir la ruta completa al archivo CSV y readme.md dentro del directorio seleccionado
    csv_file_name = f"{selected_map_dir}.csv"  # e.g., 'map1.csv'
    full_csv_path = os.path.join(full_map_dir_path, csv_file_name)
    readme_path = os.path.join(full_map_dir_path, "README.md")

    # Extraer coordenadas de inicio y objetivo desde readme.md
    start, goal = extract_coordinates(readme_path)
    print(f"Coordenadas de inicio: {start}")
    print(f"Coordenadas de objetivo: {goal}")

    # Cargar el mapa seleccionado
    charMap = load_map(full_csv_path)
    
    # Mostrar el mapa cargado
    print(f"Mapa seleccionado: {selected_map_dir}")
    dump_map(charMap)

    # Ejecutar el algoritmo A*
    start_time = time.time()
    a_star_path = a_star(charMap, start, goal)
    a_star_time = time.time() - start_time
    print("Ruta A*:", a_star_path)
    print("Tiempo A*:", a_star_time)

    # Ejecutar el algoritmo DFS
    start_time = time.time()
    dfs_path = dfs(charMap, start, goal)
    dfs_time = time.time() - start_time
    print("Ruta DFS:", dfs_path)
    print("Tiempo DFS:", dfs_time)

    # Convertir rutas a comandos
    a_star_commands = convert_to_commands(a_star_path)
    dfs_commands = convert_to_commands(dfs_path)
    
    print("Comandos A*:", a_star_commands)
    print("Comandos DFS:", dfs_commands)

    # Visualizar la ruta A* progresivamente
    print("Visualizando la ruta A*...")
    visualize_path_progressive(charMap, a_star_path, "A*")

    # Visualizar la ruta DFS progresivamente
    print("Visualizando la ruta DFS...")
    visualize_path_progressive(charMap, dfs_path, "DFS")

if __name__ == "__main__":
    main()