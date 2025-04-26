from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Game state
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False

def check_winner():   
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def check_draw():
    for row in board:
        if '' in row:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player, game_over
    if game_over:
        return jsonify({'error': 'Game is over'})

    data = request.get_json()
    row, col = int(data['row']), int(data['col'])

    if board[row][col] != '':
        return jsonify({'error': 'Cell is already occupied'})

    board[row][col] = current_player
    winner = check_winner()
    if winner:
        game_over = True
        return jsonify({'winner': winner})
    elif check_draw():
        game_over = True
        return jsonify({'draw': True})

    current_player = 'O' if current_player == 'X' else 'X'
    return jsonify({'current_player': current_player})

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    return jsonify({'status': 'Game reset'})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
