import math
import numpy as np

class Maze:
    def __init__(self):
        # maze variables
        self.start = [0,0]
        self.end = [0,0]
        self.walls = []
        self.width = 0
        self.height = 0
        # read maze from file
        file = open("maze.txt","r")
        grid_string = file.readlines()
        self.set_up_maze(grid_string)
    def set_up_maze(self,grid_string):
        for row in range(len(grid_string)):
            for col in range(len(grid_string[row])):
                if grid_string[row][col] == 'S':
                    self.start = [row,col]
                elif grid_string[row][col] == 'E':
                    self.end = [row,col]
                elif grid_string[row][col] == 'O':
                    self.walls.append([row,col])
                elif grid_string[row][col] == '\n':
                    self.width = col
        self.height = len(grid_string)
    def get_reward_value(self,x,y):
        if not self.in_bounds(x,y):
            return -2
        if [x,y] in self.walls:
            return -1
        if [x,y] == self.end:
            return 500
        return 0
    def get_action(self,x,y,i):
        if i == 0:
            return x + 1, y
        if i == 1:
            return x - 1, y
        if i == 2:
            return x, y + 1
        if i == 3:
            return x, y - 1
        else:
            return x, y
    def in_bounds(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        else:
            return True
    def get_average(self,x,y,grid):
        result = []
        if [x,y] == self.end:
            return 500
        if [x,y] in self.walls:
            return -1
        max_value = -100000
        max_index = 0
        for i in range(4):
            x1, y1 = self.get_action(x,y,i)
            if self.in_bounds(x1,y1):
                value = 0.9 * grid[x1][y1]
                if value > max_value:
                    max_value = value
                    max_index = i
                result.append(value)
            else:
                result.append(0.9 * -2)
        result.pop(max_index)
        return_val = max_value * 0.7
        for i in range(3):
            return_val += result[i] * 0.1
        return return_val

    def value_mapping(self):
        value_map = []
        for i in range(self.height):
            v_row = []
            for j in range(self.width):
                v_row.append(0)
            value_map.append(v_row)
        # first iteration, base values
        for y in range(self.height):
            for x in range(self.width):
                value_map[x][y] = self.get_reward_value(x,y)
        
        for i in range(30):
            for y in range(self.height):
                for x in range(self.width):
                    value_map[x][y] = self.get_average(x,y,value_map)
        
        #
        return value_map
    
    def find_optimal_path(self, value_map):
        path_map = []
        for i in range(len(value_map)):
            path_row = []
            for j in range(len(value_map[i])):
                if value_map[i][j] == -10:
                    path_row.append('X')
                else:
                    path_row.append(' ')
            path_map.append(path_row)
        start_pos = self.start
        while start_pos != self.end:
            path_map[start_pos[0]][start_pos[1]] = '*'
            max_value = -100000
            max_move = start_pos
            for i in range(4):
                x1, y1 = self.get_action(start_pos[0],start_pos[1],i)
                if self.in_bounds(x1,y1):
                    possible_value = value_map[x1][y1]
                    if possible_value > max_value:
                        max_value = possible_value
                        max_move = [x1,y1]
            start_pos = max_move
        path_map[start_pos[0]][start_pos[1]] = 'E'
        return path_map
                
                    

# todo: for-loop for iteration, instead of copy pasting 7 times :/
#       actually applying the value map to a bot that uses it to solve the maze
#       stress testing

grid = Maze()
# print(np.matrix(grid.value_mapping()))
print(np.matrix(grid.find_optimal_path(grid.value_mapping())))