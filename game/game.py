import numpy as np

class Board():
    def __init__(self, board = None, current_board = None) -> None:
        if board == None:
            self.board = np.zeros(81, np.short)   
            self.move_count = 0         
        else:
            self.board = board
            self.move_count = np.count_nonzero(board)

        self.current_board = -1 if current_board == None else current_board       

    def get_subboard(self, board: int, safe: bool = True):
        idx = 9 * board
        subboard = self.board[idx:idx+9]
        if safe:
            return np.copy(subboard)
        else:
            return subboard

    def subboard_winner(self, board: int) -> int | None:
        subboard = self.get_subboard(board, safe=True)
        open_spaces = np.count_nonzero(subboard)
        if open_spaces > 6:
            # Not enough moves on this board for a victory
            return None
        
        subboard = np.reshape(subboard, (3, 3))

        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
                return 1
            elif np.all(board[i, :] == -1) or np.all(board[:, i] == -1):
                return -1

        if np.all(np.diag(board) == 1) or np.all(np.diag(np.fliplr(board)) == 1):
            return 1
        elif np.all(np.diag(board) == -1) or np.all(np.diag(np.fliplr(board)) == -1):
            return -1

        # Check for ongoing game or draw
        if open_spaces > 0:
            # Game ongoing
            return None
        else:
            # Draw
            return 0
    
    def subboard_open(self, board: int) -> bool:
        subboard = self.get_subboard(board, safe=True)
        open_spaces = np.count_nonzero(subboard)
        if open_spaces > 6:
            # Not enough moves on this board for a victory
            return True
        
        subboard = np.reshape(subboard, (3, 3))

        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if abs(np.sum(board[i, :])) == 3 or abs(np.sum(board[:, i])) == 3:
                return False
            
        if abs(np.sum(board)) == 3 or abs(np.sum(np.fliplr(board))) == 3:
            return False

        # Check for ongoing game or draw
        if open_spaces > 0:
            # Game ongoing
            return True
        else:
            # Draw
            return False
   
    def turn(self):
        return self.move_count % 2

    def copy(self):
        return Board(np.copy(self.board))
    
    def move_to_idx(self, move: tuple[int]):
        return (9 * move[0]) + move[1]

    def is_move_legal(self, move: tuple[int]):
        idx = self.move_to_idx(move)

        # Is this square occupied already?
        if self.board[idx] != 0:
            return False
        # Is this move in the wrong board?
        elif self.current_board != -1 and move[0] != self.current_board:
            return False
        # Is this board already completed?
        elif self.current_board == -1 and not self.subboard_open(move[0]):
            return False
        
        return True
        

    def make_move(self, move: tuple[int], copy=False):
        if copy:
            new_board = self.copy()
            new_board.make_move(move)
            return new_board
        else:
            idx = self.move_to_idx(move)
            assert self.board[idx] == 0

            self.board[idx] = 1 if self.turn() == 0 else -1
            self.current_board = move[0]
            self.move_count += 1

            return self
