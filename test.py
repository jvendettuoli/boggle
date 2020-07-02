from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def test_home_page(self):
        """Test if intial page HTML is displayed"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Welcome!</h2>', html)

    def test_board(self):
        """Test if board is setup and displayed"""

        with app.test_client() as client:
            res = client.get('/board', query_string={'size-input': '5'})
            html = res.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertIn('<tr class="row">', html)
            self.assertEqual(res.status_code, 200)

    def test_check_word(self):
        """Test if server gives proper response to submitted words"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['size'] = 5
                session['board'] = [["T", "E", "S", "T", "O"],
                                    ["T", "E", "S", "T", "O"],
                                    ["T", "E", "S", "T", "O"],
                                    ["T", "E", "S", "T", "O"],
                                    ["T", "E", "S", "T", "O"]]

            # Check for word on board
            res = client.get('/check-word', query_string={'word': 'test'})
            self.assertEqual(res.json['result'], 'ok')

            # Check for real word not on board
            res = client.get('/check-word', query_string={'word': 'false'})
            self.assertEqual(res.json['result'], 'not-on-board')

            # Check for fake word
            res = client.get('/check-word', query_string={'word': 'zzdrs'})
            self.assertEqual(res.json['result'], 'not-word')

    def test_save_stats(self):
        """Test if server properly updates the highscore when necessary."""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['highscore'] = 5

            # Check if highscore properly updated
            res = client.post(
                '/save-stats', json={'score': 10})
            self.assertIn('highscore', session)
            self.assertEqual(res.json['new_highscore'], True)

            res = client.post(
                '/save-stats', json={'score': 1})
            self.assertIn('highscore', session)
            self.assertEqual(res.json['new_highscore'], False)
