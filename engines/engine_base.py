from game.board import Board

class BaseEngine():
    def __init__(self) -> None:
        # Engine Name
        self.name = "Default Engine Name"
        # Your name
        self.player = "Nobody"        
        
        # Include any other metadata or variables you want in your init

    # Must be overridden with your algo
    def best_move(self, board: Board, time_limit: float) -> tuple[tuple[int], dict]:
        """
        Finds the best move from the given board and returns it, along with an optional metadata dict
        """
        raise Exception(f"{self.name}: best_move() is not implemented!")
    
