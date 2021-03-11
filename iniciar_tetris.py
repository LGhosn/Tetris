import tetris
import interfaz_tetris
import teclas
import puntuaciones
import gamelib

TECLAS = teclas.identificar_tecla()

def main():
    # Inicializar el estado del juego
    gamelib.resize(650, 850)
    pieza_inicial = tetris.generar_pieza()
    juego = tetris.crear_juego(pieza_inicial)
    siguiente_pieza = tetris.generar_pieza()
    puntuacion = 0

    timer_bajar = interfaz_tetris.ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        # Dibujar la pantalla
        interfaz_tetris.dibujar_tablero(juego, puntuacion)
        interfaz_tetris.dibujar_pieza(juego)
        interfaz_tetris.dibujar_superficie(juego)
        interfaz_tetris.dibujar_siguiente_pieza(siguiente_pieza)
        gamelib.draw_end()

        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
            # Actualizar el juego, según la tecla presionada
            if TECLAS[event.key] == 'DERECHA':
                juego = teclas.mover_derecha(juego)
            
            if TECLAS[event.key] == 'IZQUIERDA':
                juego = teclas.mover_izquierda(juego)
            
            if TECLAS[event.key] == 'ROTAR':
                juego = teclas.rotar(juego)

            if TECLAS[event.key] == 'DESCENDER':
                juego, hay_superficie = teclas.descender(juego, siguiente_pieza, event)
                if hay_superficie == True:
                    puntuacion += 15
                    siguiente_pieza = tetris.generar_pieza()
            
            if TECLAS[event.key] == 'GUARDAR':
                teclas.guardar(juego, puntuacion)
            
            if TECLAS[event.key] == 'CARGAR':
                juego, puntuacion = teclas.cargar(juego, puntuacion, event)

            if TECLAS[event.key] == 'SALIR':
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
            nombre = gamelib.input('Ingrese su nombre: ')
            if nombre == None:
                nombre = ''
            puntos_historicos = puntuaciones.agregar_puntuacion(nombre, puntuacion)
            interfaz_tetris.mostrar_puntuaciones(nombre, puntuacion, puntos_historicos)

gamelib.init(main)
