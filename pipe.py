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

'''
Representation of each piece on the board
'''
class Pipe:
    def __init__(self, string):
        self.identification = string[0]
        self.guidance = string[1]
        self.is_right = False
        self.top = OFF
        self.bot = OFF
        self.right = OFF
        self.left = OFF
    
    def guidance_to_bits(self):
        '''
        Changes the top, bot, right and left bits
        based on the current guidance
        The bits can be: ON, OFF
        '''
        raise NotImplementedError

    def bits_to_guidance(self):
        '''
        Changes the guidance based on the bits
        '''
        raise NotImplementedError
    
    def rotation_posibilities(self, top, bot, right, left):
        '''
        Returns every possibility of rotations so that
        it matches the desired position
        The arguments can be: ON, OFF, UNKNOWN
        '''
        raise NotImplementedError
    
    '''
    Rotates the pipe based on the arguments
    '''
    def rotate(self, bits):
        [top, bot, right, left] = bits
        self.top = top
        self.bot = bot
        self.right = right
        self.left = left
        self.bits_to_guidance()

    def verify_posibilities(self, possibilities, bits):
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

    def get_pipe_bits(self):
        return (self.top, self.bot, self.right, self.left)

    def get_pipe_id(self):
        return self.identification+self.guidance
    
    def print_parser(self, i):
        return '1' if i == ON else '.'

    def print_pipe_id(self):
        print(self.identification + self.guidance, end='')
    
    def get_pipe_representation(self):
        return ('. '+self.print_parser(self.top)+' .', self.print_parser(self.left)+' 1 '+self.print_parser(self.right), '. '+self.print_parser(self.bot)+' .')

    @staticmethod
    def copy_pipe(pipe):
        new_pipe = Pipe.create_pipe(pipe.get_pipe_id())
        new_pipe.is_right = pipe.is_right
        return new_pipe

    @staticmethod
    def create_pipe(string):
        if(string[0] == 'F'):
            return ClosePipe(string)
        if(string[0] == 'B'):
            return BifPipe(string)
        if(string[0] == 'V'):
            return CurvePipe(string)
        if(string[0] == 'L'):
            return ConPipe(string)

class ClosePipe(Pipe):
    def __init__(self, string):
        super().__init__(string)
        self.guidance_to_bits()

    def guidance_to_bits(self):
        if(self.guidance == 'C'):
            self.top = ON
            self.left = self.right = self.bot = OFF
        elif(self.guidance == 'B'):
            self.bot = ON
            self.left = self.right = self.top = OFF
        elif(self.guidance == 'E'):
            self.left = ON
            self.bot = self.right = self.top = OFF
        elif(self.guidance == 'D'):
            self.right = ON
            self.left = self.bot = self.top = OFF
    
    def bits_to_guidance(self):
        if(self.top == ON):
            self.guidance = 'C'
        elif(self.bot == ON):
            self.guidance = 'B'
        elif(self.left == ON):
            self.guidance = 'E'
        elif(self.right == ON):
            self.guidance = 'D'
    
    def rotation_posibilities(self, top, bot, right, left):
        bits = (top, bot, right, left)
        possibilities = [[ON, OFF, OFF, OFF], [OFF, ON, OFF, OFF],
                         [OFF, OFF, ON, OFF], [OFF, OFF, OFF, ON]]

        return super().verify_posibilities(possibilities, bits)
    
class BifPipe(Pipe):

    def __init__(self, string):
        super().__init__(string)
        self.guidance_to_bits()

    def guidance_to_bits(self):
        if(self.guidance == 'C'):
            self.bot = OFF
            self.left = self.right = self.top = ON
        elif(self.guidance == 'B'):
            self.top = OFF
            self.left = self.right = self.bot = ON
        elif(self.guidance == 'E'):
            self.right = OFF
            self.bot = self.left = self.top = ON
        elif(self.guidance == 'D'):
            self.left = OFF
            self.right = self.bot = self.top = ON
    
    def bits_to_guidance(self):
        if(self.top == OFF):
            self.guidance = 'B'
        elif(self.bot == OFF):
            self.guidance = 'C'
        elif(self.left == OFF):
            self.guidance = 'D'
        elif(self.right == OFF):
            self.guidance = 'E'
    
    def rotation_posibilities(self, top, bot, right, left):
        bits = (top, bot, right, left)
        possibilities = [[OFF, ON, ON, ON], [ON, OFF, ON, ON],
                         [ON, ON, OFF, ON], [ON, ON, ON, OFF]]
        
        return super().verify_posibilities(possibilities, bits)
    
