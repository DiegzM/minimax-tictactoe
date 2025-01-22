from flask import Flask, render_template, redirect, request, session, url_for
import os
import random
from functions import reset_grid, ai_move, check_win

app = Flask(__name__)
app.secret_key = os.urandom(24) 

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get('play'):
            if request.form.get('mode') == 'active':
                session['mode'] = 'o'
            else:
                session['mode'] = 'x'
            session['depth'] = int(request.form.get('depth'))
            return redirect('/game')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')
    

@app.route('/game', methods=["GET", "POST"])
def game():

    if 'grid' not in session:
        session['grid'] = reset_grid()
    grid = session['grid']
    if 'mode' not in session:
        session['mode'] = 'x'
    mode = session['mode']
    opponent = ''
    depth = session['depth']

    if mode == 'o':
        opponent = 'x'
    else:
        opponent = 'o'
    message = ''

    if request.method == "POST":

        if request.form.get('square'):
            square = request.form.get('square')
            row, col = map(int, square.split())
            empty_squares = [[i, j] for i, row in enumerate(grid) for j, value in enumerate(row) if value == '']
            game_over = False
            
            if not empty_squares:
                game_over = True
                message = 'TIE!'
            for i in grid:
                if any(word in i for word in ['win_x', 'lose_x', 'win_o', 'lose_o']):
                    game_over = True
                for word in ['win_x', 'lose_x']:
                    if word in i:
                        message = 'X WON!'
                        break
                for word in ['win_o', 'lose_o']:
                    if word in i:
                        message = 'O WON!'
                        break
            if not game_over:
                if [row, col] in empty_squares:
                    grid[row][col] = mode
                    win_grid, won = check_win(grid, 'win')
                    if won:
                        grid = win_grid
                        session['grid'] = grid
                        message = mode.upper() + ' WON!'
                        game_over = True
                    else:
                        move = ai_move(grid, opponent, depth)
                        if move:
                            grid[move[0]][move[1]] = opponent
                        lose_grid, lost = check_win(grid, 'lose')
                        if lost:
                            grid = lose_grid
                            session['grid'] = grid
                            message = opponent.upper() + ' WON!'
                            game_over = True
                empty_squares = [[i, j] for i, row in enumerate(grid) for j, value in enumerate(row) if value == '']
                if not empty_squares and not game_over:
                    message = 'TIE!'

        elif request.form.get('reset'):
            if mode == 'o':
                grid = reset_grid()
                move = ai_move(grid, opponent, depth)
                grid[move[0]][move[1]] = 'x'
                session['grid'] = grid
            else:
                grid = reset_grid()
        elif request.form.get('quit'):
            grid = reset_grid()
            session['grid'] = grid
            return redirect('/')

        session['grid'] = grid

    else:
        if mode == 'o':
            grid = reset_grid()
            move = ai_move(grid, opponent, depth)
            grid[move[0]][move[1]] = 'x'
            session['grid'] = grid
        else:
            grid = reset_grid()
        session['grid'] = grid
    
    return render_template('game.html', grid=grid, message=message)

if __name__ == "__main__":
    app.run(debug=False)