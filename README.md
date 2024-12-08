# Connect-4

This is our Connect 4 AI for the Minds and Machines Connect 4 Project 

Link to Report:
https://docs.google.com/document/d/1-dDO5mXBttYbzZ3cBEFF1mnbpyPeIA_D1hy030kfWCQ/edit?usp=sharing

This code is built off the following dependencies hooking up to a server via websockets 

Link to Server/Dependencies: 
https://github.com/exoRift/mindsmachines-connect4/blob/master/documentation/introduction.md

Connect-4 write-up - Timothy Pollard, Jordan Walek

1. 	INTRODUCTION
Connect-4 involves many cognitive functions like planning, pattern recognition, and decision-making to analyze the board and predict future moves. We chose this project because we wanted to create a full-function AI that works to play a childhood game that we all know and love, Connect-4, that will beat a human every time it plays and mimic these cognitive functions. Our final version of this game will be a fully functioning AI that a human can play against. It will be able to predict the humans' next move and be able to solve this game so that the humans to lose every time. The question that we hope to answer; is whether it is possible to create a program that will take account of every possible move on a connect-4 board and choose the best move to get 4 in a row the fastest and beat the human who is playing. 
This relates to our discussion about the mind: Will our program have a mind of its own? In class, we have discussed whether AI has a mind or not. Since an AI can think and act by itself it does have a mind which is a byproduct of a human. Since we are programming an AI to search for all the possible moves and choose the best option to win, it will be in theory acting on its own.



2. 	PROGRAM
The program starts off by creating the following tools to make the process of playing Connect 4 possible for a machine: 
Checking is a move is possible on the Connect 4 board
Making a move on the Connect 4 board
Undoing a move on the Connect 4 board,
Checking if a player has won  “four in a row”
Checking if there are three in a row to seek out potential moves 
After these tools have been made the program will then ask for input from the user. Asking for the server ip of the Connect 4 game, then whether the user would like to join or play a game. Then if the user decides to join a game they will be prompted for a game id. The program will then connect to the game via the websockets module. If the user decides to create a game they will be connected to the server and be given a game session. 
The main loop of the program to play connect 4 has three possible cases it can do from the input it gets from the server. If the game has started, if the opponent has played a move, and if the game is won, lost, drawn or terminated. 
If the game has started it will calculate its move then update the board data then send that move back to the server.
If the opponent has played a move, the program will update the board data, calculate its move, update the board then send that move back to the server. 
If the game is won, lost, drawn or terminated the program terminates and turns itself off. 
To calculate its move the program will start by getting all possible board states after one move. If the move ends up in a win for the program it will play it, if it ends up in a win for the opponent it will block. If neither of these conditions are found, the program will then evaluate the positions and give it points. This is dependent on if there are potential wins in future board states, if there are more three in a row for better moves in the future. And the exact inverse is true if a move tends to lead to losses it will lose points. This will happen for all possible states after one move or one “layer”. This will happen up to the 6th layer of possible moves, or all possible positions that are 6 moves in the future. The points are then weighed to cut off and favor different possible moves/positions until it finds the move with the highest number of points. These points are arbitrarily set depending on how we want the program to  “behave” to favor some positions/patterns over another. This allows us to calibrate or change the AI to tend to look for different things. Or follow different principles in Connect 4. For example moves will be given more points if that move is near the middle of the board. Since it is considered a principle to control the center in Connect 4. 
3. 	RESULTS: What is your program able to do (or not do)?
 Our program resulted in an AI that successfully beat a human every time we played against it. When testing it with other group’s AI, during our program we found out that whoever AI goes first will increase the chance of winning tremendously. Due to the nature of the game of Connect 4. Overall we were astounded with the results of our AI considering the approach to design it.
4. 	DISCUSSION:  Did the program satisfy your goals? If not, can you say why? How did the program relate to anything we talked about in class? What improvements/extensions would you like to see?
In the end, we were able to satisfy our goals and create an AI that would win every game when it was tested against a human. Our program, in a way, acts like a brain by seeing all possible options on the board and following principles to find the best move to achieve the end goal of winning by mimicking the unique cognitive function of analyzing. This relates to the main core of the class by the relation between programming, machines and minds. Since our program to some extent is copying the human analysis/methodology of Connect 4. 

