import random
import copy

def reset_grid():
    return [['','',''],
            ['','',''],
            ['','','']]

def ai_move(grid, player, depth):
    moves = get_available_moves(grid)
    if moves:
        score, move = minimax(grid, player, depth, True)
        return move
    return None

def get_available_moves(grid):
    return [[i, j] for i in range(3) for j in range(3) if grid[i][j] == '']

def minimax(grid, player, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    indices, won = check_for_3(grid)
    if won:
        return (-100 if is_maximizing else 100), None
    
    moves = get_available_moves(grid)
    if not moves or depth == 0:
        return evaluate_position(grid, player), None

    opponent = 'o' if player == 'x' else 'x'
    best_moves = []
    
    if is_maximizing:
        max_score = float('-inf')
        for move in moves:
            grid[move[0]][move[1]] = player
            score, _ = minimax(grid, opponent, depth - 1, False, alpha, beta)
            grid[move[0]][move[1]] = ''
            
            if score > max_score:
                max_score = score
                best_moves = [move]
            elif score == max_score:
                best_moves.append(move)
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break 

        best_move = random.choice(best_moves)
        return max_score, best_move
    else:
        min_score = float('inf')
        for move in moves:
            grid[move[0]][move[1]] = player
            score, _ = minimax(grid, opponent, depth - 1, True, alpha, beta)
            grid[move[0]][move[1]] = ''
            
            if score < min_score:
                min_score = score
                best_moves = [move]
            elif score == min_score:
                best_moves.append(move)
            
            beta = min(beta, score)
            if beta <= alpha:
                break 

        best_move = random.choice(best_moves)
        return min_score, best_move

def get_winning_combos():
    return (
        ((0,0), (0,1), (0,2)),
        ((1,0), (1,1), (1,2)),
        ((2,0), (2,1), (2,2)),

        ((0,0), (1,0), (2,0)),
        ((0,1), (1,1), (2,1)),
        ((0,2), (1,2), (2,2)),

        ((0,0), (1,1), (2,2)),
        ((0,2), (1,1), (2,0))
    )

def evaluate_position(grid, player):

    opponent = 'o' if player == 'x' else 'x'
    score = 0
    
    winning_combos = get_winning_combos()
    
    for combo in winning_combos:
        values = [grid[i][j] for i, j in combo]
        if opponent not in values:
            score += values.count(player)
            
    return score

def check_for_3(grid):
    
    winning_combos = get_winning_combos()
    for combo in winning_combos:
        values = [grid[i][j] for i, j in combo]
        if values[0] != '' and all(v == values[0] for v in values):
            return [list(pos) for pos in combo], True
            
    return [], False

def check_win(grid, status):
    indices, won = check_for_3(grid)
    if not won:
        return grid, won
        
    winner = grid[indices[0][0]][indices[0][1]]
    for i, j in indices:
        grid[i][j] = f'{status}_{winner}'
        
    return grid, won