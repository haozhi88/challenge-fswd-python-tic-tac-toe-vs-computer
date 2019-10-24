"""""""""""""""""""""
Import libraries
"""""""""""""""""""""
import random

"""""""""""""""""""""
Constant variables
"""""""""""""""""""""
WIN_COMBINATION = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]
TOTAL_SQUARES = 9
PLAYER_NONE = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
OPPONENT_HUMAN = 0
OPPONENT_DUMB = 1
OPPONENT_SMART = 2
PLAY = ["-","X","O"]

"""""""""""""""""""""
Global variables
"""""""""""""""""""""
board = [
    0,0,0,
    0,0,0,
    0,0,0
]
steps = 0
current_player = PLAYER_ONE
current_opponent = OPPONENT_HUMAN

"""""""""""""""""""""
Functions: Display
"""""""""""""""""""""
def display_board():
    print("Here is the output:")
    for row in range(0,3):
        row_string = "["
        for index, col in enumerate(board[row*3:row*3+3]):
            row_string += f"'{PLAY[col]}'"
            if index < 2:
                row_string += ","      
        row_string += "]"
        print(row_string)

def get_player_display():
    global current_player, current_opponent
    if current_player == PLAYER_ONE:
        return f"Player {current_player}"
    else:
        if current_opponent == OPPONENT_HUMAN:
            return f"Player {current_player}"
        else:
            return f"Computer"

def get_winning_display():
    global current_player, current_opponent
    if current_player == PLAYER_ONE:
        return f"Player {current_player} won!"
    else:
        if current_opponent == OPPONENT_HUMAN:
            return f"Player {current_player} won!"
        else:
            return f"Computer won!"

"""""""""""""""""""""
Functions: Input
"""""""""""""""""""""
def get_input():
    global board, steps, current_player

    print("=========")
    print(get_player_display())
    print("=========")

    while True:
        print("Put in your X coordinate:")
        coordinate_x = input()
        print("Put in your Y coordinate:")
        coordinate_y = input()

        if not coordinate_x.isdigit():
            print("[Alert] Coordinate X is not a number. Please enter again!")
        elif not coordinate_y.isdigit():
            print("[Alert] Coordinate Y is not a number. Please enter again!")
        else:
            x = int(coordinate_x)
            y = int(coordinate_y)

            if x > 2:
                print("[Alert] Coordinate X is out of range. Please enter between 0-2!")
            elif y > 2:
                print("[Alert] Coordinate Y is out of range. Please enter between 0-2!")
            else:
                index = y*3+x
                if board[index] == PLAYER_NONE:
                    return index
                else:
                    print("[Alert] This section is already played. Please enter again!")

def get_replay():
    while True:
        print("Play again? (Y/N)")
        userinput = input().upper()

        if userinput == "Y":
            return True
        elif userinput == "N":
            return False
        else:
            print("Unrecognized command. Please enter again!")

"""""""""""""""""""""
Functions: Game Logic
"""""""""""""""""""""
def init_game():
    global board, steps, current_player, current_opponent
    for index, element in enumerate(board):
        board[index] = PLAYER_NONE
    current_player = PLAYER_ONE
    current_opponent = choose_player()
    steps = 0

def choose_player():
    while True:
        print("Choose player")
        print("  0: Human")
        print("  1: Dumb computer")
        print("  2: Smart computer")
        userinput = input().upper()

        if userinput == "0":
            return OPPONENT_HUMAN
        elif userinput == "1":
            return OPPONENT_DUMB
        elif userinput == "2":
            return OPPONENT_SMART
        else:
            print("Unrecognized command. Please enter again!")

def check_game(check_player):
    global WIN_COMBINATION, board, steps
    result = 0

    # Check for win
    for i, i_element in enumerate(WIN_COMBINATION):
        count = 0
        for j, j_element in enumerate(range(0,3)):
            index = WIN_COMBINATION[i][j]
            if board[index] == check_player:
                count += 1
        
        if count == 3:
            result = 1
            break
    
    # Check for tie
    if result == 0 and steps == 8:
        result = 2

    return result  # 0: continue, 1: win, 2: tie

def update_game():
    global current_player, steps
         
    steps += 1
    if current_player == PLAYER_ONE:
        current_player = PLAYER_TWO
    else:
        current_player = PLAYER_ONE

