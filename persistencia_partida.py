import csv

ARCHIVO_PARTIDA = 'partida.txt'

def guardar_partida(sup, pieza_actual, puntuacion):
    '''
    Convierte a la superficie, pieza y puntuacion en cadena para escribirlo en el archivo y guardar la partida.
    '''
    superficie = ''
    pieza = ''
    with open(ARCHIVO_PARTIDA, 'w') as partida:
        for x, y in sup:
            superficie += f'{x},{y};'
        partida.writelines(superficie.rstrip(';') + ' # sup' +'\n')

        for x, y in pieza_actual:
            pieza += f'{x},{y};'
        partida.writelines(pieza.rstrip(';') + ' # pieza' + '\n')
            
        partida.writelines(str(puntuacion))

def convertir_superficie_pieza(fila):
    '''
    Convierte la superficie/pieza que está en forma de cadena y la devuelve en una lista de tuplas.
    '''
    coordenadas = fila[0].split(';')
    estado_juego = []
    for coordenada in coordenadas:
        if len(coordenada) == 4:
            acomodar_coordenada = ''
            acomodar_coordenada += coordenada[2] + coordenada[3]
            estado_juego.append((int(coordenada[0]), int(acomodar_coordenada)))
        else:
            estado_juego.append((int(coordenada[0]), int(coordenada[2])))
    return estado_juego


def cargar_partida():
    '''
    Carga la partida guardada anteriormente.
    Devolviendo la superficie, pieza_actual y puntuacion correspondiente
    '''
    with open(ARCHIVO_PARTIDA) as piezas:
        lector = csv.reader(piezas, delimiter=' ')

        for fila in lector:
            if len(fila) == 1:
                puntuacion = int(fila[0])
                continue 
            
            if fila[2] == 'sup':
                superficie = convertir_superficie_pieza(fila)
            if fila[2] == 'pieza':
                pieza_actual = convertir_superficie_pieza(fila)

    return superficie, pieza_actual, puntuacion
