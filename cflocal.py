#Runs the Local version of the 2 player connect 4 game

import cffunctions
import connectfour

def run():
    '''
    Runs the console-mode user interface from start to finish.
    '''
    
    _welcome_prompt()
    startup = cffunctions.startup_game()
   
    game = startup.game_s
    cffunctions.view_board(game)

    end = play_local(game)

    cffunctions.display_winner(end)

def play_local(game: cffunctions.GameState) -> int:
    '''
    Initiates the turn by turn game and returns the integer value of the
    winner once the game is ended. 
    '''

    end = 0
    while end == 0:
        
        cffunctions.displayTurn(game.turn)
        temp = cffunctions.finalize_move(game)
        game = temp.game_s
        

        cffunctions.view_board(game)
        end = connectfour.winner(game)

    return end


#Private Functions

def _welcome_prompt() -> None:
    '''
    Prints the welcome prompt for the Local Connect Four Game
    '''
    
    print('*************************************')
    print('* WELCOME TO CONNECT FOUR LOCAL 2P! *')
    print('*************************************')

    return None

if __name__ == '__main__':
    run()
