import random, copy, os

# personajes
gato, raton = 'G', 'R'
winner = raton
personaje = 0

# ---------------- FUNCIONES ----------------

def limpiar_consola():
    if os.name == "nt": #para windows
        os.system("cls")
    else: #pal resto
        os.system("clear")

def crear_matriz(fila,columna):
    matriz =[]
    for i in range(fila):
        matriz.append([])
        for j in range(columna):
            matriz[i].append('*')
    return matriz

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))

def spawn_random(personaje, tablero): 
    while True:
        x = random.randint(0, len(tablero) - 1)
        y = random.randint(0, len(tablero[0]) - 1)
        if tablero[x][y] == '*':
            tablero[x][y] = personaje
            return tablero

def obtener_coords(tablero, personaje):
    for fila in range(len(tablero)):
        for col in range(len(tablero[0])):
            if tablero[fila][col] == personaje:
                return fila, col
    
def movimiento(direccion, personaje, tablero):
    x,y = obtener_coords(tablero, personaje)
    
    dx, dy = 0,0
    if direccion == 'w': dx = -1
    if direccion == 's': dx = 1
    if direccion == 'a': dy = -1
    if direccion == 'd': dy = 1
    if direccion == 'q': dx = -1; dy = -1
    if direccion == 'e': dx = -1; dy = 1
    if direccion == 'z': dx = 1; dy = -1
    if direccion == 'c': dx = 1; dy = 1

    nx, ny = x+dx, y+dy

    captura = False
    if 0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]):
        if tablero[nx][ny] == '*' or (personaje == gato and tablero[nx][ny] == raton):
            if personaje == gato and tablero[nx][ny] == raton:
                captura = True  #  gato comió al ratón
            tablero[nx][ny] = personaje
            tablero[x][y] = '*'

    return tablero, captura



def generar_movimientos(tablero, personaje):
    movimientos = []
    x,y = obtener_coords(tablero, personaje)
    direcciones = ['w','s','a','d','q','e','z','c']

    for d in direcciones:
        nx, ny = x, y
        if d == 'w': nx -= 1
        if d == 's': nx += 1
        if d == 'a': ny -= 1
        if d == 'd': ny += 1
        if d == 'q': nx -= 1; ny -= 1
        if d == 'e': nx -= 1; ny += 1
        if d == 'z': nx += 1; ny -= 1
        if d == 'c': nx += 1; ny += 1

        if 0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]):
            if tablero[nx][ny] == '*' or (personaje == gato and tablero[nx][ny] == raton):
                movimientos.append(d)
    return movimientos


def evaluar_estado(coords_gato, coords_raton, turnos_restantes):
    if coords_gato == coords_raton:
        return 100  # Gato gana
    if turnos_restantes <= 0:
        return -100  # Ratón gana
    return 0  # Ningún ganador todavía


# def heuristica(coords_gato, coords_raton):
#     # distancia Manhattan
#     distancia = abs(coords_gato[0] - coords_raton[0]) + abs(coords_gato[1] - coords_raton[1])
#     print(-distancia)
#     return -distancia   # cuanto mas alta la heurística (menos negativa), mejor para el gato
def heuristica(coords_gato, coords_raton):
    dx = abs(coords_gato[0] - coords_raton[0])
    dy = abs(coords_gato[1] - coords_raton[1])
    return -max(dx, dy)  # distancia Chebyshev

     

def minimax(tablero, coords_gato, coords_raton, turnos_restantes, maximizando_gato, profundidad, max_profundidad):
    # 1) chequeo victorias
    estado = evaluar_estado(coords_gato, coords_raton, turnos_restantes)
    if estado == 100 or estado == -100:
        return estado, None

    # 2) si llega a prof maxima -> usar heuristica
    if profundidad == max_profundidad:
        return heuristica(coords_gato, coords_raton), None

    # 3) ramas
    if maximizando_gato:
        mejor_valor = -float('inf')
        mejor_mov = None
        for mov in generar_movimientos(tablero, gato):
            copia = copy.deepcopy(tablero)
            copia, captura = movimiento(mov, gato, copia)

            # Si el gato capturaes victoria 
            if captura:
                return 100, mov

            nuevas_coords_gato = obtener_coords(copia, gato)
            nuevas_coords_raton = obtener_coords(copia, raton)
            valor, _ = minimax(copia, nuevas_coords_gato, nuevas_coords_raton,
                               turnos_restantes-1, False, profundidad+1, max_profundidad)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_valor, mejor_mov

    else:  # turno del ratón (minimizador)
        peor_valor = float('inf')
        peor_mov = None
        for mov in generar_movimientos(tablero, raton):
            copia = copy.deepcopy(tablero)
            copia, _ = movimiento(mov, raton, copia)
            nuevas_coords_raton = obtener_coords(copia, raton)
            nuevas_coords_gato = obtener_coords(copia, gato)
            valor, _ = minimax(copia, nuevas_coords_gato, nuevas_coords_raton,
                               turnos_restantes-1, True, profundidad+1, max_profundidad)
            if valor < peor_valor:
                peor_valor = valor
                peor_mov = mov
        return peor_valor, peor_mov




