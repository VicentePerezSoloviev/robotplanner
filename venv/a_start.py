import numpy as np
import cv2

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node, maze):
    camino = []
    result = [[-1 for i in range(len(maze[0]))] for j in range(len(maze))]
    current = current_node
    while current is not None:
        camino.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    camino = camino[::-1]
    start_value = 0
    # we update the path of start to end found by A-star serch with every step incremented by 1
    for i in range(len(camino)):
        result[camino[i][0]][camino[i][1]] = start_value
        start_value += 1
    return result

def search(maze, cost, start, end):

    nodo_fin = Node(None, tuple(end))
    nodo_fin.g = nodo_fin.h = nodo_fin.f = 0

    nodo_ini = Node(None, tuple(start))
    nodo_ini.g = nodo_ini.h = nodo_ini.f = 0

    nodos_por_visitar = []
    nodos_visitados = []

    nodos_por_visitar.append(nodo_ini)

    outer_iterations = 0
    maximo_iter = (len(maze) // 2) ** 7 #numero máximo de iteraciones muy alto para evitar bucles

    while len(nodos_por_visitar) > 0:
        outer_iterations += 1
        print (outer_iterations)

        current_node = nodos_por_visitar[0]
        current_index = 0
        for index, item in enumerate(nodos_por_visitar):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > maximo_iter:
            print("En numero de iteraciones ha superado el maximo")
            return return_path(current_node, maze)

        if current_node == nodo_fin:
            return return_path(current_node, maze)

        nodos_por_visitar.pop(current_index)        #sacamos del monton por visitar
        nodos_visitados.append(current_node)        #y añadimos al monton de visitados

        hijos = []
        move = [[-1, 0], [0, -1], [1, 0], [0, 1]]   #movimientos para encontrar hijos

        for hijo in move:
            node_position = (current_node.position[0] + hijo[0], current_node.position[1] + hijo[1])

            if (node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[0]) - 1) or node_position[1] < 0):   #limites
                continue
            if maze[node_position[0]][node_position[1]] != 0: continue   #miramos si es terreno para navegar

            new_node = Node(current_node, node_position)
            hijos.append(new_node)

        for child in hijos:
            if len([visited_child for visited_child in nodos_visitados if visited_child == child]) > 0: continue    #ya está visitado

            child.g = current_node.g + cost
            child.h = (((child.position[0] - nodo_fin.position[0])**2) + ((child.position[1] - nodo_fin.position[1])**2))   #distancia euclidea
            child.f = child.g + child.h

            if len([i for i in nodos_por_visitar if child == i and child.g > i.g]) > 0: continue #en caso de que el que ya esta metido sea mejor

            nodos_por_visitar.append(child)

def img2grid (file):
    img = cv2.imread(file)
    Mat = []

    for i in range (len(img)):
        Mat.append([])
        for j in range (len(img[i])):
            Mat[i].append([])
            if np.array_equal(img[i][j], np.array([0, 0, 0], np.int32)):            #negro
                Mat[i][j] = 1
            elif np.array_equal(img[i][j], np.array([255, 255, 255], np.int32)):    #blanco
                Mat[i][j] = 0
            elif np.array_equal(img[i][j], np.array([0, 255, 0], np.int32)):    #inicio
                Mat[i][j] = 0
                inicio = [i,j]
            elif np.array_equal(img[i][j], np.array([0, 255, 255], np.int32)):  # fin
                Mat[i][j] = 0
                fin = [i, j]
            else:
                Mat[i][j] = 2

    return Mat, inicio, fin

def grid2img (mat):
    img2 = np.zeros((len(mat), len(mat[0]), 3), np.uint8)

    for i in range (len(mat)):
        for j in range (len(mat[i])):
            if mat[i][j] == 1:
                img2[i][j] = [0, 0, 0]
            elif mat[i][j] == 0:
                img2[i][j] = [255, 255, 255]
            else:
                img2[i][j] = [0, 0, 255]

    cv2.imwrite('../img.png', img2)

if __name__ == '__main__':

    maze, start, end = img2grid('C:/Users/Vicente/PycharmProjects/p3robots_planner/Labirinto_003.png')
    print (maze)
    for i in maze:
        print (i)

    '''start = [0, 0]  # starting position
    end = [40, 40]  # ending position'''
    cost = 1  # cost per movement

    camino = search(maze, cost, start, end)

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (camino[i][j] != -1):
                maze[i][j] = 2    #blanco para caminos sin navegar

    grid2img(maze)

    print(maze)