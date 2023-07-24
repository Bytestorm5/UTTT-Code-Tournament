from board import Board, board_from_repr

board = board_from_repr("1 1 -1 -1 -1 -1 1 0 1 -1 0 0 0 0 0 0 0 0 1 0 1 0 1 1 0 -1 -1 1 0 0 1 0 -1 1 1 0 1 -1 -1 0 0 0 0 0 -1 1 -1 1 -1 -1 0 1 -1 0 -1 1 -1 0 -1 0 0 1 0 1 -1 1 0 -1 -1 0 1 0 1 0 -1 0 0 0 1 0 -1 1")
print(board)
print(list(board.get_legal_moves()))