class CurvePipe(Pipe):
    def __init__(self, string):
        super().__init__(string)
        self.guidance_to_bits()

    def guidance_to_bits(self):
        if(self.guidance == 'C'):
            self.bot = self.right = OFF
            self.left = self.top = ON
        elif(self.guidance == 'B'):
            self.bot = self.right = ON
            self.left = self.top = OFF
        elif(self.guidance == 'E'):
            self.bot = self.left = ON
            self.right = self.top = OFF
        elif(self.guidance == 'D'):
            self.bot = self.left = OFF
            self.right = self.top = ON
    
    def bits_to_guidance(self):
        if(self.top == ON and self.left == ON):
            self.guidance = 'C'
        elif(self.bot == ON and self.right == ON):
            self.guidance = 'B'
        elif(self.left == ON and self.bot == ON):
            self.guidance = 'E'
        elif(self.top == ON and self.right == ON):
            self.guidance = 'D'
    
    def rotation_posibilities(self, top, bot, right, left):
        bits = (top, bot, right, left)
        possibilities = [[ON, OFF, OFF, ON], [OFF, ON, ON, OFF],
                         [OFF, ON, OFF, ON], [ON, OFF, ON, OFF]]
        
        return super().verify_posibilities(possibilities, bits)

class ConPipe(Pipe):
    def __init__(self, string):
        super().__init__(string)
        self.guidance_to_bits()

    def guidance_to_bits(self):
        if(self.guidance == 'H'):
            self.bot = self.top = OFF
            self.left = self.right = ON
        elif(self.guidance == 'V'):
            self.bot = self.top = ON
            self.left = self.right = OFF
    
    def bits_to_guidance(self):
        if(self.top == ON and self.bot == ON):
            self.guidance = 'V'
        elif(self.left == ON and self.right == ON):
            self.guidance = 'H'
    
    def rotation_posibilities(self, top, bot, right, left):
        bits = (top, bot, right, left)
        possibilities = [[ON, ON, OFF, OFF], [OFF, OFF, ON, ON]]

        return super().verify_posibilities(possibilities, bits)

'''
Represents the states used in the searching algorithms
'''
class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
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
    def __init__(self,parts):
        self.board = np.array(parts)

    def get_value(self, row: int, col: int) -> Pipe:
        '''
        Returns the pipe on a specific position of the board
        '''
        return self.board[row][col]

    def adjacent_values(self, row: int, col: int) -> tuple:
        '''
        Returns the pieces directly up and down
        The return values are either a Pipe or None
        '''
        top = self.board[row - 1][col] if row - 1 >= 0 else None
        bot = self.board[row + 1][col] if row + 1 < len(self.board) else None
        left = self.board[row][col - 1] if col - 1 >= 0 else None
        right = self.board[row][col + 1] if col + 1 < len(self.board[row]) else None

        return (top, bot, right, left)

    def print_board(self):
        for i in self.board:
            for j in range(3):
                for k in range(len(i)):
                    print(i[k].get_pipe_representation()[j], end='|')
                print()
            print('-----+'*len(self.board[0]))
    
    def print_board_id(self):
        for i in self.board:
            for j in range(len(i)):
                if j != 0:
                    print('\t', end='')
                i[j].print_pipe_id()
            print()
    
    @staticmethod
    def copy_board(board):
        line = len(board.board)
        col = len(board.board[0])
        new_board = [[0 for i in range(col)] for j in range(line)]
        for i in range(line):
            for j in range(col):
                new_board[i][j] = Pipe.copy_pipe(board.board[i][j])

        return Board(new_board)

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
                parsed_current_line.append(Pipe.create_pipe(pipe))
            parsedLines.append(parsed_current_line)
        
        board = Board(parsedLines)
        return board

