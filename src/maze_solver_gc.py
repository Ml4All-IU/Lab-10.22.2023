# GOOGLE COLAB VERSION
import numpy as np

grid = ["SOOOOOOOOO",
        "***OOO*O*O",
        "*O*****O*O",
        "*O*OOO*O*O",
        "*O*O*O*O*O",
        "*O*O*O***O",
        "*O*O*OOO*O",
        "*OOO*****O",
        "*OO**OO*OO",
        "****O****E"]

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

END_REWARD = 50
WALLS_REWARD = -1
OUT_OF_BOUNDS_REWARD = -2
GAMMA = 0.9
MAX_VALUE_PERCENTAGE = 0.7
VALUE_PERCENTAGE = 0.1

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
  neighbors_max = -99999999
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

def valueMap():
  value_map = []
  # init with base rewards
  for y in range(maze_height):
    val_row = []
    for x in range(maze_width):
      val_row.append(getRewardAmount(x,y))
    value_map.append(val_row)
  
  # value iteration
  for i in range(30):
    for y in range(maze_height):
      for x in range(maze_width):
        value_map[y][x] = getValue(x,y,value_map)
  
  return value_map

def getBestPath(value_map):
  pos = start
  path = []
  out = 0
  while pos != end:
    path.append(pos)
    out += 1
    if(out >= 200):
      print("BAD")
      return None
    max_val = -9999999
    max_move = pos
    for i in range(4):
      next_state = getAction(pos[0],pos[1],i)
      if inBounds(next_state[0],next_state[1]):
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
# temp check to make sure it finds best path for sure
print(len(getBestPath(valueMap())))
