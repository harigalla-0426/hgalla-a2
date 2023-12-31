#
# raichu.py : Play the game of Raichu
#
# hgalla, rathlur, vchitti
#
# Based on skeleton code by D. Crandall, Oct 2021
# The code for minimax was developed after referring to following youtube video: https://youtu.be/l-hh51ncgDI
# This includes a basic structure of minimax along with alpha beta pruning
import sys
from copy import deepcopy


def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def string_output(board, N):
    board_string = ''
    for i in range(N):
        for j in range(N):
            board_string += board[i][j]
    return board_string

def string_to_board(string_value, N):
    '''
    This method will return the board in a matrix format from an input string.
    '''
    board = []

    for i in range(0, len(string_value), N):
        row = []
        for j in range(N):
            row.append(string_value[i+j])
        board.append(row)

    return board


def is_valid_index(i, j, N):
    '''
    This method will check if the given index is inside the scope of the board
    '''
    if i >= 0 and i < N and j >= 0 and j < N:
        return True
    else:
        return False


def find_count(board):
    '''
    This method will return the count along with indices of each piece on the board
    '''
    # Symbols:
    # . - Empty spot on board
    # w - White pichus
    # W - White pikachu
    # b - Black pichu
    # B - Black Pikachu
    # @ - White Raichu
    # $ - Black Raichu

    pieces_count = {'W': [], 'w': [], 'b': [], 'B': [], '@': [], '$': []}

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] in 'wWbB@$':
                pieces_count[board[i][j]].append((i, j))

    return pieces_count


def return_modified_board(board, oldPos, newPos, isAttack = False, attackPos = None, returnCopy = True):
    '''
    Return the modified board by swapping the positions and other options specified like: 	
    whether it's in attack mode or whether to return a copy of board etc.
    '''

    if returnCopy:
        new_board = deepcopy(board)
        new_board[oldPos[0]][oldPos[1]], new_board[newPos[0]][newPos[1]] = \
        new_board[newPos[0]][newPos[1]], new_board[oldPos[0]][oldPos[1]]

        if isAttack:
            new_board[attackPos[0]][attackPos[1]] = '.'

        check_raichu_evolution(new_board, len(new_board))

        return new_board
    else:
        board[oldPos[0]][oldPos[1]], board[newPos[0]][newPos[1]] = board[newPos[0]][newPos[1]], board[oldPos[0]][oldPos[1]]
        
        if isAttack:
            board[attackPos[0]][attackPos[1]] = '.'

        check_raichu_evolution(board, len(board))

        return board


def evaluation_function(board_state):
    '''
    To calculate the evaluation function e(s), which will help decide how good a particular board is for one player
    '''
    remaining_count = find_count(board_state)

    # Weights for pichus, pikachus and raichus respectively
    x1 = 2
    x2 = 4
    x3 = 8

    eval_value = x1*(len(remaining_count['w']) - len(remaining_count['b'])) \
        + x2*(len(remaining_count['W']) - len(remaining_count['B'])) \
        + x3*(len(remaining_count['@']) - len(remaining_count['$']))

    return eval_value


def check_raichu_evolution(board, N):
    '''	
    Check for raichu formation for both white and black pieces	
    '''
    # Evolve to black raichu when pichu or pikachu reaches row 0
    for j in range(len(board[0])):
        if board[0][j] in 'bB':
            board[0][j] = '$'

    # Evolve to white raichu when a white pichu or pikachu reaches row N-1
    for j in range(len(board[N-1])):
        if board[N-1][j] in 'wW':
            board[N-1][j] = '@'


def check_game_end(board_state, isWhite):
    '''	
    Check if the game has ended	
    '''
    count_map = find_count(board_state)
    if (isWhite and (len(count_map['b']) == 0 and len(count_map['B']) == 0 and len(count_map['$']) == 0)):
        return True

    if (not isWhite and (len(count_map['w']) == 0 and len(count_map['W']) == 0 and len(count_map['@']) == 0)):
        return True

    return False


