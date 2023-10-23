import math

import numpy as np
#        12345
maze2 = ["S    ",
        "     ",
        "     ",
        "     ",
        "    E"]

# todo: for-loop for iteration, instead of copy pasting 7 times :/
#       actually applying the value map to a bot that uses it to solve the maze
#       stress testing

class Grid:
    def __init__(self):
        self.maze_height = 10
        self.maze_width = 10
        self.maze = []
        for i in range(self.maze_height):
            self.maze.append([0,0,0,0,0,0,0,0,0,0])
        # reward for end
        self.maze[6][2] = 50
    def get_value(self,x,y,grid):
        if x < 0 or x >= self.maze_width or y < 0 or y >= self.maze_height:
            return -10
        elif x == 6 and y == 2:
            return 50
        else:
            return grid[x][y]
    def value_iteration(self):
        value_map = []
        for i in range(self.maze_height):
            value_map.append([0,0,0,0,0,0,0,0,0,0])
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += self.get_value(x+1,y,self.maze)
                cell_value += self.get_value(x-1,y,self.maze)
                cell_value += self.get_value(x,y+1,self.maze)
                cell_value += self.get_value(x,y-1,self.maze)
                cell_value /= 4
                value_map[x][y] = cell_value
        
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = cell_value
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = cell_value
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = cell_value
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = cell_value
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = cell_value
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell_value = 0
                cell_value += 0.9 * self.get_value(x+1,y,value_map)
                cell_value += 0.9 * self.get_value(x-1,y,value_map)
                cell_value += 0.9 * self.get_value(x,y+1,value_map)
                cell_value += 0.9 * self.get_value(x,y-1,value_map)
                cell_value /= 4
                value_map[x][y] = int(cell_value)
        return value_map

grid = Grid()
print(np.matrix(grid.value_iteration()))