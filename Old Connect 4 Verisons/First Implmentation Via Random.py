# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:33:35 2024

@author: Tim/Jordan
"""

import asyncio
import websockets
import random
import nest_asyncio

nest_asyncio.apply()

def calculate_move(col):
    return random.randint(0, 6)

async def gameloop(socket, created):
    active = True

    while active:
        try:
            message = (await socket.recv()).split(':')
            if message[0] == 'GAMESTART':
                col = calculate_move(message[1])
                await socket.send(f'PLAY:{col}')
            elif message[0] == 'OPPONENT':
                col = calculate_move(message[1])
                await socket.send(f'PLAY:{col}')
            elif message[0] in {'WIN', 'LOSS', 'DRAW', 'TERMINATED'}:
                print(message[0])
                active = False
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
            active = False
        except Exception as e:
            print(f"Error during gameloop: {e}")
            active = False

async def create_game(server):
    try:
        async with websockets.connect(f'ws://{server}/create') as socket:
            await gameloop(socket, True)
    except websockets.InvalidURI as e:
        print(f"Invalid URI: {e}")
    except websockets.InvalidHandshake as e:
        print(f"Invalid handshake: {e}")
    except Exception as e:
        print(f"Failed to create game: {e}")

async def join_game(server, id):
    try:
        async with websockets.connect(f'ws://{server}/join/{id}') as socket:
            await gameloop(socket, False)
    except websockets.InvalidURI as e:
        print(f"Invalid URI: {e}")
    except websockets.InvalidHandshake as e:
        print(f"Invalid handshake: {e}")
    except Exception as e:
        print(f"Failed to join game: {e}")

if __name__ == '__main__':
    server = input('Server IP: ').strip()
    protocol = input('Join game or create game? (j/c): ').strip()

    loop = asyncio.get_event_loop()
    
    if protocol == 'c':
        loop.run_until_complete(create_game(server))
    elif protocol == 'j':
        id = input('Game ID: ').strip()
        loop.run_until_complete(join_game(server, id))
    else:
        print('Invalid protocol!')