# ---------------- JUEGO ----------------
print('Configuraciones iniciales')
fila, columna = int(input('ingrese las filas: ')), int(input('ingrese las columnas: '))
tablero = crear_matriz(fila,columna)
spawns = input('spawn aleatorio? (s/n)')
if spawns == 'n':
    tablero[0][0] = gato
    tablero[fila-1][columna-1] = raton
if spawns == 's':
    spawn_random(raton, tablero)
    spawn_random(gato, tablero)
coords_gato = obtener_coords(tablero, gato)
coords_raton = obtener_coords(tablero, raton)

print(f'Bienvenido al juego del gato y el raton')
print(f'1. Jugar 1 vs IA')
print(f'2. IA vs IA')
print(f'3. 1v1 sin camisa')
modo_juego = int(input('Seleccione la opcion: '))
if modo_juego == 1:
    print(f'Que queres ser?')
    print(f'1. Gato\n2. Raton\nEnter = random')    
    personaje = int(input() or 0)
    if personaje == 0:
        personaje = random.randint(1,2)
        print(f'vas a ser {'gato' if personaje ==1 else 'raton'}')
    max_profundidad = int(input('ingrese la inteligencia del bot (1-5): '))
    max_profundidad_gato, max_profundidad_raton = max_profundidad, max_profundidad

if modo_juego == 2:
    max_profundidad_raton = int(input('ingrese la inteligencia del raton (1-5): '))
    max_profundidad_gato = int(input('ingrese la inteligencia del gato (1-5): '))
    


turnos_a_jugar = int(input('Ingrese la cantidad de turnos: '))
turno_actual = 0

while turno_actual < turnos_a_jugar:
    if modo_juego in [1, 3]:
        limpiar_consola()

    print(f'TURNO {turno_actual+1}')

    # --- Turno Gato ---
    if (modo_juego == 1 and personaje == 1) or modo_juego == 3:  # Gato humano
        print('Movete GATITA')
        mostrar_tablero(tablero)
        direccion = input('a donde nos movemos (w/a/s/d) y (q,e,z,c) diagonales: ')
        tablero, _ = movimiento(direccion, gato, tablero)
    else:  # IA Gato
        print('Gato juega')
        _, mejor_mov = minimax(tablero, coords_gato, coords_raton,
                               turnos_a_jugar - turno_actual, True, 0, max_profundidad_gato)
        if mejor_mov:
            tablero, _ = movimiento(mejor_mov, gato, tablero)

    # Actualizar coordenadas
    coords_gato = obtener_coords(tablero, gato)

    # Verificar si el gato atrapo al ratón
    if evaluar_estado(coords_gato, coords_raton, turnos_a_jugar - turno_actual) == 100:
        winner = gato
        break

    # --- Turno Raton ---
    if (modo_juego == 1 and personaje == 2) or modo_juego == 3:  # Ratón humano
        print('Te toca RATA')
        mostrar_tablero(tablero)
        direccion = input('a donde nos movemos (w/a/s/d) y (q,e,z,c) diagonales: ')
        tablero, _ = movimiento(direccion, raton, tablero)
    else:  # IA Raton
        print('Ratón juega')
        _, mejor_mov = minimax(tablero, coords_gato, coords_raton,
                               turnos_a_jugar - turno_actual, False, 0, max_profundidad_raton)
        if mejor_mov:
            tablero, _ = movimiento(mejor_mov, raton, tablero)

    # Actualizar coordenadas
    coords_gato = obtener_coords(tablero, gato)
    coords_raton = obtener_coords(tablero, raton)

    mostrar_tablero(tablero)

    # Verificar si el ratón fue atrapado
    if evaluar_estado(coords_gato, coords_raton, turnos_a_jugar - turno_actual) == 100:
        winner = gato
        break

    turno_actual += 1



# ---------------- RESULTADO ----------------
if modo_juego == 1 or modo_juego ==3:
    limpiar_consola()
print(f'JUEGO TERMINADO')
mostrar_tablero(tablero)
if winner == gato:

    print("""
     _._     _,-'""`-._
    (,-.`._,'(       |\`-/|
        `-.-' \ )-`( , o o)
              `-    \`_`"'-
    """)
    print('gato wins')
else:
    print('''
            _     _
            \).-.(/
             (O O) (
             />@<\ )
    ___ ____(\ _ /)__    _______
 .-" _ "     ** **   "=-"  \    \   
|   ( )     _           o   :.   .
|    "     ( )     ()       ::   :
|_          "          ..   ::   :
  )     Sencillo ()   (  )  :|   |
|"    ()     para el   ""   :|   |
|   O        o .-.  roedor  ./   /
\____.--._____(---)___(-)__//___/


    ''')
    print('gano el raton')
