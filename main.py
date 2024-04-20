from sys import stdin
import numpy as np


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
Representação interna de uma peça
'''
class Part:

    def __int__(self,string):
        self.guidance = string[1]
        self.type = string[0]

    def getype(self):
        return self.type

    def getguidance(self):
        return self.guidance
    
    def setguidance(self,guidance):
        self.guidance = guidance

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


class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        pass

    '''
    Retorna uma lista de ações que podem ser executadas a
    partir do estado passado como argumento.
    '''
    def actions(self, state: State):
        pass

    '''
    Retorna o estado resultante de executar a 'action' sobre
    'state' passado como argumento. A ação a executar deve ser uma
    das presentes na lista obtida pela execução de
    self.actions(state). 
    '''
    def result(self, state: State, action):
        pass

    '''
    Função heuristica utilizada para a procura A*.
    '''
    def h(self, node: Node):
        pass


'''
Lê a instância do problema do standard input (stdin)
e retorna uma instância da classe Board.
'''
@staticmethod
def parse_instance():
    lines = stdin.readlines().strip().split("\n")
    n = len(lines)
    parts = [lines[i].split("\t") for i in range(n)]
    board = Board(n,n,[[Part(string) for string in parts[i]] for i in range(n)])
    return board