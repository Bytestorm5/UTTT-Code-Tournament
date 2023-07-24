# This is where unit tests for the board go
# Should NEVER be imported, this should purely be run as a standalone script to make sure the board is working properly

from board import Board
import time
import random

board = Board()

boards = []

start = time.time()
i = 0
for _ in range(1000):
    moves = list(board.get_legal_moves())
    if len(moves) == 0:
        break
    move = random.choice(moves)        
    board.make_move(move)
    boards.append(board.copy())
    i += 1
avg_time = (time.time() - start) / i
print(boards)
print(board)
print(f"Avg. Copy Time: {avg_time} over {i}")
