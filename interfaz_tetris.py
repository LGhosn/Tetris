from asyncio.windows_events import NULL
import tetris
import gamelib

ESPERA_DESCENDER = 8
ANCHO_BORDE = 20
ANCHO_TABLERO = 425
ALTO_TABLERO = 830
ANCHO_ALTO_CELDA = 45

def dibujar_tablero(juego, puntuacion):
    '''
    Dibuja el tablero conjunto a la interfaz de la siguiente pieza.
    '''
    gamelib.title('TETRIS')
    gamelib.draw_rectangle(ANCHO_BORDE, ANCHO_BORDE, ANCHO_TABLERO, ALTO_TABLERO, outline='#6C3483', fill='',width='4')
    gamelib.draw_text('-TETRIS-', ANCHO_TABLERO + 120, ALTO_TABLERO - 775, size='22', fill='#0BEAFA')

    for i in range(ANCHO_BORDE + ANCHO_ALTO_CELDA, ANCHO_TABLERO, ANCHO_ALTO_CELDA):
        gamelib.draw_line(i, ANCHO_BORDE, i, ALTO_TABLERO, fill='#BDC3C7', width=1)
    for j in range(ANCHO_BORDE + ANCHO_ALTO_CELDA, ALTO_TABLERO, ANCHO_ALTO_CELDA):
        gamelib.draw_line(ANCHO_BORDE, j, ANCHO_TABLERO, j, fill='#BDC3C7', width=1)
    
    gamelib.draw_text(f'Puntuacion: {puntuacion}',ANCHO_TABLERO + 120, 470, size='16', fill='red')
            
def dibujar_pieza(juego):
    '''
    Dibuja la pieza que esta cayendo.
    '''
    _, pieza = juego
    for x, y in pieza:
        x1, x2 = ANCHO_BORDE + 5 + (x * ANCHO_ALTO_CELDA), ANCHO_BORDE - 5 + ((x + 1) * ANCHO_ALTO_CELDA) 
        y1, y2 = ANCHO_BORDE + 5 + (y * ANCHO_ALTO_CELDA), ANCHO_BORDE - 5 + ((y + 1) * ANCHO_ALTO_CELDA)
        gamelib.draw_rectangle(x1, y1, x2, y2, fill='#00FDF9')

def dibujar_superficie(juego):
    '''
    Dibuja la superficie consolidada.
    '''
    superficie, _ = juego
    for x, y in superficie:
        x1, x2 = ANCHO_BORDE + 5 + (x * ANCHO_ALTO_CELDA), ANCHO_BORDE - 5 + ((x + 1) * ANCHO_ALTO_CELDA) 
        y1, y2 = ANCHO_BORDE + 5 + (y * ANCHO_ALTO_CELDA), ANCHO_BORDE - 5 + ((y + 1) * ANCHO_ALTO_CELDA)
        gamelib.draw_rectangle(x1, y1, x2, y2, fill='#8E8E8E')

def dibujar_siguiente_pieza(siguiente_pieza):
    '''
    Dibuja la siguiente pieza que va a caer.
    '''

    gamelib.draw_rectangle(ANCHO_TABLERO + 45, ANCHO_BORDE + 100, ANCHO_TABLERO + 195, ANCHO_BORDE + 280, outline='#28B463', fill='', width='2')

    for x, y in siguiente_pieza:
        x1, x2 = ANCHO_TABLERO + 55 + ((x + 1) * (ANCHO_ALTO_CELDA - 15)), ANCHO_TABLERO + 53 + ((x + 2) * (ANCHO_ALTO_CELDA - 15)) 
        y1, y2 = 155 + (y * (ANCHO_ALTO_CELDA - 15)), 153 + ((y + 1) * (ANCHO_ALTO_CELDA - 15))
        gamelib.draw_rectangle(x1, y1, x2, y2, fill='#C700FD')

def mostrar_puntuaciones(nombre, puntuacion, puntos_historicos, teclas):
    '''
    Dibuja la interfaz al terminar el juego
    '''
    while gamelib.loop(fps=30):
        gamelib.draw_begin()

        gamelib.draw_image('game_over.gif', 100, 20)
        gamelib.draw_text('TU PUNTUACION :', 650 // 2, 300, size='20')
        gamelib.draw_rectangle(0, 350, 650, 450, fill='#F4D03F', outline='#34495E')
        gamelib.draw_text(f'{nombre} : {puntuacion} pts', 650 // 2, 400, size='18', fill='#28B463')
        gamelib.draw_text('- - - RANKING - - -', 650 // 2, 500, size='20', fill='pink')
        gamelib.draw_text('"R" para volver a jugar',100, 20, size='10', fill='pink')
        gamelib.draw_text('"Esc" para salir',100, 40, size='10', fill='pink')
        
        y = 560
        x = 325 // 2
        posicion = 1
        for puntos, jugador in puntos_historicos:
            gamelib.draw_text(f'{posicion}.{jugador} : {puntos} pts', x, y, size='18', fill='#F1C40F')
            y += 60
            posicion += 1
            if y == 860:
                y = 560
                x = 487
        gamelib.draw_end()

        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                # Actualizar el juego, según la tecla presionada
                tecla_presionada = teclas.get(event.key, None)
                if not tecla_presionada:
                    break
                if tecla_presionada == 'REINICIAR':
                    return True                    

                if tecla_presionada == 'SALIR':
                    return False



def intefazGameOver(nombre, puntuacion, puntos_historicos, teclas):
    return mostrar_puntuaciones(nombre, puntuacion, puntos_historicos, teclas)
