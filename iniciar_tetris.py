from asyncio.windows_events import NULL
import tetris
import interfaz_tetris
import teclas
import puntuaciones
import gamelib

TECLAS = teclas.identificar_tecla()

def inicializarTetris():
    gamelib.resize(650, 850)
    pieza_inicial = tetris.generar_pieza()
    juego = tetris.crear_juego(pieza_inicial)
    siguiente_pieza = tetris.generar_pieza()
    return juego, siguiente_pieza, 0

def dibujarInterfaz(juego, puntuacion, siguiente_pieza):
    gamelib.draw_begin()
    interfaz_tetris.dibujar_tablero(juego, puntuacion)
    interfaz_tetris.dibujar_pieza(juego)
    interfaz_tetris.dibujar_superficie(juego)
    interfaz_tetris.dibujar_siguiente_pieza(siguiente_pieza)
    gamelib.draw_end()

def manejadorDeEventos(juego, siguiente_pieza, puntuacion):
    pass

def gameOver(puntuacion):
    nombre = gamelib.input('Ingrese su nombre: ')
    if nombre == None:
        nombre = ''
    puntos_historicos = puntuaciones.agregar_puntuacion(nombre, puntuacion)
    return interfaz_tetris.intefazGameOver(nombre, puntuacion, puntos_historicos, TECLAS)


def gameloop():
    juego, siguiente_pieza, puntuacion = inicializarTetris()

    timer_bajar = interfaz_tetris.ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        # Dibujar la pantalla
        dibujarInterfaz(juego, puntuacion, siguiente_pieza)

        # manejadorDeEventos(juego, siguiente_pieza, puntuacion)
        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                # Actualizar el juego, según la tecla presionada
                tecla_presionada = TECLAS.get(event.key, None)
                if not tecla_presionada:
                    break
                if tecla_presionada == 'DERECHA':
                    juego = teclas.mover_derecha(juego)

                if tecla_presionada == 'IZQUIERDA':
                    juego = teclas.mover_izquierda(juego)

                if tecla_presionada == 'ROTAR':
                    juego = teclas.rotar(juego)

                if tecla_presionada == 'DESCENDER':
                    juego, hay_superficie = teclas.descender(
                        juego, siguiente_pieza, event)
                    if hay_superficie == True:
                        puntuacion += 15
                        siguiente_pieza = tetris.generar_pieza()

                if tecla_presionada == 'GUARDAR':
                    teclas.guardar(juego, puntuacion)

                if tecla_presionada == 'CARGAR':
                    juego, puntuacion = teclas.cargar(juego, puntuacion, event)
                
                if tecla_presionada == 'SALIR':
                    return

        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = interfaz_tetris.ESPERA_DESCENDER
            # Descender la pieza automáticamente
            juego, booleano = tetris.avanzar(juego, siguiente_pieza)
            if booleano == True:
                puntuacion += 15
                siguiente_pieza = tetris.generar_pieza() 

        if tetris.terminado(juego):
            if gameOver(puntuacion):
                juego, siguiente_pieza, puntuacion = inicializarTetris()
            else:
                return

def main():
    gameloop()

gamelib.init(main)
