# DFS and A* Pathfinding Algorithms - Enhanced Implementation

This compressed folder includes two main `.py` files: `enhanced.py` and `main.py`.

- `main.py` → Contains the original BFS code modified into DFS. This corresponds to the first part of the deliverable.
- `enhanced.py` → Contains the DFS code with several enhancements.

## Enhancements in `enhanced.py`

### 1. EXTRA (ALGORITHMIC): A* ALGORITHM IMPLEMENTED WITH HEURISTIC

```python
# A* Algorithm
def a_star(charMap, start, goal):
    open_set = []
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set.append(start)
    parent = {start: None}

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
                    continue  # Wall or visited

                tentative_g_score = g_score[current] + 1

                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                if neighbor not in open_set:
                    open_set.append(neighbor)

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    parent[neighbor] = current

    return []

# Reconstruct path for A*
def reconstruct_path(parent, current):
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

# Heuristic for A*
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])  # Manhattan Distance
```

---

### 2. EXTRA (ALGORITHMIC): BACKTRACE ADDED TO GREEDY (DFS)

```python
# DFS Algorithm
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

    return []

# Reconstruct path for DFS
def reconstruct_dfs_path(parent, current):
    path = []
    while current:
        path.append(current)
        current = parent[current]
    return path[::-1]
```

---

### 3. EXTRA (COMPARISON): QUANTITATIVE COMPARISON OF ALGORITHMS (TIME & DISTANCE)

The script extracts time and distance metrics (displaying the path taken by each algorithm) for comparison. Each part of the data extraction is commented within `enhanced.py`.

---

### 4. EXTRA (MINOR): CONVERSION TO ROBOT MOVEMENT COMMANDS

```python
# Path to movement command conversion
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
```

---

### 5. EXTRA (MINOR): VISUALIZATION IMPROVED USING PYGAME

Real-time progressive visualization is implemented using `pygame` as the algorithms execute.

---

### 6. EXTRA (MINOR): VIDEO LINK

Watch the demonstration here: https://youtu.be/WoCieLZ7qy8

---

### 7. ADDITIONAL EXTRAS

- **Random map loading**: Maps are randomly selected from folders `map1` to `map11`. This ensures a different map is visualized on each run.
- **Automatic start/goal extraction**: Start and goal coordinates are extracted from the `README.md` file inside each `map1` to `map11` folder. A script reads these files to retrieve the coordinates automatically.

---

## APPENDIX I

- **Important**: You must update the path in the scripts to correctly extract data from the `master-ipr` folder.
- Each function and enhancement is explained step by step within the code, making it easy to follow the development process.

---

**Author**: José Pablo Palmero Ramos
