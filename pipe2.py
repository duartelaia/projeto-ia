import numpy as np
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# Grupo 05:
# ist1106876 Duarte Laia
# ist1106929 Eduardo Silva

# Used for rotations
OFF = 0
ON = 1
UNKNOWN = 2

# Rotation: [top, bot, right, left]
pipes_to_bits = {
    'F':{'C':(ON, OFF, OFF, OFF),
         'B':(OFF, ON, OFF, OFF),
         'E':(OFF, OFF, OFF, ON),
         'D':(OFF, OFF, ON, OFF)},

    'B':{'C':(ON, OFF, ON, ON),
         'B':(OFF, ON, ON, ON),
         'E':(ON, ON, OFF, ON),
         'D':(ON, ON, ON, OFF)},

    'V':{'C':(ON, OFF, OFF, ON),
         'B':(OFF, ON, ON, OFF),
         'E':(OFF, ON, OFF, ON),
         'D':(ON, OFF, ON, OFF)},

    'L':{'H':(OFF, OFF, ON, ON),
         'V':(ON, ON, OFF, OFF)},
}

bits_to_pipes = {
    (ON, OFF, OFF, OFF):'FC',
    (OFF, ON, OFF, OFF):'FB',
    (OFF, OFF, OFF, ON):'FE',
    (OFF, OFF, ON, OFF):'FD',

    (ON, OFF, ON, ON):'BC',
    (OFF, ON, ON, ON):'BB',
    (ON, ON, OFF, ON):'BE',
    (ON, ON, ON, OFF):'BD',

    (ON, OFF, OFF, ON):'VC',
    (OFF, ON, ON, OFF):'VB',
    (OFF, ON, OFF, ON):'VE',
    (ON, OFF, ON, OFF):'VD',

    (OFF, OFF, ON, ON):'LH',
    (ON, ON, OFF, OFF):'LV'
}

def get_all_rotations(pipe):
    return list(pipes_to_bits[pipe[0]].values())

def get_possible_rotations(pipe, top, bot, right, left):
    bits = (top, bot, right, left)
    possibilities = get_all_rotations(pipe)
    for i in range(4):
        j = 0
        while(j < len(possibilities)):
            # Remove a possibility if the bit we want is ON
            # and on the possibility is OFF, and vice-versa
            if(bits[i] == ON and possibilities[j][i] == OFF):
                possibilities.pop(j)
            elif(bits[i] == OFF and possibilities[j][i] == ON):
                possibilities.pop(j)
            else:
                j += 1
    return possibilities

def parse_pipe_to_bits(pipe):
    return pipes_to_bits[pipe[0]][pipe[1]]

'''
Represents the states used in the searching algorithms
'''
class PipeManiaState:
    state_id = 0

    def __init__(self, board, right_counter):
        self.board = board
        self.close = False
        self.right_counter = right_counter
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        '''
        Used in case of a draw in the list managment of opened in 
        informed searches
        '''
        return self.id < other.id

'''
Representação interna de uma grelha de PipeMania.
'''
class Board:
    def __init__(self,board):
        self.board = board
        self.lines = len(board)
        self.columns = len(board[0])

    def get_value(self, row: int, col: int) -> str:
        '''
        Returns the pipe on a specific position of the board
        '''
        return parse_pipe_to_bits(self.board[row][col])
    
    def get_id(self, row: int, col: int) -> str:
        '''
        Returns the pipe on a specific position of the board
        '''
        return self.board[row][col][:2]
    
    def is_right(self, row: int, col: int) -> str:
        '''
        Returns true if a pipe on a specific position of the board is right
        '''
        return bool(int(self.board[row][col][2]))
    
    def set_right(self, row: int, col: int, val:str) -> str:
        '''
        Sets a pipe to rotated
        '''
        self.board[row][col] = self.board[row][col][:2]+val
    
    def rotate(self, action):
        '''
        Rotates a pipe based on an action
        '''
        position = action[0]
        rotation = tuple(action[1])
        self.board[position[0]][position[1]] = bits_to_pipes[rotation] + self.board[position[0]][position[1]][2]


    def adjacent_values(self, row: int, col: int) -> tuple:
        '''
        Returns the pipes directly up and down
        The return values are either a Pipe or None
        '''
        top = parse_pipe_to_bits(self.board[row - 1][col]) if row - 1 >= 0 else None
        bot = parse_pipe_to_bits(self.board[row + 1][col]) if row + 1 < len(self.board) else None
        left = parse_pipe_to_bits(self.board[row][col - 1]) if col - 1 >= 0 else None
        right = parse_pipe_to_bits(self.board[row][col + 1]) if col + 1 < len(self.board[row]) else None

        return (top, bot, right, left)
    
    def adjacent_positions(self, row: int, col: int) -> tuple:
        '''
        Returns the positions directly up and down
        The return values are either a Pipe or None
        '''
        top = (row - 1, col) if row - 1 >= 0 else None
        bot = (row + 1,col) if row + 1 < len(self.board) else None
        left = (row,col - 1) if col - 1 >= 0 else None
        right = (row,col + 1) if col + 1 < len(self.board[row]) else None

        return (top, bot, right, left)
    
    def print_board_id(self):
        for i in range(self.lines):
            for j in range(self.columns):
                if j != 0:
                    print('\t', end='')
                print(self.board[i][j][:2],end='')
            print()
    
    def print_board_right(self):
        for i in range(self.lines):
            for j in range(self.columns):
                if j != 0:
                    print('\t', end='')
                print(self.board[i][j],end='')
            print()

    @staticmethod
    def copy_board(board):
        return Board(np.copy(board.board))

    '''
    Reads the instance of the problem from stdin and
    returns an instance of type Board
    '''
    @staticmethod
    def parse_instance():
        lines = sys.stdin.readlines()
        parsedLines = []
        for line in lines:
            current_line = line.split()
            parsed_current_line = []
            for pipe in current_line:
                parsed_current_line.append(pipe+'0')
            parsedLines.append(parsed_current_line)
        
        board = Board(np.array(parsedLines, dtype='<U3'))
        return board

