#cfsockets consists the tools for socket handling required by the main function

from collections import namedtuple
import socket
import cffunctions
import connectfour

_SHOW_DEBUG_TRACE = False

CfConnection = namedtuple('CfConnection', ['socket', 'input', 'output'])

#HOST = 'circinus-32.ics.uci.edu'
#PORT = 4444


#EXCEPTIONS

class CfProtocolError(Exception):
    pass

#FUNCTIONS

def connect(host: str, port: int) -> CfConnection:
    '''
    Connects to a Connect Four server running on the given host and listening
    on the given port, returning a CfConnection object describing
    that connection if successful, or raising an exception if the attempt
    to connect fails.
    '''

    cf_socket = socket.socket()
    cf_socket.connect((host,port))

    cf_input = cf_socket.makefile('r')
    cf_output = cf_socket.makefile('w')
    
    return CfConnection(socket = cf_socket,
                        input = cf_input,output = cf_output)

def hello(connection: CfConnection, username: str) -> bool:
    '''
    Logs a user into the cf service over a previously-made connection.
    Returns True if logging in was successful and raises an exception
    if the expected response was not recieved. 
    '''
    _write_line(connection, f'I32CFSP_HELLO {username}')

    response = _read_line(connection)
    
    if response == f'WELCOME {username}':
        return True
    else:
        close(connection)
        raise CfProtocolError()

def grid_send(connection: CfConnection, cr: cffunctions.ColsRows) -> bool:
    '''
    The function sends the grid (columns and rows) to the specified server
    connection to play connect four on. If the response after doing so is
    unexpected, then connections are closed and an exception is raised.
    '''

    _write_line(connection, f'AI_GAME {cr.cols} {cr.rows}')

    line = _read_line(connection)

    if line == 'READY':
        return True
    else:
        close(connection)
        raise CfProtocolError()


def move_send(connection: CfConnection,
              move: cffunctions.currMove)-> None:
    '''
    Sends the users move via the currMove object type to the
    specified connection (server). 
    '''

    if move.move == 'D':
        _write_line(connection, f'DROP {move.col}')
    elif move.move == 'P':
        _write_line(connection, f'POP {move.col}')

    return None

def ai_move(connection: CfConnection) -> cffunctions.currMove:
    '''
    Reads the servers move by reading the line sent by the server
    and determines wheter it is a drop or a pop command. If it is neither,
    an exception is raised.
    '''

    line = _read_line(connection)
    line = line.split()
    if line[0] == 'DROP':
        return cffunctions.currMove(move = 'D', col = int(line[1]))

    elif line[0] == 'POP':
        return cffunctions.currMove(move = 'P', col = int(line[1]))
    else:
        close(connection)
        raise CfProtocolError()
   


def check_winner(game: connectfour.GameState,
                 connection: CfConnection)-> bool:
    '''
    Checks whether the server has declared a winner or is about to engage
    with the next move. If it is the users turn then it checks whether
    server sends a 'READY' and 'OKAY' when it is the servers turn. If the
    server returns 'INVALID' or if another message is read, an exception is
    raised. 
    '''
    
    line = _read_line(connection)
    if line == 'WINNER_RED' or line == 'WINNER_YELLOW':
        end = connectfour.winner(game)

        if line == 'WINNER_RED' and end == connectfour.RED:
            return True
        elif line == 'WINNER_YELLOW' and end == connectfour.YELLOW:
            return True
        else:
            #Contradicting Winners
            close(connection)
            raise CfProtocolError()
    elif line == 'READY' and game.turn == 1:
        return False
    elif line == 'OKAY' and game.turn == 2:
        return False
    elif line == 'INVALID':
        #Other functions make sure moves sent by the user are always valid
        #If server says its invalid then there is a misunderstanding
        close(connection)
        raise CfProtocolError()
    else:
        close(connection)
        raise CfProtocolError()
        
        
def close(connection: CfConnection)-> None:
    '''
    Closes the input and ouput of the socket and then the socket itself.
    '''
    
    connection.input.close()
    connection.output.close()
    connection.socket.close()
    


#Private Functions

def _read_line(connection: CfConnection) -> str:
    '''
    Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
     
    line = connection.input.readline()[:-1]
    if _SHOW_DEBUG_TRACE:
        print('RCVD: ' + line)

    return line

def _write_line(connection: CfConnection, line: str) -> None:
    '''
    Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    
    connection.output.write(line + '\r\n')
    connection.output.flush()

    if _SHOW_DEBUG_TRACE:
        print('SENT: ' + line)


