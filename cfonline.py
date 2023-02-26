#CONNECT FOUR VS AI ONLINE 

import cffunctions
import connectfour
import cfsockets

HOST = 'circinus-32.ics.uci.edu'
PORT = 4444

def run_cf():
    '''
    Runs the console-mode user interface from start to finish.
    '''

    _welcome_prompt()
    connection = cfsockets.connect(HOST,PORT)
    
    username = _request_username()
    cfsockets.hello(connection, username)

    startup = cffunctions.startup_game()
    game = startup.game_s
    grid = startup.grid
    
    cfsockets.grid_send(connection, grid)
    
    cffunctions.view_board(game)

    game = play_ai(game, connection)
        
    cffunctions.display_winner(connectfour.winner(game))


        
def play_ai(game: cffunctions.GameState,
                   connection: cfsockets.CfConnection) -> cffunctions.GameState:
    '''
    Initiates the turn by turn game and returns the final game board when the
    game has ended. The function iterates between the client and the servers moves
    until one of them is declared the winner. If an illegal move is detected from
    the server, connection is terminated. 
    '''
    winner = False

    while winner == False:
        cffunctions.displayTurn(game.turn)

        temp = cffunctions.finalize_move(game)
        game = temp.game_s
        
        cfsockets.move_send(connection, temp.action) 
        cffunctions.view_board(game)
        
        winner = cfsockets.check_winner(game, connection)
        if winner == True:
            break

        cffunctions.displayTurn(game.turn)
        
        ai_move = cfsockets.ai_move(connection)
        ai_legal_move = cffunctions.initiate_move(game, ai_move)
        if ai_legal_move.validity == False:
            cfsockets.close(connection)
            raise cfsockets.CfProtocolError()
        
        game = ai_legal_move.game_s
        cffunctions.view_board(game)
        winner = cfsockets.check_winner(game, connection)
        


    return game


def _welcome_prompt() -> None:
    '''
    Prints the welcome prompt for the Connect Four Game vs AI
    '''
    
    print('*********************************')
    print('* WELCOME TO CONNECT FOUR VS AI *')
    print('*********************************')
    print('*****YOU = RED | AI = YELLOW*****')

    return None

def _request_username()-> str:
    '''
    Requests the user to enter a username in order to play. If the user
    enters an empty username or a username with spaces (or tabs), it asks
    the user to enter it again. 
    '''

    validity = False
    while validity == False:
        user = input('Enter username: ')
        if len(user.split()) < 1:
            print('ERROR. CANNOT ACCEPT EMPTY USERNAME')
        elif len(user.split()) > 1:
            print('ERROR. USERNAME SHOULD NOT CONSIST SPACES OR TABS')
        else:
            validity = True

    return user


if __name__ == '__main__':
    run_cf()