def get_possibilities(state, position):
    # Get the adjacent values
    board = state.board
    adjacent_values = board.adjacent_values(position[0], position[1])
    adjacent_positions = board.adjacent_positions(position[0], position[1])

    top_rot = bot_rot = right_rot = left_rot = OFF

    # Get the possible rotations
    if adjacent_values[0]:
        top_rot = adjacent_values[0][1] if board.is_right(adjacent_positions[0][0], adjacent_positions[0][1]) else UNKNOWN
    if adjacent_values[1]:
        bot_rot = adjacent_values[1][0] if board.is_right(adjacent_positions[1][0], adjacent_positions[1][1]) else UNKNOWN
    if adjacent_values[2]:
        right_rot = adjacent_values[2][3] if board.is_right(adjacent_positions[2][0], adjacent_positions[2][1]) else UNKNOWN
    if adjacent_values[3]:
        left_rot = adjacent_values[3][2] if board.is_right(adjacent_positions[3][0], adjacent_positions[3][1]) else UNKNOWN

    return get_possible_rotations(board.get_id(position[0], position[1]),top_rot, bot_rot, right_rot, left_rot)

'''
Function that makes inferences on the board, based
on a starting position
Returns False if the board is invalid, otherwhise
returns True
'''
def make_inferences(state, first_pos):
    board = state.board
    stack = [first_pos]
    max_count = (state.board.columns*state.board.lines) * 1
    count = 0

    while len(stack) > 0 and count <= max_count:
        count += 1
        current_pos = stack.pop()
        if(not board.is_right(current_pos[0], current_pos[1])):
            state.right_counter += 1

        board.set_right(current_pos[0], current_pos[1], '1')

        adjacent_values = board.adjacent_values(current_pos[0], current_pos[1])
        adjacent_positions = board.adjacent_positions(current_pos[0], current_pos[1])
        possibilities = get_possibilities(state, current_pos)
        
        # If there is only one possibility, rotate the pipe and add the adjacent pipes to the stack
        if len(possibilities) == 1:
            board.rotate([current_pos,possibilities[0]])
            if adjacent_values[0] and not board.is_right(adjacent_positions[0][0], adjacent_positions[0][1]):
                stack.append((current_pos[0] - 1, current_pos[1]))
            if adjacent_values[1] and not board.is_right(adjacent_positions[1][0], adjacent_positions[1][1]):
                stack.append((current_pos[0] + 1, current_pos[1]))
            if adjacent_values[2] and not board.is_right(adjacent_positions[2][0], adjacent_positions[2][1]):
                stack.append((current_pos[0], current_pos[1] + 1))
            if adjacent_values[3] and not board.is_right(adjacent_positions[3][0], adjacent_positions[3][1]):
                stack.append((current_pos[0], current_pos[1] - 1))
        elif len(possibilities) == 0:
            state.right_counter -= 1
            return False
        else:
            board.set_right(current_pos[0], current_pos[1], '0')
            state.right_counter -= 1
    return True

