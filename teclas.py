import tetris
import csv
import persistencia_partida

def identificar_tecla():
    '''
    Identifica y devuelve un diccionario con la tecla presionada como clave y su acción como valor.
    '''
    teclas = {}
    with open('teclas.txt') as acciones_teclas:
        lector = csv.reader(acciones_teclas, delimiter=' ')
        for fila in lector:
            if len(fila) == 0:
                continue

            teclas[fila[0]] = fila[2]

        return teclas

def descender(juego, siguiente_pieza, event):
    '''
    Devuelve el nuevo estado del juego al descender.
    '''
    return tetris.avanzar(juego, siguiente_pieza)

def guardar(juego, puntuacion):
    '''
    Guarda la partida actual.
    '''
    superficie, pieza_actual = juego
    persistencia_partida.guardar_partida(superficie, pieza_actual, puntuacion)

def cargar(juego, puntuacion, event):
    '''
    Devuelve el nuevo estado del juego conjunto a la puntuacion guardada.
    '''
    superficie, pieza_actual, puntuacion = persistencia_partida.cargar_partida()
    juego = superficie, pieza_actual
    return juego, puntuacion

def mover_derecha(juego):
    '''
    Devuelve el nuevo estado del juego al mover a la derecha.
    '''
    juego = tetris.mover(juego, tetris.DERECHA)
    return juego

def mover_izquierda(juego):
    '''
    Devuelve el nuevo estado del juego al mover a la izquierda.
    '''
    juego = tetris.mover(juego, tetris.IZQUIERDA)
    return juego

def rotar(juego):
    '''
    Devuelve el nuevo estado del juego al rotar la pieza
    '''
    juego = tetris.rotar(juego)
    return juego
