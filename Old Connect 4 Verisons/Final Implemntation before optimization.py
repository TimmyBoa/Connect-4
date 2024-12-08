import asyncio
import websockets
import random
import logging

#Helps debug and prints information sent back and forth between AI and Server 
logging.basicConfig(level=logging.DEBUG)

def is_valid_move(board, col):
    '''
    checks if a given move is valid
    '''
    return board[0][col] == 0

def make_move(board, col, player):
    '''
    makes move given board player and col 
    finds first empty space starting from the bottom going up 
    '''
    for row in range(5, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return

def undo_move(board, col):
    '''
    undos first filled slot for a given col going down starting at the top 
    '''
    for row in range(len(board)):
        if not board[row][col] == 0:
            board[row][col] = 0
            return

def check_win(board, player):
    '''
    checks for horizontal, vertical, and diagonal wins
    returns True if there is a win otherwise is False 
    '''
    #Horizontal Win
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row][col + i] == player for i in range(4)]):
                return True
            
    #Vertical Win 
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if all([board[row + i][col] == player for i in range(4)]):
                return True
            
    #Diagonal Up to the Right Win 
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row + i][col + i] == player for i in range(4)]):
                return True

    #Diagonal Down to the Right Win
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row -
                          i][col + i] == player for i in range(4)]):
                return True
    #No wins in the board state
    return False

def evaluate_window(window, player):
    '''
    window equals cells currently being looked or 4 consurtive slots 
    adds or subtracts from score if it contains more of the opponents or players pieces 
    adds a factor to help look for moves that give more potential rows
    '''
    score = 0
    opponent = 2 if player == 1 else 1
    
    #Score/Point Factors
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4

    return score

def evaluate_board(board, player):
    '''
    evalutes a board position based upon all windows in the frame that lead potential wins
    and matches for the AI Giving a score if its "better"
    
    Increases score based upon if there are AI pieces- 
    in the center since central control is a principle you should generally follow in connect 4 
    '''
    score = 0
    rows, cols = len(board), len(board[0])
    
    #Central Control Score
    center_array = [board[i][cols // 2] for i in range(rows)]
    center_count = center_array.count(player)
    score += center_count * 3

    #Up and Downs potential Matches
    for row in range(rows):
        row_array = [board[row][i] for i in range(cols)]
        for col in range(cols - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player)

    #Left and Right Matches
    for col in range(cols):
        col_array = [board[i][col] for i in range(rows)]
        for row in range(rows - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player)
            
    #Diagonal Up to Right Matches
    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)
            
    #Diagonal Down to Right Matches
    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def is_terminal_node(board):
    '''
    Determines is a given board is a leaf or terminal node
    meaning there are no possible moves in the board position
    '''
    
    #checks if the position is won by a particular player
    if check_win(board, 1) or check_win(board, 2):
        return True
    
    #checks if the Game is Drawn
    for col in range(len(board[0])):
        if board[0][col] != 0:
            return True
    
    return False

def minimax(board, depth, alpha, beta, maximizing_player, player):
    '''
    Through recurison evalutes all nodes/boards in a given position up to the depth specfied 
    Alpha and Beta are used to find best/Worst nodes and are intizalied in function due to the use of Recursion
    '''
    #gets valid moves 
    valid_moves=[]
    for col in range(len(board[0])):
        if is_valid_move(board, col):
            valid_moves.append(col)
    terminal = is_terminal_node(board)
    
    #evalutes the position if it is a leaf or terminal node or the start
    if depth == 0 or terminal:
        if terminal:
            if check_win(board, player):
                return (None, 100000000000000)
            elif check_win(board, 2 if player == 1 else 1):
                return (None, -10000000000000)
            else:
                return (random.choice(valid_moves), 0)
        else:
            return (random.choice(valid_moves), evaluate_board(board, player))
        
    #Calculating positions if AI turn
    if maximizing_player:
        value = -float('inf')
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            make_move(board, col, player)
            new_score = minimax(board, depth - 1, alpha, beta, False, player)[1] #recurison for each layer
            undo_move(board, col)
            
            #Calculates Score for path in Tree
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    
    #Calculating positions for other player  
    else:
        value = float('inf')    
        best_col = random.choice(valid_moves)
        opponent = 2 if player == 1 else 1
        for col in valid_moves:
            
            make_move(board, col, opponent)
            new_score = minimax(board, depth - 1, alpha, beta, True, player)[1] #recurison for each layer
            undo_move(board, col)
            
            #Calculates Score for path in Tree
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def calculate_move(board, player, depth):
    '''
    Calculates move using Minimax Function to evaluate potential board states
    checks for all edge cases including getting valid moves and if there are no aviable moves 
    '''
    
    #potential moves 
    valid_moves=[]
    for col in range(len(board[0])):
        if is_valid_move(board, col):
            valid_moves.append(col)
    
    #no possible moves 
    if not valid_moves:
        return None
    
    #Calculating Best move 
    best_col, _ = minimax(board, depth, -float('inf'), float('inf'), True, player)
    
    #If no good options plays a random move 
    if best_col is None:
        best_col = random.choice(valid_moves)
    return best_col

async def gameloop(socket, created):
    '''
    Main Game Loop That allows AI to play connect 4 with Input/Output from the Server following this API
    https://github.com/exoRift/mindsmachines-connect4/blob/master/documentation/datasheet.png
    '''
    active = True
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    while active: #Loops While Game is not Ended 
        message = (await socket.recv()).split(':') #Message from Server 

        match message[0]: 
            case 'GAMESTART': #Game Started
                if created:
                    col = calculate_move(board, 1, 6) #Finds best move
                    make_move(board, col, 1) #Updates Board
                    await socket.send(f'PLAY:{col}') #Send move to the Server
                
            case 'OPPONENT': #Opponent has Moved 
                make_move(board, int(message[1]), 2) #Updates Board
                col = calculate_move(board, 1, 6) #Finds best move
                make_move(board, col, 1)  #Updates board
                await socket.send(f'PLAY:{col}') #Send move to the sever
                
            case 'WIN' | 'LOSS' | 'DRAW' | 'TERMINATED': # Game has ended
                print(message[0])
                active = False

async def create_game(server):
        async with websockets.connect(f'ws://{server}/create') as socket: # Establish websocket connection
            await gameloop(socket, True)

async def join_game(server, id):
    try:
        async with websockets.connect(f'ws://{server}/join/{id}') as socket: # Establish websocket connection
            await gameloop(socket, False)
    except Exception as e:
        print(f"Error connecting to the game server: {e}")
        
if __name__ == '__main__': # Program entrypoint
  server = input('Server IP: ').strip() # Get IP from console

  protocol = input('Join game or create game? (j/c): ').strip() # Get action from console

  match protocol:
    case 'c':
      asyncio.run(create_game(server))
    case 'j':
      id = input('Game ID: ').strip()

      asyncio.run(join_game(server, id))
    case _:
      print('Invalid protocol!')

#Test Code without the Server 
'''
if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    for x in range(len(board) * len(board[0])):
        player = 1 if x % 2 == 0 else 2
        col = calculate_move(board, player, 3)
        make_move(board, col, player)
        print(f"Player {player} placed at column {col}")
'''
