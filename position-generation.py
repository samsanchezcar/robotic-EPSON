import sys
sys.setrecursionlimit(10000)

# --- 1. Configuración del Tablero ---
ROWS = 5
COLS = 6
TOTAL_SQUARES = ROWS * COLS  # 30

# Coordenadas iniciales (fila, columna)
START_H1 = (0, 5)  # H1 (Casilla 1): Esquina superior derecha
START_H2 = (4, 0)  # H2 (Casilla 30): Esquina inferior izquierda

# Movimientos del "caballo"
MOVES_ROW = [-2, -2, -1, -1, 1, 1, 2, 2]
MOVES_COL = [-1, 1, -2, 2, -2, 2, -1, 1]


# --- Utilidades ---
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def is_free_for_piece(r, c, board_piece, other_pos):
    """
    Verifica que (r,c) no haya sido visitada por esta pieza
    y que no sea la posición actual de la otra pieza (evita colisión).
    """
    if not in_bounds(r, c):
        return False
    if board_piece[r][c] != 0:
        return False
    if other_pos is not None and (r, c) == other_pos:
        return False
    return True

def count_onward_moves_for_piece(r, c, board_piece, other_pos):
    """Cuenta movimientos posibles desde (r,c) para la heurística Warnsdorff"""
    cnt = 0
    for i in range(8):
        nr = r + MOVES_ROW[i]
        nc = c + MOVES_COL[i]
        if is_free_for_piece(nr, nc, board_piece, other_pos):
            cnt += 1
    return cnt

def get_valid_moves_for_piece(r, c, board_piece, other_pos):
    """
    Devuelve lista ordenada (heurística Warnsdorff) de (onward_count, nr, nc)
    para la pieza cuya tabla de visitas es board_piece, evitando other_pos.
    """
    moves = []
    for i in range(8):
        nr = r + MOVES_ROW[i]
        nc = c + MOVES_COL[i]
        if is_free_for_piece(nr, nc, board_piece, other_pos):
            onward = count_onward_moves_for_piece(nr, nc, board_piece, other_pos)
            moves.append((onward, nr, nc))
    moves.sort()  # menor onward primero
    return moves


# --- Algoritmo recursivo que hace recorrer a ambos huevo 30 casillas cada uno ---
def solve_both_knights(h1_pos, h2_pos, turn, board_h1, board_h2, steps_h1, steps_h2):
    """
    - h1_pos, h2_pos: posiciones actuales
    - turn: 1 (mueve H1) o 2 (mueve H2)
    - board_h1, board_h2: tableros de visitas (0 = no visitada, >0 = paso)
    - steps_h1, steps_h2: contadores de pasos dados por cada huevo (1..30)
    """
    # Caso éxito: ambos han visitado las 30 casillas
    if steps_h1 == TOTAL_SQUARES and steps_h2 == TOTAL_SQUARES:
        return True

    if turn == 1:
        current_pos = h1_pos
        board_current = board_h1
        other_pos = h2_pos
        current_steps = steps_h1
    else:
        current_pos = h2_pos
        board_current = board_h2
        other_pos = h1_pos
        current_steps = steps_h2

    valid_moves = get_valid_moves_for_piece(current_pos[0], current_pos[1], board_current, other_pos)

    # Si no hay movimientos válidos y no estamos aún en objetivo -> fallo
    if not valid_moves:
        return False

    for _, nr, nc in valid_moves:
        # asignamos siguiente paso para la pieza actual
        next_step = current_steps + 1
        board_current[nr][nc] = next_step

        if turn == 1:
            # H1 movió a (nr,nc)
            new_h1 = (nr, nc)
            new_h2 = h2_pos
            if solve_both_knights(new_h1, new_h2, 2, board_h1, board_h2, next_step, steps_h2):
                return True
        else:
            # H2 movió a (nr,nc)
            new_h1 = h1_pos
            new_h2 = (nr, nc)
            if solve_both_knights(new_h1, new_h2, 1, board_h1, board_h2, steps_h1, next_step):
                return True

        # backtrack
        board_current[nr][nc] = 0

    return False


# --- Funciones de impresión y ejecución ---
def print_boards(board_h1, board_h2):
    print("Tablero: pasos de H1 (0 = no visitado)")
    print("------------------------------------")
    for r in board_h1:
        print(" ".join(f"{x:2d}" for x in r))
    print("\nTablero: pasos de H2 (0 = no visitado)")
    print("------------------------------------")
    for r in board_h2:
        print(" ".join(f"{x:2d}" for x in r))
    print("\nNotas:")
    print(" - Cada tablero muestra el orden de visita de ese huevo (1..30).")
    print(" - En todo momento evitamos que ambos ocupen la misma casilla.")


def run_solver():
    # crear tableros de visita separados
    board_h1 = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    board_h2 = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Colocar posiciones iniciales como paso 1 para ambos huevos
    board_h1[START_H1[0]][START_H1[1]] = 1
    board_h2[START_H2[0]][START_H2[1]] = 1

    # pasos actuales
    steps_h1 = 1
    steps_h2 = 1

    # Empezamos con el turno de H1 (puedes revertir si prefieres)
    if solve_both_knights(START_H1, START_H2, 1, board_h1, board_h2, steps_h1, steps_h2):
        print("¡Solución encontrada! (cada huevo visitó 30 casillas)")
        print_boards(board_h1, board_h2)
    else:
        print("No se encontró solución con la heurística/orden actual.")

if __name__ == "__main__":
    run_solver()
