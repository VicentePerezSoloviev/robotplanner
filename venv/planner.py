import cv2
import numpy as np
import math

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
            if mat[i][j] == 0:
                img2[i][j] = [255, 255, 255]
            if mat[i][j] == 1:
                img2[i][j] = [0,0,0]
            if mat[i][j] == 2:
                img2[i][j] = [0, 0, 255]

    cv2.imwrite('../img.png', img2)

def distance2final (posRel, posFin):
    return math.sqrt(pow(posFin[0] - posRel[0], 2) + pow(posFin[1] - posRel[1], 2))

def distanceIdeal (posIni, posRel, posFin):
    d2f = distance2final(posRel, posFin)
    d2i = distance2final(posRel, posIni)

    #return d2i - d2f
    if d2i != 0 and d2f != 0:
        return 1/d2f - 1/d2i
    elif d2f == 0:
        return d2i
    else: return d2f
    #return d2f - 1.2*(d2i)    #cuanto menor sea mejor

def column(matrix, i):
    return [row[i] for row in matrix]

def findPath (mat, posIni, posFin):
    posRel = posIni
    posAnterior = []
    i = 0
    bestSplit = posRel

    #while posRel != posFin and i != 100:
    for i in range (100000):
        values = []
        if (posRel[0] + 1 < len(mat) and mat[posRel[0] + 1][posRel[1]] == 0):
            values.append([distanceIdeal(posIni, [posRel[0] + 1, posRel[1]], posFin), [posRel[0] + 1, posRel[1]]])
        if (posRel[0] - 1 > 0 and mat[posRel[0] - 1][posRel[1]] == 0):
            values.append([distanceIdeal(posIni, [posRel[0] - 1, posRel[1]], posFin), [posRel[0] - 1, posRel[1]]])
        if (posRel[1] + 1 < len(mat[0]) and mat[posRel[0]][posRel[1] + 1] == 0):
            values.append([distanceIdeal(posIni, [posRel[0], posRel[1] + 1], posFin), [posRel[0], posRel[1] + 1]])
        if (posRel[1] - 1 >= 0 and mat[posRel[0]][posRel[1] - 1] == 0):
            values.append([distanceIdeal(posIni, [posRel[0], posRel[1] - 1], posFin), [posRel[0], posRel[1] - 1]])

        # [dist, [pos]]
        if (len(values) > 0):
            mx = np.amax(column(values, 0))
            for i in range (len(values)):
                if values[i][0] == mx:
                    index = i

            bestSplit = values[index][1]
            posRel = bestSplit  #actualizo posicion
            mat[bestSplit[0]][bestSplit[1]] = 2 #pinto camino
            print (values[index])

        i = i+1
    return mat

def main():
    mat, inicio, fin = img2grid('C:/Users/Vicente/PycharmProjects/p3robots_planner/Labirinto_003.png')   #matriz de 0s y 1s con el mapa
    mat = findPath(mat, inicio, fin)
    grid2img(mat)



    print('Exe finished')




# --------------------------------------------------------------------------

if __name__ == '__main__':
    main()