'''
Problem to be solved by search
'''
class PipeMania(Problem):
    def __init__(self, initial_board: Board):
        initial_state = PipeManiaState(initial_board)
        super().__init__(initial_state)

    '''
    Returns a list of actions that can be executed from
    the state passed as argument
    An action is a list with the position of the pipe
    and the rotation to be executed
    '''
    def actions(self, state: PipeManiaState):
        board = state.board
        
        wrong_pipe_pos = 0

        # Check if there is a pipe which isn't right
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if not board.get_value(i, j).is_right:
                    wrong_pipe_pos = (i, j)
                    break
            if wrong_pipe_pos != 0:
                break

        if wrong_pipe_pos == 0:
            return []
        
        # Start the algorithmic part
        stack = [wrong_pipe_pos]

        while len(stack) > 0:
            current_pos = stack.pop()
            current_pipe = board.get_value(current_pos[0], current_pos[1])
            current_pipe.is_right = True

            # Get the adjacent values
            adjacent_values = board.adjacent_values(current_pos[0], current_pos[1])

            top_rot = bot_rot = right_rot = left_rot = OFF

            # Get the possible rotations
            if adjacent_values[0]:
                top_rot = adjacent_values[0].bot if adjacent_values[0].is_right else UNKNOWN
            if adjacent_values[1]:
                bot_rot = adjacent_values[1].top if adjacent_values[1].is_right else UNKNOWN
            if adjacent_values[2]:
                right_rot = adjacent_values[2].left if adjacent_values[2].is_right else UNKNOWN
            if adjacent_values[3]:
                left_rot = adjacent_values[3].right if adjacent_values[3].is_right else UNKNOWN

            possibilities = current_pipe.rotation_posibilities(top_rot, bot_rot, right_rot, left_rot)
            
            # If there is only one possibility, rotate the pipe and add the adjacent pipes to the stack
            if len(possibilities) == 1:
                current_pipe.rotate(possibilities[0])
                if adjacent_values[0] and not adjacent_values[0].is_right:
                    stack.append((current_pos[0] - 1, current_pos[1]))
                if adjacent_values[1] and not adjacent_values[1].is_right:
                    stack.append((current_pos[0] + 1, current_pos[1]))
                if adjacent_values[2] and not adjacent_values[2].is_right:
                    stack.append((current_pos[0], current_pos[1] + 1))
                if adjacent_values[3] and not adjacent_values[3].is_right:
                    stack.append((current_pos[0], current_pos[1] - 1))
            elif len(possibilities) == 0:
                return []
            else:
                current_pipe.is_right = False

        current_pipe.is_right = True
        return [[current_pos, possibility] for possibility in possibilities]
            

    '''
    Returns the resulting state of executing an action on
    the 'state' passed as argument
    '''
    def result(self, state: PipeManiaState, action):
        new_board = Board.copy_board(state.board)
        position = action[0]
        rotation = action[1]
        new_board.get_value(position[0], position[1]).rotate(rotation)
        return PipeManiaState(new_board)
    
    '''
    Returns true if the state passed as argument is a goal state.
    '''
    def goal_test(self, state: PipeManiaState):
        stack = [(0, 0)]  
        visited = set()

        while stack:
            row, col = stack.pop()
            visited.add((row, col))

            # Get the current pipe and its adjacent values
            current_pipe = state.board.get_value(row, col)
            adjacent_values = state.board.adjacent_values(row, col)

            # Check if there is an invalid connection. If there is a connection and it isnt invalid, add to the stack
            if (adjacent_values[0] is None and current_pipe.top == ON) or (adjacent_values[0] and (adjacent_values[0].bot != current_pipe.top)):
                return False
            elif current_pipe.top == ON and (row - 1, col) not in visited:
                stack.append((row - 1, col))

            if (adjacent_values[1] is None and current_pipe.bot == ON) or (adjacent_values[1] and (adjacent_values[1].top != current_pipe.bot)):
                return False
            elif current_pipe.bot == ON and (row + 1, col) not in visited:
                stack.append((row + 1, col))

            if (adjacent_values[2] is None and current_pipe.right == ON) or (adjacent_values[2] and (adjacent_values[2].left != current_pipe.right)):
                return False
            elif current_pipe.right == ON and (row, col + 1) not in visited:
                stack.append((row, col + 1))

            if (adjacent_values[3] is None and current_pipe.left == ON) or (adjacent_values[3] and (adjacent_values[3].right != current_pipe.left)):
                return False
            elif current_pipe.left == ON and (row, col - 1) not in visited:
                stack.append((row, col - 1))

        return len(visited) == len(state.board.board)*len(state.board.board[0])

    '''
    Heuristic function used in A*
    '''
    def h(self, node: Node):
        return 0


if __name__ == "__main__":
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    if goal_node:
        goal_node.state.board.print_board_id()
    else:
        print("tamale")