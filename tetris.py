import piezas
import random

ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6
ARCHIVO_PIEZA = 'piezas.txt'

PIEZAS,ROTACIONES = piezas.rotaciones(ARCHIVO_PIEZA)

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if not pieza:
        return random.choice(PIEZAS)
    return PIEZAS[pieza]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y).
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = []

    for coordenada_x, coordenada_y in pieza:
        pieza_trasladada.append((coordenada_x + dx, coordenada_y + dy))

    return tuple(pieza_trasladada)

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de
    sus posiciones superiores es 0 (cero).
    """
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)
    superficie = []

    return superficie, pieza_centrada

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return ANCHO_JUEGO, ALTO_JUEGO

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    _, pieza_centrada = juego

    return pieza_centrada

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    superficie, _= juego

    return (x, y) in superficie

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    _, pieza_centrada = juego

    pieza_movida = trasladar_pieza(pieza_centrada, direccion, 0)

    for coordenada_x, coordenada_y in pieza_movida:
        if coordenada_x < 0 or coordenada_x >= ANCHO_JUEGO or hay_superficie(juego, coordenada_x, coordenada_y):
            return juego

    return _, pieza_movida

# ****** FUNCIONES AUXILIARES PARA AVANZAR ******
def hay_que_consolidar_pieza(juego, pieza_descendida):
    ''' Evalua y devuelve si hay que consolidar la pieza que baja ya sea porque llegó
        al final del tablero o porque hay otra superficie consolidada.'''

    for coordenada_x, coordenada_y in pieza_descendida:
        if coordenada_y >= ALTO_JUEGO or hay_superficie(juego, coordenada_x, coordenada_y):
            return True
    return False

def eliminar_filas(juego):
    '''Elimina todas las filas completas que hay en el juego.
        Devuelve las filas que hay que bajar.'''

    superficie, _ = juego

    filas_por_bajar = []
    for y in range(ALTO_JUEGO):
        fila_completa = []
        for x in range(ANCHO_JUEGO):
            if hay_superficie(juego, x, y):
                fila_completa.append((x,y))

        if len(fila_completa) == ANCHO_JUEGO:
            filas_por_bajar.append(y)
            for coordenada in fila_completa:
                superficie.remove(coordenada)

    return filas_por_bajar

def bajar_filas_eliminadas(juego, nueva_pieza, filas_por_bajar):
    '''Baja todas las filas que "eliminar_filas(juego)" eliminó.
        Devuelve una un nuevo estado del juego.'''

    superficie, _ = juego

    nueva_superficie = []
    for coordenada_x, coordenada_y in superficie:
        if coordenada_y < max(filas_por_bajar):
            nueva_superficie.append((coordenada_x, coordenada_y + len(filas_por_bajar)))
        else:
            nueva_superficie.append((coordenada_x, coordenada_y))

    return nueva_superficie, nueva_pieza

def consolidar_pieza(juego, pieza_descendida, siguiente_pieza):
    '''Consolida la pieza y elimina filas si es necesario.
        Si se eliminan filas devuelve un nuevo estado del juego
        considerando lo menciando. Sino devuelve otro estado de juego
        con la misma superficie inicial.
        '''

    superficie, _ = juego

    nueva_pieza = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)

    for coordenadas in pieza_actual(juego):
        superficie.append(coordenadas)

    filas_por_bajar = eliminar_filas(juego)

    if len(filas_por_bajar) > 0:
            return bajar_filas_eliminadas(juego, nueva_pieza, filas_por_bajar)


    return superficie, nueva_pieza

# ***********************************************

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.

    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).

    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar
    completamente en la grilla para poder seguir jugando, si al intentar
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada,
    se debe devolver el mismo juego que se recibió.
    """
    superficie, _ = juego

    pieza_descendida = trasladar_pieza(pieza_actual(juego), 0, 1)

    if terminado(juego):
        return juego, False

    if hay_que_consolidar_pieza(juego, pieza_descendida):

        superficie, nueva_pieza = consolidar_pieza(juego, pieza_descendida, siguiente_pieza)

        juego_nuevo = superficie, nueva_pieza
        return juego_nuevo, True

    juego_nuevo = superficie, pieza_descendida
    return juego_nuevo, False

def rotar(juego):
    '''
    Recibe la pieza actual del juego y en caso de ser posible devuelve la pieza rotada.
    '''
    _, pieza_actual = juego

    rotar_pieza = sorted(pieza_actual)

    primer_coordenada_x, primer_coordenada_y = rotar_pieza[0]

    for i in range(len(rotar_pieza)):
        rotar_pieza[i] = ((rotar_pieza[i][0] - primer_coordenada_x, rotar_pieza[i][1] - primer_coordenada_y))

    siguiente_rotacion = ROTACIONES[f'{rotar_pieza}']

    for l in range(len(siguiente_rotacion)):
        rotar_pieza[l] = ((siguiente_rotacion[l][0] + primer_coordenada_x, siguiente_rotacion[l][1] + primer_coordenada_y))
    
    for coordenada_x, coordenada_y in rotar_pieza:
        if hay_superficie(juego, coordenada_x, coordenada_y) or ANCHO_JUEGO <= coordenada_x or ALTO_JUEGO <= coordenada_y:
            return _, pieza_actual

    return _, rotar_pieza


def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    for coordenada_x, coordenada_y in pieza_actual(juego):
        if hay_superficie(juego, coordenada_x, coordenada_y):
            return True
    return False
