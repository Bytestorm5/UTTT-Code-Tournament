from engines.engine_base import BaseEngine
from game.board import Board

import random

class SampleEngine(BaseEngine):
    def __init__(self, board_start: int) -> None:
        self.name = "Sample Engine"
        self.player = "Kamil*"
        
        self.total_boards_evaluated = board_start
    
    def best_move(self, board: Board, time_limit: float) -> tuple[tuple[int], dict]:
        """
        Finds the best move from the given board and returns it, along with an optional metadata dict
        """
        board_count = 0
        moves = list(board.get_legal_moves())
        selected_move = 0
        while random.randint(0, 10) != 1:
            selected_move = random.randint(0, len(moves)-1)
            board_count += 1
        
        self.total_boards_evaluated += board_count

        return moves[selected_move], {'boards evaluated': board_count, 'total boards': self.total_boards_evaluated}
