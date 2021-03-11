import csv

ARCHIVO_PUNTUACIONES = 'puntuaciones.txt'


def historial_puntuaciones():
    '''
    Lee el archivo de puntuaciones para devolver las puntuaciones que haya.
    '''
    puntos_historicos = []
    with open(ARCHIVO_PUNTUACIONES) as puntuaciones:
        historial = puntuaciones.readline()
        datos = historial.split(';')

        for elemento in datos:
            if len(elemento) == 0:
                continue
            jugador, puntos = elemento.split(',')
            puntos_historicos.append((int(puntos), jugador))

        puntos_historicos = sorted(puntos_historicos, reverse=True)
        
        return puntos_historicos


def comparar_con_historial(puntos_historicos):
    '''
    Recorre los diez mejores puntajes para convertirlos en cadena y así escribirlo en el archivo.
    '''

    puntos_historicos = puntos_historicos[:10]

    historial = ''

    for puntos, nombre in puntos_historicos:
        historial += f'{nombre},{puntos};'
    
    with open(ARCHIVO_PUNTUACIONES, 'w') as puntuaciones:
        puntuaciones.writelines(historial)
    
    return puntos_historicos



def agregar_puntuacion(nombre, puntuacion_actual):
    '''
    Agrega la puntuación_actual al archivo de todas las puntuaciones.
    Devuelve una lista de tuplas con las 10 mejores puntuaciones.
    '''
    puntos_historicos = historial_puntuaciones()
    puntos_historicos.append((puntuacion_actual, nombre))
    puntos_historicos = sorted(puntos_historicos, reverse=True)

    if len(puntos_historicos) == 10:
        puntos_historicos = comparar_con_historial(puntos_historicos)
    else:
        with open(ARCHIVO_PUNTUACIONES, 'a') as puntuaciones:
            puntuaciones.writelines(nombre + ',' + str(puntuacion_actual) + ';')

    return puntos_historicos
