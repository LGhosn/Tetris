import csv

def convertir_rotacion(fila, i):
    '''
    Convierte la rotacion que está en formato de cadena en una lista de tuplas.
    '''
    por_rotar = fila[i].split(';')
    rotacion = []
    for coordenada in por_rotar:
        if coordenada[2] == '-' and coordenada[3].isdecimal():
            rotacion.append((int(coordenada[0]), -int(coordenada[3])))
        else:
            rotacion.append((int(coordenada[0]), int(coordenada[2])))
    return rotacion

def rotaciones(archivo):
    '''
    Lee el archivo de las piezas y devuelve un diccionarion con cada rotación como clave y valor.
    '''
    rotaciones_piezas = {}

    with open(archivo) as piezas:
        lector = csv.reader(piezas, delimiter=' ')
        for fila in lector:
            if fila[2] == 'Cubo':
                rotaciones_cubo = convertir_rotacion(fila, 0)
                rotaciones_piezas[f'{rotaciones_cubo}'] = rotaciones_cubo

            elif fila[3] == 'Z':
                rotacion_z_0 = convertir_rotacion(fila, 0)
                rotacion_z_1 = convertir_rotacion(fila, 1)

                rotaciones_piezas[f'{rotacion_z_0}'] = rotacion_z_1
                rotaciones_piezas[f'{rotacion_z_1}'] = rotacion_z_0
            
            elif fila[3] == 'S':
                rotacion_s_0 = convertir_rotacion(fila, 0)
                rotacion_s_1 = convertir_rotacion(fila, 1)

                rotaciones_piezas[f'{rotacion_s_0}'] = rotacion_s_1
                rotaciones_piezas[f'{rotacion_s_1}'] = rotacion_s_0
            
            elif fila[3] == 'I':
                rotacion_i_0 = convertir_rotacion(fila, 0)
                rotacion_i_1 = convertir_rotacion(fila, 1)

                rotaciones_piezas[f'{rotacion_i_0}'] = rotacion_i_1
                rotaciones_piezas[f'{rotacion_i_1}'] = rotacion_i_0
            
            elif fila[5] == 'L':
                rotacion_l_0 = convertir_rotacion(fila, 0)
                rotacion_l_1 = convertir_rotacion(fila, 1)
                rotacion_l_2 = convertir_rotacion(fila, 2)
                rotacion_l_3 = convertir_rotacion(fila, 3)

                rotaciones_piezas[f'{rotacion_l_0}'] = rotacion_l_1
                rotaciones_piezas[f'{rotacion_l_1}'] = rotacion_l_2
                rotaciones_piezas[f'{rotacion_l_2}'] = rotacion_l_3
                rotaciones_piezas[f'{rotacion_l_3}'] = rotacion_l_0

            
            elif fila[5] == '-L':
                rotacion_inversa_l_0 = convertir_rotacion(fila, 0)
                rotacion_inversa_l_1 = convertir_rotacion(fila, 1)
                rotacion_inversa_l_2 = convertir_rotacion(fila, 2)
                rotacion_inversa_l_3 = convertir_rotacion(fila, 3)

                rotaciones_piezas[f'{rotacion_inversa_l_0}'] = rotacion_inversa_l_1
                rotaciones_piezas[f'{rotacion_inversa_l_1}'] = rotacion_inversa_l_2
                rotaciones_piezas[f'{rotacion_inversa_l_2}'] = rotacion_inversa_l_3
                rotaciones_piezas[f'{rotacion_inversa_l_3}'] = rotacion_inversa_l_0
                
            elif fila[5] == 'T':
                rotacion_t_0 = convertir_rotacion(fila, 0)
                rotacion_t_1 = convertir_rotacion(fila, 1)
                rotacion_t_2 = convertir_rotacion(fila, 2)
                rotacion_t_3 = convertir_rotacion(fila, 3)

                rotaciones_piezas[f'{rotacion_t_0}'] = rotacion_t_1
                rotaciones_piezas[f'{rotacion_t_1}'] = rotacion_t_2
                rotaciones_piezas[f'{rotacion_t_2}'] = rotacion_t_3
                rotaciones_piezas[f'{rotacion_t_3}'] = rotacion_t_0

    piezas_iniciales = (rotaciones_cubo, rotacion_z_0, rotacion_s_0, rotacion_i_0, rotacion_l_0, rotacion_inversa_l_0, rotacion_t_0)
    return piezas_iniciales, rotaciones_piezas
