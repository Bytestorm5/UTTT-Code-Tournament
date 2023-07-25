from game.board import Board

from engines.engine_base import BaseEngine
from engines.sample import SampleEngine as Player1
from engines.secret import SecretEngine as Player2

import time
import requests
import sys
import traceback

# Some limits on how long an engine can think for.
# Most engines should stop by the soft limit, going beyond the hard limit forfeits the game
TIME_SOFT_LIMIT = 90
TIME_HARD_LIMIT = 100

def send_board(input_string):
    endpoint_url = 'http://localhost:5000/update_board'  # Replace with the actual endpoint URL
    data = {'board_repr': input_string}

    try:
        response = requests.post(endpoint_url, data=data)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def run_game(p1: BaseEngine, p2: BaseEngine, game_num: int = -1, update_site: bool = True) -> int:
    board = Board()

    bonus_time = 0

    # Didn't feel like writing this every time
    def soft_limit():
        return TIME_SOFT_LIMIT + bonus_time
    def hard_limit():
        return TIME_HARD_LIMIT + bonus_time

    while board.winner() == None:
        symbol = 'X' if board.turn() == 0 else 'O'
        current_player = p1 if board.turn() == 0 else p2
        
        # X; Player 1
        print(f"[Game {game_num}]: {current_player.name} ({symbol}) is thinking...")
        
        board_copy = board.copy() # Done before timer starts to reduce overhead
        try:
            start = time.time()
            move = current_player.best_move(board_copy, soft_limit())
            time_taken = time.time() - start

            board.make_move(move[0]) # In case the player plays an illegal move
        except Exception:
            print(f"[Game {game_num}]: {current_player.name} ({symbol}) has crashed with the following error:")
            traceback.print_exc()
            return -1 if board.turn() == 1 else 1
        print(f"[Game {game_num}]: {current_player.name} ({symbol}) has decided on the move {move} in {time_taken}s")

        if time_taken > hard_limit():
            print(f"[Game {game_num}]: {current_player.name} ({symbol}) took too long ({time_taken} > {hard_limit()}) and has lost the game.")
            return board.turn() * -1
        elif time_taken > soft_limit():
            bonus_time = 1.5 * (time_taken - soft_limit())
            print(f"[Game {game_num}]: {current_player.name} ({symbol}) exceeded the soft time limit ({time_taken} > {soft_limit()}); {bonus_time}s awarded to opponent.")
        else:
            bonus_time = 0
        
        print(board)

        send_board(repr(board))
    
    winner = p1 if board.turn() == 1 else p2 # Inverted since the turn will rollover regardless of victory
    victory_status = board.winner()

    if victory_status == 0:
        print(f"[Game {game_num}]: Game has ended in a draw.")
    else:
        print(f"[Game {game_num}]: {winner.name} ({winner.player}) has won Game {game_num}")

    return board.winner()

# Creates a new 
def getPlayer1(game_num) -> BaseEngine:
    engine = Player1(0) # Any input args provided by player    
    #engine.name += " (X)" # temp- just to differentiate
    return engine
def getPlayer2(game_num) -> BaseEngine:
    engine = Player2(game_num) # Any input args provided by player    
    #engine.name += " (O)" # temp- just to differentiate
    return engine

if __name__ == "__main__":    
    UPDATE_SITE = True
    if '-q' in sys.argv or '--quiet' in sys.argv:
        UPDATE_SITE = False


    points = {
        1: 0,
        -1: 0
    }
    total_games = 0

    def update_points(victory_status: int, flipped: bool):
        if victory_status in points:
            points[victory_status * (1 + (-2 * int(flipped)))] += 1
        else: # Draw
            points[1] += 0.5
            points[-1] += 0.5

        p1 = getPlayer1(total_games)
        p2 = getPlayer2(total_games)

        p1 = f"{p1.name} ({p1.player})"
        p2 = f"{p2.name} ({p2.player})"

        print(f"Scoreboard:\n - {p1}: {points[1]}\n - {p2}: {points[-1]}")

    def run_game_pair():
        global total_games
        game1 = run_game(getPlayer1(total_games), getPlayer2(total_games), total_games, UPDATE_SITE)
        update_points(game1, False)
        total_games += 1

        game2 = run_game(getPlayer2(total_games), getPlayer1(total_games), total_games, UPDATE_SITE)
        total_games += 1
        update_points(game2, True)

    def point_diff():
        return abs(points[1] - points[-1])
    
    for _ in range(5): # 10 games
        run_game_pair()

    if point_diff() >= 2:        
        if points[1] > points[-1]:
            player = getPlayer1(total_games)
        else:
            player = getPlayer2(total_games)
        print(f"[Master]: {player.name} ({player.player}) has won!")
        exit()
    else:
        print("--- Entering Phase 2; 1 pt tolerance ---")

    for _ in range(5): # 10 games
        run_game_pair()

    if point_diff() >= 1:        
        if points[1] > points[-1]:
            player = getPlayer1(total_games)
        else:
            player = getPlayer2(total_games)
        print(f"[Master]: {player.name} ({player.player}) has won!")
        exit()
    else:
        print("--- Entering Phase 3; Time Trouble ---")
        TIME_SOFT_LIMIT /= 4
        TIME_HARD_LIMIT /= 4
    
    for _ in range(5): # 10 games
        run_game_pair()
    
    if point_diff() >= 1:        
        if points[1] > points[-1]:
            player = getPlayer1(total_games)
        else:
            player = getPlayer2(total_games)
        print(f"[Master]: {player.name} ({player.player}) has won!")
        exit()
    else:
        print(f"[Master]: The match is a draw! Figure out what to do")