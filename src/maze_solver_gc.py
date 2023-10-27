# Google Colab Version
# Make maze and maze variables - DO NOT TOUCH
import numpy as np

grid = ["SOOOOOOOOO",
        "***O*****O",
        "*O***O*OOO",
        "*O*OOO****",
        "*O***OOOO*",
        "*OOO*O****",
        "*****O*O**",
        "*OOOOO***O",
        "*******O*O",
        "OOOOOOOO*E"]

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

INFINITY = 9999999999

# Tweakable constants
END_REWARD = 1
WALLS_REWARD = -1
OUT_OF_BOUNDS_REWARD = -1
GAMMA = 0.9999
MAX_VALUE_PERCENTAGE = 0.7
VALUE_PERCENTAGE = (1.0 - MAX_VALUE_PERCENTAGE) / 3.0

# ----------------------------------------------------------------

# Provided functions - DO NOT TOUCH
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

def getInitialValueMap():
  value_map = []
  for y in range(maze_height):
    val_row = []
    for x in range(maze_width):
      val_row.append(getRewardAmount(x,y))
    value_map.append(val_row)
  return value_map

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

def onPath(x,y):
  if [x,y] in walls:
    return False
  elif [x,y] == end:
    return False
  else:
    return inBounds(x,y)

# ----------------------------------------------------------------

# TODO
def getValue(x,y,grid):
  # early exit in case value is already set we only want to sample values
  if not onPath(x,y):
    return getRewardAmount(x,y)

  # initial variables
  neighbors = []
  max = -INFINITY
  max_index = 0

  # loop over possible actions
  for i in range(4):
    next_state = getAction(x,y,i)
    value = 0
    # check if theres value and if not
    if inBounds(next_state[0],next_state[1]):
      value = grid[next_state[1]][next_state[0]] * GAMMA
    else:
      value = OUT_OF_BOUNDS_REWARD * GAMMA
    # check if value is highest yet
    if value > max:
      max = value
      max_index = i
    neighbors.append(value)

  # take out highest values
  neighbors.pop(max_index)
  result = 0

  #sum up result
  result += max * MAX_VALUE_PERCENTAGE
  for i in range(len(neighbors)):
    result += neighbors[i] * VALUE_PERCENTAGE
  return result

def valueMap():
  value_map = getInitialValueMap()

  # value iteration
  previous_value = 0
  next_value = 0
  delta = INFINITY
  while delta >= (1 - GAMMA) / GAMMA:
    previous_value = value_map[start[1]][start[0]]
    # create temporary map so that you don't sample values you're editing
    temp_map = value_map
    # edit values
    for y in range(maze_height):
      for x in range(maze_width):
        next_value = getValue(x,y,temp_map)
        value_map[y][x] = next_value
    next_value = value_map[start[1]][start[0]]
    # update delta
    delta = abs(previous_value - next_value)

  for y in range(maze_height):
    for x in range(maze_width):
      value = value_map[y][x]
      value_map[y][x] = round(value, 3)

  return value_map

def getBestPath(value_map):
  # start at start and make variables
  pos = start
  path = []
  # out in case it gets stuck
  out = 0
  while pos != end:
    out += 1
    # only append positions not already found
    if pos not in path:
      path.append(pos)
    # figuring out maximum value
    max_val = -INFINITY
    max_move = pos
    # out if stuck
    if out == 200:
      return path
    # check all neighboring actions
    for i in range(4):
      next_state = getAction(pos[0],pos[1],i)
      # helps get more accurate. not always needed
      if next_state in path:
        continue
      # get neighboring actions
      if inBounds(next_state[0],next_state[1]):
        val = value_map[next_state[1]][next_state[0]]
        if val > max_val:
          max_val = val
          max_move = next_state
    pos = max_move
  # add the last position
  path.append(pos)
  return path

# ----------------------------------------------------------------

# Output - DO NOT TOUCH
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

print(" ")

print(np.matrix(valueMap()))

print(" ")
# print(np.matrix(printPath(valueMap())))
# print("Length of path:")
# print(len(getBestPath(valueMap())))

# SEE FINAL OUTPUT HERE:
