#! /usr/bin/env python

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)

#FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv" # Linux-style absolute path
#FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" # Windows-style absolute path, note the `\\` and edit `USER_NAME`
#FILE_NAME = "../../../../map1/map1.csv" # Linux-style relative path
FILE_NAME = "/home/jospalram/Descargas/master-ipr/map1/map1.csv" # Windows-style relative path, note the `\\`
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2

# # Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

# # Mapa

# ## Creamos estructura de datos para mapa

charMap = []

# ## Creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

# ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## A nivel mapa, integramos la info que teníamos de start & end

charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# ## Volcamos mapa por consola

dumpMap()

# # Grafo búsqueda

# ## Creamos el primer nodo
init = Node(START_X, START_Y, 0, -2)
# init.dump() # comprobar que primer nodo bien

# ## `nodes` contendrá los nodos del grafo

nodes = []

# ## Añadimos el primer nodo a `nodes`

nodes.append(init)

# ## Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

counter = 0

while not done:
    if counter > 2:
        quit()
    counter = counter +1
    
    print("--------------------- number of nodes: "+str(len(nodes)))
    node = nodes[-1]
    node.dump() # comprobar que nodo bien


    # up
    tmpX = node.x - 1
    tmpY = node.y
    if( charMap[tmpX][tmpY] == '4' ):
        print("up: GOALLLL!!!")
        goalParentId = node.myId  # aquí sustituye por real
        done = True
        break
    elif ( charMap[tmpX][tmpY] == '0' ):
        print("up: mark visited")
        newNode = Node(tmpX, tmpY, len(nodes), node.myId)
        charMap[tmpX][tmpY] = '2'
        nodes.append(newNode)
        dumpMap()
        continue

    # right
    tmpX = node.x
    tmpY = node.y + 1
    if( charMap[tmpX][tmpY] == '4' ):
        print("right: GOALLLL!!!")
        goalParentId = node.myId # aquí sustituye por real
        done = True
        break
    elif ( charMap[tmpX][tmpY] == '0' ):
        print("right    : mark visited")
        newNode = Node(tmpX, tmpY, len(nodes), node.myId)
        charMap[tmpX][tmpY] = '2'
        nodes.append(newNode)
        dumpMap()
        continue
    
    # down
    tmpX = node.x + 1
    tmpY = node.y
    if( charMap[tmpX][tmpY] == '4' ):
        print("down: GOALLLL!!!")
        goalParentId = node.myId # aquí sustituye por real
        done = True
        break
    elif ( charMap[tmpX][tmpY] == '0' ):
        print("down: mark visited")
        newNode = Node(tmpX, tmpY, len(nodes), node.myId)
        charMap[tmpX][tmpY] = '2'
        nodes.append(newNode)
        dumpMap()
        continue

    
    # left
    tmpX = node.x
    tmpY = node.y - 1
    if( charMap[tmpX][tmpY] == '4' ):
        print("left: GOALLLL!!!")
        goalParentId = node.myId # aquí sustituye por real
        done = True
        break
    elif ( charMap[tmpX][tmpY] == '0' ):
        print("left: mark visited")
        newNode = Node(tmpX, tmpY, len(nodes), node.myId)
        charMap[tmpX][tmpY] = '2'
        nodes.append(newNode)
        dumpMap()
        continue


# ## Display solución hallada

print("%%%%%%%%%%%%%%%%%%%")
ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            node.dump() #Volcar información por pantalla
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True