'''
Problem to be solved by search
'''
class PipeMania(Problem):
    def __init__(self, initial_board: Board):
        initial_state = PipeManiaState(initial_board, 0)
        super().__init__(initial_state)

    '''
    Returns a list of actions that can be executed from
    the state passed as argument
    An action is a list with the position of the pipe
    and the rotation to be executed
    '''
    def actions(self, state: PipeManiaState):

        if state.close:
            return []

        board = state.board

        wrong_pipe_pos = 0
        wrong_pipe_possibilities = [0, 0, 0, 0, 0]

        # Check if there is a pipe which isn't right
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if not board.is_right(i, j):
                    current_wrong_pipe_pos = (i, j)
                    current_wrong_pipe_possibilities = get_possibilities(state, current_wrong_pipe_pos)
                    if len(current_wrong_pipe_possibilities) < len(wrong_pipe_possibilities):
                        wrong_pipe_possibilities = current_wrong_pipe_possibilities
                        wrong_pipe_pos = current_wrong_pipe_pos
                    
                    if (len(wrong_pipe_possibilities) == 0):
                        return []
                    
                    elif (len(wrong_pipe_possibilities) == 1):
                        # Make inferences on the board
                        if not make_inferences(state, wrong_pipe_pos):
                            return []

        if wrong_pipe_pos == 0:
            return []

        if(not board.is_right(wrong_pipe_pos[0], wrong_pipe_pos[1])):
                state.right_counter += 1
        board.set_right(wrong_pipe_pos[0], wrong_pipe_pos[1], '1')
        
        return [[wrong_pipe_pos, possibility] for possibility in wrong_pipe_possibilities]
            

    '''
    Returns the resulting state of executing an action on
    the 'state' passed as argument
    '''
    def result(self, state: PipeManiaState, action):
        new_board = Board.copy_board(state.board)
        new_board.rotate(action)
        return PipeManiaState(new_board, state.right_counter)
    
    '''
    Returns true if the state passed as argument is a goal state.
    '''
    def goal_test(self, state: PipeManiaState):
        stack = [(0, 0)]  
        visited = set()
        
        if state.right_counter != state.board.columns*state.board.lines:
            return False

        while stack:
            row, col = stack.pop()
            visited.add((row, col))

            # Get the current pipe and its adjacent values
            current_pipe = state.board.get_value(row, col)
            adjacent_values = state.board.adjacent_values(row, col)

            # Check if there is an invalid connection. If there is a connection and it isnt invalid, add to the stack
            if (adjacent_values[0] is None and current_pipe[0] == ON) or (adjacent_values[0] and (adjacent_values[0][1] != current_pipe[0])):
                return False
            elif current_pipe[0] == ON and (row - 1, col) not in visited:
                stack.append((row - 1, col))

            if (adjacent_values[1] is None and current_pipe[1] == ON) or (adjacent_values[1] and (adjacent_values[1][0] != current_pipe[1])):
                return False
            elif current_pipe[1] == ON and (row + 1, col) not in visited:
                stack.append((row + 1, col))

            if (adjacent_values[2] is None and current_pipe[2] == ON) or (adjacent_values[2] and (adjacent_values[2][3] != current_pipe[2])):
                return False
            elif current_pipe[2] == ON and (row, col + 1) not in visited:
                stack.append((row, col + 1))

            if (adjacent_values[3] is None and current_pipe[3] == ON) or (adjacent_values[3] and (adjacent_values[3][2] != current_pipe[3])):
                return False
            elif current_pipe[3] == ON and (row, col - 1) not in visited:
                stack.append((row, col - 1))

        if state.right_counter != len(visited):
            state.close = True

        return len(visited) == state.board.columns*state.board.lines

    '''
    Heuristic function used in A*
    '''
    def h(self, node: Node):
        board = node.state.board
        if not node.action:
            return 0
        position = node.action[0]
        rotation = node.action[1]

        adjacent_values = board.adjacent_values(position[0], position[1])
        off_count = 0
        if adjacent_values[0] and adjacent_values[0][1] == ON == rotation[0]:
            off_count += adjacent_values[0].count(OFF)
        if adjacent_values[1] and adjacent_values[1][0] == ON == rotation[1]:
            off_count += adjacent_values[1].count(OFF)
        if adjacent_values[2] and adjacent_values[2][3] == ON == rotation[2]:    
            off_count += adjacent_values[2].count(OFF)
        if adjacent_values[3] and adjacent_values[3][2] == ON == rotation[3]:
            off_count += adjacent_values[3].count(OFF)
                
        return off_count

if __name__ == "__main__":
    b1 = Board.parse_instance()
    problem = PipeMania(b1)
    goal_node = greedy_search(problem)
    if goal_node:
        goal_node.state.board.print_board_id()
    else:
        print("tamale")