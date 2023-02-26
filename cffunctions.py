#Deals with the common functions used in the connect four game accross local
#and online.

import connectfour
from connectfour import GameState
from connectfour import InvalidMoveError
from collections import namedtuple


GameStartup = namedtuple('GameStartup', ['game_s', 'grid'])
currMove = namedtuple('currMove', ['move', 'col'])
LegalMove = namedtuple('legalMove', ['game_s', 'validity'])
ColsRows = namedtuple('ColsRows', ['cols', 'rows'])
FinalizedMove = namedtuple('FinalizedMove', ['game_s', 'action'])


def displayTurn(turn: int) -> None:
    '''
    Compares the integer parameter and displays whose turn it is.
    1 = RED and 2 = YELLOW.
    '''
    if turn == 1:
        print("RED'S TURN")
    elif turn == 2:
        print("YELLOW'S TURN")

    return None


def view_board(game_state: GameState) -> None:
    '''
    Takes the GameState object parameter and numbers the collumns and then
    displays each collumn to display the connect four board. 
    '''

    _number_spacing(connectfour.columns(game_state))
    
    rows = 0
    while rows < connectfour.rows(game_state):
        cols = 0
        while cols < connectfour.columns(game_state):
            _print_location(game_state.board[cols][rows])
            cols += 1
            
        print('\n')
        rows += 1

def grid_size_prompt() -> ColsRows:
    '''
    Prints the instructions and prompts the user to enter the Rows and
    Columns. Returns a ColsRows tuple with the rows and cols entered by
    the user.
    '''

    print('*****ENTER THE COLLUMNS AND ROWS FOR YOUR GRID!*****')
    print(f'NOTE: COLUMN RANGE IS {connectfour.MIN_COLUMNS} - {connectfour.MAX_COLUMNS} ', end = '')
    print(f'AND ROW RANGE IS {connectfour.MIN_ROWS} - {connectfour.MAX_ROWS}')
    
    c = int(input('Enter Collumns: '))
    r = int(input('Enter Rows: '))
    

    return ColsRows(cols= c, rows= r)

def startup_game() -> GameStartup:
    '''
    Starts up the game by asking the user enter the grid and establishing a new game.
    If the grid is invalid, the user is shown an error message and is prompted to re-enter
    the grid. Returns a GameStartup namedtuple object with the game state and grid.
    '''

    validity = False
    
    while validity == False:
        
        try:
            grid = grid_size_prompt()
            game = connectfour.new_game(grid.cols,grid.rows)
            validity = True
        except ValueError:
            print('ERROR. RETRY!')
        
    return GameStartup(game_s = game, grid = grid)


def move_options(game_state: GameState)-> currMove:
    '''
    Prompts the user to enter DROP or POP depending on the action they want to
    make for their move. If the syntax is incorrect, the user is given an error
    message and is promoted to re-enter their choice. The user is then prompted to
    enter the column number to apply the action for their move. If the column
    number entered is above or below the given range, then an error message is
    shown and the user is promted to re enter the column number. The function then
    returns a currMove namedtuple object including the move 'm' and column 'col'.
    '''
    
    move_str = ''
    while not move_str.startswith('DROP') or not move_str.startswith('POP'):
        move_str = input('ENTER "DROP" OR "POP" FOR THE ACTION IN THIS MOVE: ')
        move_str = move_str.upper()
        if move_str.startswith('DROP'):
            m = 'D'
            break
        elif move_str.startswith('POP'):
            m = 'P'
            break
        else:
            print('ERROR: INVALID ACTION. RETRY')

    num = -1
    while num < 1 or num > connectfour.columns(game_state):
        num = int(input('ENTER COLUMN NUMBER FOR YOUR MOVE: '))
        if num < 1 or num > connectfour.columns(game_state):
            print('ERROR: INVALID COLUMN. RETRY')

     
    return currMove(move = m, col = num)

def initiate_move(game_state: GameState, current_move: currMove) -> LegalMove:
    '''
    Initiates the move sent by the user via the currMove object and attempts
    to make changes to the grid. The game state gets updated with a pop or a
    drop command if valid and returns the modified game state. If the move is
    invalid, it alerts the user of an invalid move and returns the unchanged
    game state back. The return is done via LegalMove namedtuple object
    consisting game state 'game_s' and validity of the move 'validity'.
    '''
    
    try:
        if current_move.move == 'D':
            game_state = connectfour.drop(game_state, current_move.col - 1)
        elif current_move.move == 'P':
            game_state = connectfour.pop(game_state, current_move.col - 1)
        
        return LegalMove(game_s = game_state, validity = True)
    except InvalidMoveError:
        print('ERROR: INVALID MOVE.')
        return LegalMove(game_s = game_state, validity = False)
        
def finalize_move(game_state: GameState) -> GameState:
    '''
    Responsible to make sure the user enters valid commands for the connect four
    board and repeats the loop until the right commands are entered. Once the move
    valid and registered, the function then returns a FinalizedMove namedtuple
    object consisting the new gamestate and the action taken by the user during the
    move.
    '''

    validity = False
    while validity == False:
        
        action = move_options(game_state)
        temp = initiate_move(game_state, action)
        validity = temp.validity
        game_state = temp.game_s

    return FinalizedMove(game_s =game_state, action= action)

def display_winner(winner: int) -> None:
    '''
    Prints the winner according to the int in the parameter.
    1 = Red and 2 = Yellow.
    '''

    if winner == connectfour.RED:
        print('RED WINS')
    elif winner == connectfour.YELLOW:
        print('YELLOW WINS')

# PRIVATE FUNCTIONS

def _print_location(val: int) -> None:
    '''
    Prints R, Y, or . according to the value in the parameter for the
    display on the connectfour board. 
    '''
    if val == 0:
        print('.', end = '  ')
    elif val == 1:
        print('R', end = '  ')
    else:
        print('Y', end = '  ')

    return None

def _number_spacing(limit: int) -> None:
    '''
    Prints amount of spacing required between the numbers for the corresponding
    columns. If the number is of two digits then there should 1 space follwing it,
    else there should be a double space.
    '''
    num = 1
    while num <= limit:
        print(num, end = '')
        if num >=10:
            print(' ', end = '')
        else:
            print('  ', end = '')
        num += 1
    print('\n')        
    return None




        

    
