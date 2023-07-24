import numpy as np

class Board():
    def __init__(self, board: np.ndarray = None, current_board: int | None = None) -> None:
        """
        Set up an Ultimate Tic-Tac-Toe Board.

        Args:
            board (np.ndarray, optional): An array of 81 numbers representing the board. For each square, -1 represents O, 0 represents a blank space, and 1 represents X
            current_board (int | None, optional): Defines which board the current player must play on. If the current player may play any board, this should be None.

        Examples:
            >>> Board()
            Output: The starting position of a UTTT game.
        """
        if board == None:
            self.board = np.zeros(81, np.short)   
            self.move_count = 0         
        else:
            self.board = board
            self.move_count = np.count_nonzero(board)

        self.current_board = -1 if current_board == None else current_board       

    def get_subboard(self, board: int, safe: bool = True) -> np.ndarray:
        """
        Get a sub-board at the given index

        Args:
            board (int): The index of the sub-board to get.
            safe (bool, optional): Whether to get a "safe" version of the sub-board or not. An unsafe board allows you to make edits to the actual board by editing the sub-board. A safe board will not carry over any changes.
        
        Returns:
            type: An array of 9 numbers represting a sub-board.
        """
        idx = 9 * board
        subboard = self.board[idx:idx+9]
        if safe:
            return np.copy(subboard)
        else:
            return subboard

    def subboard_winner(self, board: int) -> int | None:
        """
        Determines if a sub-board has been won, drawn, or is still ongoing.

        Args:
            board (int): The index of the board to check.
        
        Returns:
            type: -1 if O has won, 1 if X has won, and 0 if it is a draw. Returns None if the game is ongoing.
        """
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
        """
        Determines if moves can be played on a specific sub-board.

        """
        subboard = self.get_subboard(board, safe=True)
        occupied_spaces = np.count_nonzero(subboard)
        if occupied_spaces < 3:
            # Not enough moves on this board for a victory
            return True
        
        subboard = np.reshape(subboard, (3, 3))

        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if abs(np.sum(subboard[i, :])) == 3 or abs(np.sum(subboard[:, i])) == 3:
                return False
            
        if abs(np.sum(np.diag(subboard))) == 3 or abs(np.sum(np.diag(np.fliplr(subboard)))) == 3:
            return False

        # Check for ongoing game or draw
        if occupied_spaces < 9:
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

            self.board[idx] = 1 - (2 * self.turn())
            self.current_board = move[1]
            self.move_count += 1

            return self
        
    def __str__(self) -> str:
        out_str = ""
        symbol_map = {
            1: 'X',
            0: '.',
            -1: 'O'  
        }
        # Do not do what I'm about to do if you need any amount of performance
        nested_boards = []
        for i in range(9):
            sboard = self.get_subboard(i)
            rep = []
            for square in sboard:
                rep.append(symbol_map[square])
            nested_boards.append(rep)

        for i in [0, 3, 6]:
            # i is Board index
            for j in [0, 3, 6]:
            # j is Square index
                for k in range(3):
                    out_str += f"{nested_boards[k+i][0+j]} {nested_boards[k+i][1+j]} {nested_boards[k+i][2+j]}"
                    if k != 2:
                        out_str += ' | '
                out_str += '\n'
            out_str += '---------------------\n'

        return out_str

    def __repr__(self) -> str:
        out_str = ""
        for n in self.board:
            out_str += str(int(n)) + " "
            
        out_str += str(self.current_board)
        return out_str

if __name__ == "__main__":
    board = Board()

    print(str(board))
    print(repr(board))

    print(board.is_move_legal((2,1)))
    board.make_move((2, 1))
    
    print(str(board))
    print(repr(board))