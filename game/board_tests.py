# This is where unit tests for the board go
# Should NEVER be imported, this should purely be run as a standalone script to make sure the board is working properly

from board import Board
import unittest
import numpy as np

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        # Setting up a default board for testing
        self.default_board = Board()

    def test_init(self):
        board = Board(np.ones(81, np.short), 4)
        self.assertEqual(board.move_count, 81)
        self.assertEqual(board.current_board, 4)
        self.assertTrue((board.board == np.ones(81, np.short)).all())

    def test_get_subboard(self):
        subboard = self.default_board.get_subboard(0)
        self.assertTrue((subboard == np.zeros(9)).all())
        
    def test_subboard_winner(self):
        # We'll add tests here for various board configurations
        subboards = [
            ([1, 1, 1, -1, -1, 0, 0, 0, -1], 1, "First Row"),
            ([0, 1, 0, -1, 1, 0, 0, 1, -1], 1, "Middle Column"),
            ([0, -1, 1, 0, 1, 0, -1, -1, 1], None, "Ongoing"),
            ([0, 0, -1, -1, 0, -1, 1, 1, 1], 1, "Bottom Row"),
            ([1, 0, -1, 0, 1, -1, -1, 0, 1], 1, "Top-Left to Bottom-Right Diagonal"),
            ([1, 0, -1, 0, -1, 1, -1, 0, 0], -1, "Top-Right to Bottom-Left Diagonal"),
            ([1, -1, -1, -1, 1, 1, 1, 1, -1], 0, "Draw")
        ]

        for subboard in subboards:
            test = np.array(subboard[0] + [0] * 72)
            positive_board = Board(test)
            negative_board = Board(test * -1)
            
            negative_winner = None if subboard[1] == None else subboard[1] * -1

            self.assertTrue(positive_board.subboard_winner(0) == subboard[1], subboard[2] + " | Positive\n" + str(positive_board))
            self.assertTrue(negative_board.subboard_winner(0) == negative_winner, subboard[2] + " | Negative\n" + str(negative_board))

    def test_subboard_redirection(self):
        board = Board(np.array([1, 1, 1, 0, 0, 0, 0, 0, 0] + [0] * 72), 1)
        board.make_move((1, 0))
        self.assertTrue(board.current_board == -1)
        self.assertTrue(len(list(board.get_legal_moves())) == 71)

        board = Board(np.array([1, 1, -1, 0, 0, 0, 0, 0, 0] + [0] * 72), 1)
        board.make_move((1, 0))
        self.assertTrue(board.current_board == 0)
        self.assertTrue(len(list(board.get_legal_moves())) == 6)

    def test_subboard_open(self):
        self.assertTrue(self.default_board.subboard_open(0))

    def test_turn(self):
        self.assertEqual(self.default_board.turn(), 0)
        
    def test_copy(self):
        copied_board = self.default_board.copy()
        self.assertTrue((copied_board.board == self.default_board.board).all())
        
    def test_move_to_idx(self):
        self.assertEqual(self.default_board.move_to_idx((1, 2)), 11)
        
    def test_idx_to_move(self):
        self.assertEqual(self.default_board.idx_to_move(11), (1, 2))
        self.assertEqual(self.default_board.idx_to_move(80), (8, 8))
        self.assertEqual(self.default_board.idx_to_move(0), (0, 0))
        self.assertEqual(self.default_board.idx_to_move(1), (0, 1))
        
    def test_is_move_legal(self):
        # assuming the game just started
        self.assertTrue(self.default_board.is_move_legal((0, 0)))
        
    def test_get_legal_moves(self):
        # assuming the game just started
        self.assertEqual(list(self.default_board.get_legal_moves()), [(i, j) for i in range(9) for j in range(9)])
        
    def test_make_move(self):
        # assuming the game just started
        self.default_board.make_move((0, 0))
        self.assertEqual(self.default_board.board[0], 1)
        self.assertEqual(self.default_board.current_board, 0)
        self.assertEqual(self.default_board.move_count, 1)

    def test_repr(self):
        # Default board representation
        self.assertEqual(self.default_board.__repr__(), '0 '*81 + '-1')
    

if __name__ == "__main__":
    unittest.main()