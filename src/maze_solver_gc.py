# GOOGLE COLAB VERSION
import numpy as np

grid = ["SOOOOO*OOO",
        "**********",
        "OOOO*OOOO*",
        "***O*O****",
        "*OOO*O*OOO",
        "***O******",
        "OO*O*OOOO*",
        "*O***O****",
        "*O*O*O*OOO",
        "***O*O***E"]

def readGrid():
  start = []
  end = []
  walls = []
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      if grid[row][col] == 'S':
        start = [col,row]
      elif grid[row][col] == 'E':
        end = [col,row]
      elif grid[row][col] == 'O':
        walls.append([col,row])
  maze_width = len(grid[0])
  maze_height = len(grid)
  return start, end, walls, maze_width, maze_height

start, end, walls, maze_width, maze_height = readGrid()

END_REWARD = 1
WALLS_REWARD = -1
OUT_OF_BOUNDS_REWARD = -1
GAMMA = 0.99
MAX_VALUE_PERCENTAGE = 0.7
VALUE_PERCENTAGE = 0.1

INFINITY = 9999999999

# helper functions
def inBounds(x,y):
  if x < 0 or x >= maze_width or y < 0 or y >= maze_height:
    return False
  else:
    return True

def getRewardAmount(x,y):
  if inBounds(x,y):
    if [x,y] == end:
      return END_REWARD
    elif [x,y] in walls:
      return WALLS_REWARD
    else:
      return 0
  else:
    return OUT_OF_BOUNDS_REWARD

def getAction(x,y,action):
  if action == 0:
    return [x+1,y]
  elif action == 1:
    return [x-1,y]
  elif action == 2:
    return [x,y+1]
  elif action == 3:
    return [x,y-1]
  else:
    return [x,y] 
  
  # stuff for the participants to do
def getValue(x,y,grid):
  if getRewardAmount(x,y) != 0:
    return getRewardAmount(x,y)
  neighbors = []
  # arbitrary min value
  neighbors_max = -INFINITY
  max_index = 0
  
  for i in range(4):
    next_state = getAction(x,y,i)
    value = 0
    if inBounds(next_state[0],next_state[1]):
      value = GAMMA * grid[next_state[1]][next_state[0]]
    else:
      value = GAMMA * OUT_OF_BOUNDS_REWARD
    if value > neighbors_max:
      neighbors_max = value
      max_index = i
    neighbors.append(value)
  
  neighbors.pop(max_index)
  result = 0
  result += neighbors_max * MAX_VALUE_PERCENTAGE
  for i in range(len(neighbors)):
    result += neighbors[i] * VALUE_PERCENTAGE
  return result

def onPath(x,y):
  if [y,x] in walls:
    return False
  if [y,x] == end:
    return False
  if not inBounds(y,x):
    return False
  if [y,x] == start:
    return False
  return True

def valueMap():
  value_map = []
  # init with base rewards
  for y in range(maze_height):
    val_row = []
    for x in range(maze_width):
      val_row.append(getRewardAmount(x,y))
    value_map.append(val_row)
  
  # value iteration
  #for i in range(30):
  previous_value = 0
  next_value = 0
  delta = INFINITY
  # for i in range(10):
  while delta >= (1 - GAMMA) / GAMMA:
    previous_value = value_map[start[1]][start[0]]
    temp_map = value_map
    for y in range(maze_height):
      for x in range(maze_width):
        next_value = getValue(x,y,temp_map)
        value_map[y][x] = next_value
    next_value = value_map[start[1]][start[0]]
    delta = abs(previous_value - next_value)
  
  return value_map

def getBestPath(value_map):
  pos = start
  path = []
  out = 0
  while pos != end:
    path.append(pos)
    out += 1
    if(out >= 200):
      print("NO PATH FOUND AFTER 200 ATTEMPTS")
      return None
    max_val = -INFINITY
    max_move = pos
    for i in range(4):
      next_state = getAction(pos[0],pos[1],i)
      if inBounds(next_state[0],next_state[1]) and next_state not in path:
        val = value_map[next_state[1]][next_state[0]]
        if val > max_val:
          max_val = val
          max_move = next_state
    pos = max_move
  path.append(pos)
  return path

def printPath(value_map):
  path = getBestPath(value_map)
  output = []
  if path == None:
    return output
  for row in range(len(value_map)):
    dis_row = []
    for col in range(len(value_map[row])):
      value = value_map[row][col]
      if value == END_REWARD:
        dis_row.append('E')
      elif [col,row] == start:
        dis_row.append('S')
      elif value == WALLS_REWARD:
        dis_row.append('X')
      elif [col,row] in path:
        dis_row.append('*')
      else:
        dis_row.append(' ')
    output.append(dis_row)
  return output

print(np.matrix(printPath(valueMap())))
# print(np.matrix(valueMap()))
# temp check to make sure it finds best path for sure
# print(len(getBestPath(valueMap())))
