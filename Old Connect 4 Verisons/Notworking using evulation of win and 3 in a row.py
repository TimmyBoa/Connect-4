# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:02:59 2024

@author: Tim
"""
import asyncio
import websockets
import random
import logging
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
            return board

def undo_move(board, col):
    '''
    undos first filled space for a given col going down startring at the top 
    '''
    for row in range(len(board)):
        if not board[row][col] == 0:
            board[row][col] = 0
            return board

def check_win(board, player):
    '''
    checks for horizontal vertical and diagonal wins
    '''
    potential_wins=[]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (col + 3 < len(board[0]) and\
                board[row][col] == player and\
                board[row][col+1] == player and\
                board[row][col+2] == player ):
                potential_wins.append([row, col+3])
                #potential_wins.append([row,col-1])
                
            if (row + 3 < len(board) and\
                board[row][col] == player and\
                board[row+1][col] == player and\
                board[row+2][col] == player):
                potential_wins.append([row+3, col])
                #potential_wins.append([row-1, col])
                
            if (row + 3 < len(board) and col + 3 < len(board[0]) and\
                board[row][col] == player and\
                board[row+1][col+1] == player and\
                board[row+2][col+2] == player):
                potential_wins.append([row+3, col+3])
                #potential_wins.append([row-1, col-1])
                
            if (row - 3 >= 0 and col + 3 < len(board[0]) and\
                board[row][col] == player and\
                board[row-1][col+1] == player and\
                board[row-2][col+2] == player):
                #potential_wins.append([row+1, col-1])
                potential_wins.append([row-3, col+3])
    
    if len(potential_wins)>0:
        for potential_win in potential_wins:
            if potential_win[0]<0 or potential_win[0]>5:
                potential_wins.remove(potential_win)
            
            elif potential_win[1]<0 or potential_win[1]>6:
                potential_wins.remove(potential_win)
            
            elif board[potential_win[0]][potential_win[1]]==0:
                potential_wins.remove(potential_win)
                
    if len(potential_wins)>0:
        return potential_wins
    else:
        return None

def check_3s(board, player):
    '''
    #checks for potential all 3 open move permutations
    '''
    for row in range(len(board)):
        for col in range(len(board)):
            print(":)")
    return None 

def calculate_move(board, player, depth):
    
    if player==1:
        opponent=2
    else:
        opponent=1
    #gets valid moves 
    valid_moves = []
    
    for col in range(len(board[0])) :
        if is_valid_move(board, col):
            valid_moves.append(col)
            
    #checks is there is a win condtion 
    potential_wins=check_win(board, player)
    
    if not potential_wins is None:
        return potential_wins[0][1]
    potential_blocks=check_win(board, opponent)
    if not potential_blocks is None:
        return potential_blocks[0][1]
    
    potential_moves=[]
    
    for col in valid_moves:
        make_move(board, col, player)
        moves_to_add=check_win(board, player)
        if not moves_to_add is None:
            potential_moves.append(moves_to_add)
        moves_to_add=check_win(board, opponent)
        if not moves_to_add is None:
            potential_moves.append(moves_to_add)
        undo_move(board, col)
    if len(potential_moves)>0:
        return int(random.randint(0, len(potential_moves)))
    
    return int(random.randint(0,6))

async def gameloop (socket, created):
  active = True
  board = [[0,0,0,0,0,0,0],\
           [0,0,0,0,0,0,0],\
           [0,0,0,0,0,0,0],\
           [0,0,0,0,0,0,0],\
           [0,0,0,0,0,0,0],\
           [0,0,0,0,0,0,0]]
  while active:
    message = (await socket.recv()).split(':')

    match message[0]:
      case 'GAMESTART':
        if created:
            col = calculate_move(board, 1, 1)
            board = make_move(board, col, 1)
            await socket.send(f'PLAY:{col}')
      
      case 'OPPONENT':
        board = make_move(board, int(message[1]), 2)
        col = calculate_move(board, 1, 1)
        board = make_move(board, col, 1)
        await socket.send(f'PLAY:{col}')
      
      case 'WIN' | 'LOSS' | 'DRAW' | 'TERMINATED':
        print(message[0])

        active = False

async def create_game (server):
  async with websockets.connect(f'ws://{server}/create') as socket:
    await gameloop(socket, True)

async def join_game(server, id):
    try:
        async with websockets.connect(f'ws://{server}/join/{id}') as socket:
            await gameloop(socket, False)
    except Exception as e:
        print(f"Error connecting to the game server: {e}")

if __name__=="__main__":
    board = [[0,0,0,0,0,0,0],\
             [0,0,0,0,0,0,0],\
             [0,0,0,0,0,0,0],\
             [0,0,0,0,0,0,0],\
             [0,0,0,0,0,0,0],\
             [0,0,0,0,0,0,0]]
    for x in range(len(board)*len(board[0])):
        if x % 2 == 0 :
            player =1
        else:
            player = 2
        col = calculate_move(board, player, 5)
        make_move(board, col, player)
'''
if __name__ == '__main__':
  server = input('Server IP: ').strip()

  protocol = input('Join game or create game? (j/c): ').strip()
  match protocol:
    case 'c':
      asyncio.run(create_game(server))
    case 'j':
      id = input('Game ID: ').strip()
      asyncio.run(join_game(server, id))
    case _:
      print('Invalid protocol!')
'''

