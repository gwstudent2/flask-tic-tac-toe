import unittest
from app import app, board, current_player, game_over, check_winner, check_draw

class TicTacToeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tic-Tac-Toe', response.data)

    def test_move(self):
        response = self.app.post('/move', json={'row': 0, 'col': 0})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'current_player', response.data)

    def test_invalid_move(self):
        self.app.post('/move', json={'row': 0, 'col': 0})
        response = self.app.post('/move', json={'row': 0, 'col': 0})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'error', response.data)

    def test_winner(self):
        self.app.post('/move', json={'row': 0, 'col': 0})
        self.app.post('/move', json={'row': 1, 'col': 0})
        self.app.post('/move', json={'row': 0, 'col': 1})
        self.app.post('/move', json={'row': 1, 'col': 1})
        self.app.post('/move', json={'row': 0, 'col': 2})
        response = self.app.post('/move', json={'row': 1, 'col': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'winner', response.data)

    def test_draw(self):
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 0), (2, 2), (2, 1)
        ]
        for row, col in moves:
            self.app.post('/move', json={'row': row, 'col': col})
        response = self.app.post('/move', json={'row': 2, 'col': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'draw', response.data)

    def test_reset(self):
        self.app.post('/move', json={'row': 0, 'col': 0})
        response = self.app.post('/reset')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Game reset', response.data)
        self.assertEqual(board, [['' for _ in range(3)] for _ in range(3)])
        self.assertEqual(current_player, 'X')
        self.assertFalse(game_over)

if __name__ == '__main__':
    unittest.main()