def successors(board_state, isWhiteTurn):
    '''	
    Method to find all the successors for a given board state	
    '''
    successors = []
    N = len(board_state)
        
    for (key_piece, occurrences) in find_count(board_state).items():

        if isWhiteTurn:
            # Calculate moves for white pichu
            if key_piece == 'w' and len(occurrences):
                for (i,j) in occurrences:
                    # checking whether we can move diagonally forward left
                    if is_valid_index(i+1, j-1, N):
                        # checking if the white pichu can attack
                        if board_state[i+1][j-1] == 'b' and is_valid_index(i+2, j-2, N) and board_state[i+2][j-2] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i+2, j-2), isAttack = True, attackPos=(i+1,j-1)))

                        # checking if the normal move is feasible
                        elif board_state[i+1][j-1] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i+1, j-1)))
                                
                    # checking diagnal right
                    if is_valid_index(i+1, j+1, N):
                        # checking if the white pichu can attack
                        if board_state[i+1][j+1] == 'b' and is_valid_index(i+2, j+2, N) and board_state[i+2][j+2] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i+2, j+2), isAttack = True, attackPos=(i+1,j+1)))
        
                        # checking if the normal move is feasible
                        elif board_state[i+1][j+1] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i+1, j+1)))

            # Moves for white pikachu          
            if key_piece == 'W' and len(occurrences):
                for (i,j) in occurrences:
                    # checking whether we can move straight
                    for k in range(1,3):
                        if not is_valid_index(i+k, j, N):
                            break
                        if board_state[i+k][j] not in 'bB.':
                            break
                            
                        # checking if the white pikachu can attack
                        if board_state[i+k][j] in 'bB' and is_valid_index(i+k+1, j, N) :
                            if board_state[i+k+1][j] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i+k+1, j), isAttack = True, attackPos=(i+k,j)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i+k][j] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i+k, j)))
                            
                    # checking left
                    for k in range(1,3):
                        if not is_valid_index(i, j-k, N):
                            break
                        if board_state[i][j-k] not in 'bB.':
                            break
                            
                        # checking if the white pikachu can attack
                        if board_state[i][j-k] in 'bB' and is_valid_index(i, j-k-1, N):
                            if board_state[i][j-k-1] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i, j-k-1), isAttack = True, attackPos=(i,j-k)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i][j-k] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i, j-k)))
                            
                    # checking right
                    for k in range(1,3):
                        if not is_valid_index(i, j+k, N):
                            break
                        if board_state[i][j+k] not in 'bB.':
                            break
                            
                        # checking if the black pikachu can attack
                        if board_state[i][j+k] in 'bB' and is_valid_index(i, j+k+1, N):
                            if board_state[i][j+k+1] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i, j+k+1), isAttack = True, attackPos=(i,j+k)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i][j+k] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i, j+k)))
                            
            # Raichu moves               
            if key_piece == '@' and len(occurrences):
                for (i,j) in occurrences:
                    
                    # moving forward
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    count = 0
                    for k in range(i+1, N):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[k][j] not in 'bB$.':
                            break
                            
                        if temp_board[k][j] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k, j)))
                            
                        if temp_board[k][j] in 'bB$' and is_valid_index(k+1, j, N):
                            if temp_board[k+1][j] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k+1, j), isAttack = True, attackPos=(k,j), returnCopy = False))
                            skipNextIter = True
                            temp_i = k+1
                            
                    # moving back
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    count = 0
                    for k in range(i-1, -1, -1):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[k][j] not in 'bB$.':
                            break
                        
                        if temp_board[k][j] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k, j)))
                            
                        if temp_board[k][j] in 'bB$' and is_valid_index(k-1, j, N):
                            if temp_board[k-1][j] != '.' or count==1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k-1, j), isAttack = True, attackPos=(k,j), returnCopy = False))
                            skipNextIter = True
                            temp_i = k-1
                            
                            
                    # moving left
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_j = j
                    count = 0
                    for k in range(j-1, -1, -1):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i][k] not in 'bB$.':
                            break
                            
                        if temp_board[i][k] == '.':
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k)))
                            
                        if temp_board[i][k] in 'bB$' and is_valid_index(i, k-1, N):
                            if temp_board[i][k-1] != '.' or count==1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k-1), isAttack = True, attackPos=(i,k), returnCopy = False))
                            skipNextIter = True
                            temp_j = k-1
                            
                            
                    # moving right
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_j = j
                    count = 0
                    for k in range(j+1, N):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i][k] not in 'bB$.':
                            break
                            
                        if temp_board[i][k] == '.':
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k)))
                            
                        if temp_board[i][k] in 'bB$' and is_valid_index(i, k+1, N):
                            if temp_board[i][k+1] != '.' or count==1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k+1), isAttack = True, attackPos=(i,k), returnCopy = False))
                            skipNextIter = True
                            temp_j = k+1
                            
                    # Diagonal Moves
        
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i-k, j-k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i-k][j-k] not in 'bB$.':
                            break
                            
                        if temp_board[i-k][j-k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k, j-k)))
                            
                        if temp_board[i-k][j-k] in 'bB$' and is_valid_index(i-k-1, j-k-1, N):
                            if temp_board[i-k-1][j-k-1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k-1, j-k-1), isAttack = True, attackPos=(i-k,j-k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i-k-1
                            temp_j = j-k-1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i+k, j+k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i+k][j+k] not in 'bB$.':
                            break
                            
                        if temp_board[i+k][j+k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k, j+k)))
                            
                        if temp_board[i+k][j+k] in 'bB$' and is_valid_index(i+k+1, j+k+1, N):
                            if temp_board[i+k+1][j+k+1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k+1, j+k+1), isAttack = True, attackPos=(i+k,j+k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i+k+1
                            temp_j = j+k+1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i-k, j+k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i-k][j+k] not in 'bB$.':
                            break
                            
                        if temp_board[i-k][j+k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k, j+k)))
                            
                        if temp_board[i-k][j+k] in 'bB$' and is_valid_index(i-k-1, j+k+1, N):
                            if temp_board[i-k-1][j+k+1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k-1, j+k+1), isAttack = True, attackPos=(i-k,j+k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i-k-1
                            temp_j = j+k+1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i+k, j-k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i+k][j-k] not in 'bB$.':
                            break
                            
                        if temp_board[i+k][j-k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k, j-k)))
                            
                        if temp_board[i+k][j-k] in 'bB$' and is_valid_index(i+k+1, j-k-1, N):
                            if temp_board[i+k+1][j-k-1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k+1, j-k-1), isAttack = True, attackPos=(i+k,j-k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i+k+1
                            temp_j = j-k-1
        else:
            # Moves for black pichu          
            if key_piece == 'b' and len(occurrences):
                for (i,j) in occurrences:
                    # checking whether we can move diagonally forward left
                    if is_valid_index(i-1, j-1, N):
                        # checking if the black pichu can attack
                        if board_state[i-1][j-1] == 'w' and is_valid_index(i-2, j-2, N) and board_state[i-2][j-2] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i-2, j-2), isAttack = True, attackPos=(i-1,j-1)))

                        # checking if the normal move is feasible
                        elif board_state[i-1][j-1] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i-1, j-1)))
                                
                    # checking diagonal right
                    if is_valid_index(i-1, j+1, N):
                        # checking if the black pichu can attack
                        if board_state[i-1][j+1] == 'w' and is_valid_index(i-2, j+2, N) and board_state[i-2][j+2] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i-2, j+2), isAttack = True, attackPos=(i-1,j+1)))
        
                        # checking if the normal move is feasible
                        elif board_state[i-1][j+1] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i-1, j+1)))

            # moves for black pikachu
            if key_piece == 'B' and len(occurrences):
                for (i,j) in occurrences:
                    # checking whether we can move straight
                    for k in range(1,3):
                        if not is_valid_index(i-k, j, N):
                            break
                        if board_state[i-k][j] not in 'wW.':
                            break
                            
                        # checking if the black pikachu can attack
                        if board_state[i-k][j] in 'wW' and is_valid_index(i-k-1, j, N):
                            if board_state[i-k-1][j] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i-k-1, j), isAttack = True, attackPos=(i-k,j)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i-k][j] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i-k, j)))
                            
                    # checking left
                    for k in range(1,3):
                        if not is_valid_index(i, j-k, N):
                            break
                        if board_state[i][j-k] not in 'wW.':
                            break
                            
                        # checking if the black pikachu can attack
                        if board_state[i][j-k] in 'wW' and is_valid_index(i, j-k-1, N):
                            if board_state[i][j-k-1] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i, j-k-1), isAttack = True, attackPos=(i,j-k)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i][j-k] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i, j-k)))
                            
                    # checking right
                    for k in range(1,3):
                        if not is_valid_index(i, j+k, N):
                            break
                        if board_state[i][j+k] not in 'wW.':
                            break
                            
                        # checking if the white pikachu can attack
                        if board_state[i][j+k] in 'wW' and is_valid_index(i, j+k+1, N):
                            if board_state[i][j+k+1] != '.':
                                break
                            successors.append(return_modified_board(board_state, (i,j), (i, j+k+1), isAttack = True, attackPos=(i,j+k)))
                            break

                        # checking if the normal move is feasible
                        if board_state[i][j+k] == '.':
                            successors.append(return_modified_board(board_state, (i,j), (i, j+k)))

            # Raichu moves               
            if key_piece == '$' and len(occurrences):
                for (i,j) in occurrences:
                
                # moving forward
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    count = 0
                    for k in range(i+1, N):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[k][j] not in 'wW@.':
                            break
                            
                        if temp_board[k][j] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k, j)))
                            
                        if temp_board[k][j] in 'wW@' and is_valid_index(k+1, j, N):
                            if temp_board[k+1][j] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k+1, j), isAttack = True, attackPos=(k,j), returnCopy = False))
                            skipNextIter = True
                            temp_i = k+1
                            
                    # moving back
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    count = 0
                    for k in range(i-1, -1, -1):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[k][j] not in 'wW@.':
                            break
                        
                        if temp_board[k][j] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k, j)))
                            
                        if temp_board[k][j] in 'wW@' and is_valid_index(k-1, j, N):
                            if temp_board[k-1][j] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,j), (k-1, j), isAttack = True, attackPos=(k,j), returnCopy = False))
                            skipNextIter = True
                            temp_i = k-1
                            
                            
                    # moving left
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_j = j
                    count = 0
                    for k in range(j-1, -1, -1):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i][k] not in 'wW@.':
                            break
                            
                        if temp_board[i][k] == '.':
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k)))
                            
                        if temp_board[i][k] in 'wW@' and is_valid_index(i, k-1, N):
                            if temp_board[i][k-1] != '.' or count==1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k-1), isAttack = True, attackPos=(i,k), returnCopy = False))
                            skipNextIter = True
                            temp_j = k-1
                            
                            
                    # moving right
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_j = j
                    count = 0
                    for k in range(j+1, N):
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i][k] not in 'wW@.':
                            break
                            
                        if temp_board[i][k] == '.':
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k)))
                            
                        if temp_board[i][k] in 'wW@' and is_valid_index(i, k+1, N):
                            if temp_board[i][k+1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (i,temp_j), (i, k+1), isAttack = True, attackPos=(i,k), returnCopy = False))
                            skipNextIter = True
                            temp_j = k+1
                            
                    # Diagonal Moves TODO
        
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i-k, j-k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i-k][j-k] not in 'wW@.':
                            break
                            
                        if temp_board[i-k][j-k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k, j-k)))
                            
                        if temp_board[i-k][j-k] in 'wW@' and is_valid_index(i-k-1, j-k-1, N):
                            if temp_board[i-k-1][j-k-1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k-1, j-k-1), isAttack = True, attackPos=(i-k,j-k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i-k-1
                            temp_j = j-k-1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i+k, j+k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i+k][j+k] not in 'wW@.':
                            break
                            
                        if temp_board[i+k][j+k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k, j+k)))
                            
                        if temp_board[i+k][j+k] in 'wW@' and is_valid_index(i+k+1, j+k+1, N):
                            if temp_board[i+k+1][j+k+1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k+1, j+k+1), isAttack = True, attackPos=(i+k,j+k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i+k+1
                            temp_j = j+k+1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i-k, j+k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i-k][j+k] not in 'wW@.':
                            break
                            
                        if temp_board[i-k][j+k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k, j+k)))
                            
                        if temp_board[i-k][j+k] in 'wW@' and is_valid_index(i-k-1, j+k+1, N):
                            if temp_board[i-k-1][j+k+1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i-k-1, j+k+1), isAttack = True, attackPos=(i-k,j+k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i-k-1
                            temp_j = j+k+1
                            
                    skipNextIter = False
                    temp_board = deepcopy(board_state)
                    temp_i = i
                    temp_j = j
                    count = 0
                    for k in range(1, N):
                        if not is_valid_index(i+k, j-k, N):
                            break
                        if skipNextIter:
                            skipNextIter = False
                            continue
                        if temp_board[i+k][j-k] not in 'wW@.':
                            break
                            
                        if temp_board[i+k][j-k] == '.':
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k, j-k)))
                            
                        if temp_board[i+k][j-k] in 'wW@' and is_valid_index(i+k+1, j-k-1, N):
                            if temp_board[i+k+1][j-k-1] != '.' or count == 1:
                                break
                            count += 1
                            successors.append(return_modified_board(temp_board, (temp_i,temp_j), (i+k+1, j-k-1), isAttack = True, attackPos=(i+k,j-k), returnCopy = False))
                            skipNextIter = True
                            temp_i = i+k+1
                            temp_j = j-k-1
                          
    return successors


