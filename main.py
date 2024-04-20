from sys import stdin
import numpy as np
from search import *

'''
Esta classe representa os estados utilizados nos algoritmos de procura.
'''
class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras inf """

'''
Representação interna de uma grelha de PipeMania.
'''
class Board:
    def __init__(self,parts):
        self.board = np.array(parts)

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        pass
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        pass
        
    def print_board(self):
        for i in self.board:
            for j in i:
                print(j, end=" ")
            print()
    
    '''
    Lê a instância do problema do standard input (stdin)
    e retorna uma instância da classe Board.
    '''
    @staticmethod
    def parse_instance():
        lines = stdin.readlines()
        parsedLines = []
        for line in lines:
            parsedLines.append(line.split())
        board = Board(parsedLines)
        return board

class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        ''' O construtor especifica o estado inicial. '''
        pass

    '''
    Retorna uma lista de ações que podem ser executadas a
    partir do estado passado como argumento.
    '''
    def actions(self, state: PipeManiaState):
        pass

    '''
    Retorna o estado resultante de executar a 'action' sobre
    'state' passado como argumento.
    '''
    def result(self, state: PipeManiaState, action):
        pass

    '''
    Função heuristica utilizada para a procura A*.
    '''
    def h(self, node: Node):
        pass

class Part:
    def __init__(self, string):
        self.identification = string[0]
        self.guidance = string[1]
        self.top = None
        self.bot = None
        self.right = None
        self.left = None
    
    


board = Board.parse_instance()
board.print_board()