#-*-coding: utf-8-*-
#!/usr/bin/env python

# Lógica para ciencias de la computación

#Proyecto desarrollado por Juan Camilo Llanos Gómez y Edwin Alejadro Forero Gómez
#2018 - II

#---------------------------------------------------TRES ALFÍLES EN UN TABLERO DE AJEDRÉZ ----------------------------------------------------

# Visualizacion de tableros de ajedrez 3x3 a partir de
# una lista de literales. Cada literal representa una casilla;
# el literal es positivo sii hay una alfil en la casilla.

# Formato de la entrada: - las letras proposionales seran: 1, ..., 9;
#                        - solo se aceptan literales (ej. 1, ~2, 3, ~4, etc.)
# Requiere tambien un numero natural, para servir de indice del tablero,
# toda vez que puede solicitarse visualizar varios tableros.

# Salida: archivo alfil's_%i.png, donde %i es un numero natural


def dibujar_tablero(f, n):
    # Visualiza un tablero dada una formula f
    # Input:
    #   - f, una lista de literales
    #   - n, un numero de identificacion del archivo
    # Output:
    #   - archivo de imagen alfil's_n.png

    # Inicializo el plano que contiene la figura
    fig, axes = plt.subplots()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)

    # Dibujo el tablero
    step = 1./3
    tangulos = []
    # Creo los cuadrados claros en el tablero
    tangulos.append(patches.Rectangle(\
                                    (0, step), \
                                    step, \
                                    step,\
                                    facecolor='#F3F3F3')\
                                    )
    tangulos.append(patches.Rectangle(*[(step, 0), step, step],\
            facecolor='#F3F3F3'))
    tangulos.append(patches.Rectangle(*[(2 * step, step), step, step],\
            facecolor='#F3F3F3'))
    tangulos.append(patches.Rectangle(*[(step, 2 * step), step, step],\
            facecolor='#F3F3F3'))
    # Creo los cuadrados oscuros en el tablero
    tangulos.append(patches.Rectangle(*[(2 * step, 2 * step), step, step],\
            facecolor='#D44020'))
    tangulos.append(patches.Rectangle(*[(0, 2 * step), step, step],\
            facecolor='#D44020'))
    tangulos.append(patches.Rectangle(*[(2 * step, 0), step, step],\
            facecolor='#D44020'))
    tangulos.append(patches.Rectangle(*[(step, step), step, step],\
            facecolor='#D44020'))
    tangulos.append(patches.Rectangle(*[(0, 0), step, step],\
            facecolor='#D44020'))

    # Creo las líneas del tablero
    for j in range(3):
        locacion = j * step
        # Crea linea horizontal en el rectangulo
        tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.005],\
                facecolor='black'))
        # Crea linea vertical en el rectangulo
        tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.005, 1],\
                facecolor='black'))

    for t in tangulos:
        axes.add_patch(t)

    # Cargando imagen de alfil
    arr_img = plt.imread("alfil.png", format='png')
    imagebox = OffsetImage(arr_img, zoom=0.25)
    imagebox.image.axes = axes

    # Creando las direcciones en la imagen de acuerdo a literal
    direcciones = {}
    direcciones[1] = [0.165, 0.835]
    direcciones[2] = [0.5, 0.835]
    direcciones[3] = [0.835, 0.835]
    direcciones[4] = [0.165, 0.5]
    direcciones[5] = [0.5, 0.5]
    direcciones[6] = [0.835, 0.5]
    direcciones[7] = [0.165, 0.165]
    direcciones[8] = [0.5, 0.165]
    direcciones[9] = [0.835, 0.165]

    for l in f:
        if '-' not in l:
            ab = AnnotationBbox(imagebox, direcciones[int(l)], frameon=False)
            axes.add_artist(ab)

    # plt.show()
    fig.savefig("alfil's_" + str(n) + ".png")


#################
# importando paquetes para dibujar
print "Importando paquetes..."
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import csv
from sys import argv
print "Listo!"

script, data_archivo = argv

with open(data_archivo) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    contador = 1
    for l in data:
        print "Dibujando tablero:", l
        dibujar_tablero(l, contador)
        contador += 1

csv_file.close()