def minimax(board, depth, isWhiteTurn, alpha=-2**10000, beta=2**1000):
    '''
    This method will call minimax recursively in a depth-first fashion until 	
    a) it reaches its max depth or b) it reaches a end solution. The evaluation values from 	
    these states are propagated upwards keeping in check that each player will make the best possible move	
    from the successors available.
    '''
    if depth == 0 or check_game_end(board, isWhiteTurn):
        return (evaluation_function(board), board)

    if isWhiteTurn:
        maxVal = -2*10000
        maxBoard = None
        for s in successors(board, True):
            if check_game_end(s, False):
                return (maxVal, s)
            (value, new_board) = minimax(s, depth-1, False)
            if not maxBoard:
                maxBoard = s
                maxVal = value
            elif value > maxVal:
                maxBoard = s
                maxVal = value
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return (maxVal, maxBoard)

    else:
        minVal = 2*10000
        minBoard = None
        for s in successors(board, False):
            if check_game_end(s, True):
                return (minVal, s)
            (value, new_board) = minimax(s, depth-1, True)
            if not minBoard:
                minBoard = s
                minVal = value
            elif value > minVal:
                minBoard = s
                minVal = value
            beta = max(beta, value)
            if beta <= alpha:
                break
        return (minVal, minBoard)


def find_best_move(board, N, player, timelimit):
    board = string_to_board(board, N)
    depth = 2
    while depth:
        output = minimax(board, depth, player == 'w')
        depth -= 1
        yield string_output(output[1], N)
        if check_game_end(output[1], player=='w'):
            return


def print_successors(successors):
    print(len(successors))
    for s in successors:
        print_board(s)
        print('------------------------>>>>')
        
def print_board(board):
    for i in range(len(board)):
        print(board[i])

    print(find_count(board))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player +
          " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    find_best_move(board, N, player, timelimit)
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)