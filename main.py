import random

ROWS = 6
COLS = 7
PLAYER_1 = 1
PLAYER_2 = 2
EMPTY = 0
PLAYER_1_SYMBOL = "X"
PLAYER_2_SYMBOL = "O"
EMPTY_SYMBOL = " "
SYMBOLS = {EMPTY: EMPTY_SYMBOL, PLAYER_1: PLAYER_1_SYMBOL, PLAYER_2: PLAYER_2_SYMBOL}

def create_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print("|" + "|".join(SYMBOLS[cell] for cell in row) + "|")
    print("-" * 15)
    print(" 1 2 3 4 5 6 7 ")

def get_valid_columns(board):
    return [col for col in range(COLS) if board[0][col] == EMPTY]

def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    raise ValueError(f"Spalte {col + 1} ist voll.")

def is_winning_move(board, piece):
    # Horizontale, vertikale und diagonale Gewinnbedingungen prüfen
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == piece for i in range(4)):
                return True
    return False

def evaluate_window(window, piece, opponent_piece):
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def evaluate_position(board, piece):
    opponent_piece = PLAYER_2 if piece == PLAYER_1 else PLAYER_1
    score = 0
    # Horizontale, vertikale und diagonale Fenster durchgehen
    for r in range(ROWS):
        for c in range(COLS - 3):
            score += evaluate_window(board[r][c:c + 4], piece, opponent_piece)
    for c in range(COLS):
        for r in range(ROWS - 3):
            score += evaluate_window([board[r + i][c] for i in range(4)], piece, opponent_piece)

    # Diagonale von oben links nach unten rechts
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += evaluate_window([board[r + i][c + i] for i in range(4)], piece, opponent_piece)

    # Diagonale von unten links nach oben rechts
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += evaluate_window([board[r - i][c + i] for i in range(4)], piece, opponent_piece)

    return score

def minimax(board, depth, maximizing_player, piece, alpha=float('-inf'), beta=float('inf')):
    # Abbruchbedingung: Tiefe erreicht oder ein Gewinnzug gefunden
    if depth == 0 or is_winning_move(board, piece):
        return evaluate_position(board, piece)

    valid_columns = get_valid_columns(board)
    best_score = float('-inf') if maximizing_player else float('inf')

    for col in valid_columns:
        row = get_next_open_row(board, col)
        temp_board = [row.copy() for row in board]
        temp_board[row][col] = piece if maximizing_player else (PLAYER_1 if piece == PLAYER_2 else PLAYER_2)

        score = minimax(temp_board, depth - 1, not maximizing_player, piece, alpha, beta)

        if maximizing_player:
            best_score = max(best_score, score)
            alpha = max(alpha, score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, score)

        if beta <= alpha:
            break

    return best_score

def pick_best_move(board, piece, depth=4):
    valid_columns = get_valid_columns(board)
    best_score = float('-inf')
    best_col = random.choice(valid_columns)

    for col in valid_columns:
        row = get_next_open_row(board, col)
        temp_board = [row.copy() for row in board]
        temp_board[row][col] = piece
        score = minimax(temp_board, depth, False, piece)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def block_player_win(board, piece):
    opponent_piece = PLAYER_2 if piece == PLAYER_1 else PLAYER_1
    potential_block = None

    for col in get_valid_columns(board):
        row = get_next_open_row(board, col)
        temp_board = [row.copy() for row in board]
        temp_board[row][col] = opponent_piece
        if is_winning_move(temp_board, opponent_piece):
            potential_block = col
            break

    if potential_block is not None:
        if random.random() < 0.8:
            return potential_block
    return None

def ai_make_move(board, piece):
    block_move = block_player_win(board, piece)
    if block_move is not None:
        return block_move
    return pick_best_move(board, piece)

def player_make_move(board, turn):
    current_player = PLAYER_1 if turn % 2 == 0 else PLAYER_2
    while True:
        try:
            col = int(input(f"Spieler {current_player}, wähle eine Spalte (1-7): ")) - 1
            if col in get_valid_columns(board):
                break
            print("Ungültige Eingabe. Bitte eine gültige Spalte wählen.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

    return col

def play_game(mode):
    board = create_board()
    turn = 0
    print_board(board)

    while True:
        if mode == "1" and turn % 2 == 1:
            col = ai_make_move(board, PLAYER_2)
        else:
            col = player_make_move(board, turn)

        row = get_next_open_row(board, col)
        piece = PLAYER_1 if turn % 2 == 0 else PLAYER_2
        board[row][col] = piece
        print_board(board)

        if is_winning_move(board, piece):
            print(f"{'Computer' if mode == '1' and turn % 2 == 1 else f'Spieler {piece}'} gewinnt!")
            break
        if turn == 41:
            print("Unentschieden!")
            break

        turn += 1

def main_menu():
    while True:
        print("\nHauptmenü:")
        print("1. Einzelspieler (gegen den Computer)")
        print("2. Multiplayer (2 Spieler)")
        print("3. Beenden")
        mode = input("Bitte Modus auswählen (1, 2 oder 3): ")
        if mode == "1":
            play_game(mode)
        elif mode == "2":
            play_game(mode)
        elif mode == "3":
            print("Spiel beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte 1, 2 oder 3 wählen.")

main_menu()