def play(player, position):
    status = False
    board[position] = player
    display_board()

    result = check_game(player)
    if result == 0:
        # continue
        update_game()
        status = True
    elif result == 1: 
        # win
        print(get_winning_display())
    elif result == 2: 
        # tie
        print(f"It's a tie.")
        
    return status

def player_move(player, position):
    global current_opponent
    status = play(player, position)

    if status:
        if current_opponent != OPPONENT_HUMAN:
            status = computer_move(current_opponent)

    return status

def computer_move(opponent):
    print("=========")
    print("Computer")
    print("=========")

    if opponent == OPPONENT_DUMB:
        position = generate_random_move()
    elif opponent == OPPONENT_SMART:
        position = generate_smart_move()
    else:
        print("ERROR: generate_smart_move")

    return play(current_player, position)

def generate_random_move():
    position = -1
    remain = 0

    for i, i_element in enumerate(board):
        if board[i] == 0:
            remain += 1

    if remain:
        while position < 0:
            index = random.randint(0,TOTAL_SQUARES-1)
            if board[index] == PLAYER_NONE:
                position = index

    if position == -1:
        print("ERROR: generate_random_move")

    return position

def generate_smart_move():
    player_one_min_info = get_min_info(PLAYER_ONE)
    player_two_min_info = get_min_info(PLAYER_TWO)
    position = -1

    if player_two_min_info["value"] == 1:
        # I have last step to win, play it
        position = get_last_win_move(player_two_min_info)
    elif player_one_min_info["value"] == 1:
        # Opponent has last step to win, stop him
        position = get_last_win_move(player_one_min_info)
    else:
        # Otherwise, play the move with best chances to win
        position = get_best_win_move(player_two_min_info)

    if position == -1:
        print("ERROR: generate_smart_move")

    return position

def get_min_info(player):
    global WIN_COMBINATION, board

    min_info = {
    "path": [0,0,0,0,0,0,0,0],
    "index": 0,
    "value": 3
    }

    for i, i_element in enumerate(WIN_COMBINATION):
        count = 0
        for j, j_element in enumerate(range(0,3)):
            index = WIN_COMBINATION[i][j]
            if board[index] == PLAYER_NONE:
                count += 1
            elif board[index] != player:
                count = -1
                break
        
        if count == -1:
            # invalid path because opponent has played
            min_info["path"][i] = -1 
        else:
            # count of steps to win
            min_info["path"][i] = count
            if count < min_info["value"]:
                min_info["index"] = i
                min_info["value"] = count

    return min_info

def get_last_win_move(min_info):
    global WIN_COMBINATION, board
    position = -1
    
    for i, i_element in enumerate(range(0,3)):
        index = WIN_COMBINATION[min_info["index"]][i]
        if board[index] == PLAYER_NONE:
            position = index
            break

    if position == -1:
        print("ERROR: get_last_win_move")

    return position

def get_best_win_move(min_info):
    global WIN_COMBINATION, board
    win_steps_of_each_position = [0,0,0,0,0,0,0,0,0]

    # Look for path with least steps to win
    for i, i_element in enumerate(min_info["path"]):
        if min_info["path"][i] == min_info["value"]:
            for j, j_element in enumerate(range(0,3)):
                index = WIN_COMBINATION[i][j]
                if board[index] != PLAYER_NONE:
                    win_steps_of_each_position[i] += 1

    # Among the paths, look for position with maximum chance to win
    position = -1
    max_value = -1

    for i, i_element in enumerate(win_steps_of_each_position):
        if board[i] == PLAYER_NONE:
            if win_steps_of_each_position[i] > max_value:
                max_value = win_steps_of_each_position[i]
                position = i
            elif win_steps_of_each_position[i] == max_value:
                # If multiple max_value occurs, randomly pick one
                if random.randint(0,7) == 1: # magic number: 7, no specific purpose
                    max_value = win_steps_of_each_position[i]
                    position = i

    if position == -1:
        print("ERROR: get_best_win_move")

    return position

"""""""""""""""""""""
Main program
"""""""""""""""""""""

init_game()
status = True

while True:
    if status == True:
        position = get_input()
        status = player_move(current_player, position)
    else:
        if get_replay():
            # new game
            init_game()
            status = True
        else:
            # end game
            break

