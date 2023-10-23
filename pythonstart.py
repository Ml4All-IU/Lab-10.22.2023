# starter python tests

#    1234567891234567
maze = "S       E       "

def in_bounds(coordinate):
    if coordinate[0] < 0 or coordinate[1] < 0 or coordinate[0] >= 4 or coordinate[1] >= 4:
        return False
    index = coordinate[0] + (coordinate[1] * 4)
    if maze[index] == "X":
        return False
    else:
        return True
    
def valid_move(velocity):
    if velocity[0] == velocity[1]:
        return False
    if velocity[0] > 1 or velocity[1] > 1:
        return False
    return True

def hit_end(coordinate):
    index = coordinate[0] + (coordinate[1] * 4)
    if maze[index] == "E":
        return True
    else:
        return False

# linked list to store list of coordinates
class Node:
    def __init__(self, coordinate, bad_path):
        self.coordinate = coordinate
        self.next = None
        self.length = 1
        self.bad_path = bad_path
    def add(self, coordinate):
        self.length += 1
        if self.next is None:
            self.next = Node(coordinate)
        else:
            self.next.add(coordinate)
    def append(self, next_node):
        self.length += next_node.length
        self.next = next_node
    def contains(self, coord):
        if self.coordinate == coord:
            return True
        if self.next is not None:
            return self.next.contains(coord)
        return False

class Bot:
    def __init__(self, coordinate, velocity):
        self.coordinate = coordinate
        self.velocity = velocity
    
    def move(self):
        self.coordinate = list(self.coordinate)
        self.velocity = list(self.velocity)
        self.coordinate[0] += self.velocity[0]
        self.coordinate[1] += self.velocity[1]
        self.coordinate = tuple(self.coordinate)
        self.velocity = tuple(self.velocity)

def shortest_path(bot):
    current = bot.coordinate
    curr_velocity = bot.velocity

    if not in_bounds(current):
        return Node(current,True)
    if hit_end(current):
        return Node(current,False)
    
    bot_current = Bot(current,curr_velocity)
    bot_right = Bot(current,(curr_velocity[0] + 1, curr_velocity[1]))
    bot_left = Bot(current,(curr_velocity[0] - 1, curr_velocity[1]))
    bot_up = Bot(current,(curr_velocity[0], curr_velocity[1] - 1))
    bot_down = Bot(current,(curr_velocity[0], curr_velocity[1] + 1))

    pos_bots = [bot_current,bot_right,bot_left,bot_up,bot_down]

    active_bots = []
    # filter out bad bots
    for i in range(5):
        if valid_move(pos_bots[i].velocity):
            active_bots.append(pos_bots[i])
    
    path = Node(current,True)
    for bot in active_bots:
        bot.move()
        possible_path = shortest_path(bot)
        if possible_path.bad_path:
            continue
        else:
            path.bad_path = False
            print("FOUND A GOOD PATH")
            path.append(possible_path)

    return path

def print_path(path):
    y = 0
    end_string = ''
    while y < 4:
        x = 0
        while x < 4:
            index = x + (y * 4)
            if maze[index] != ' ':
                end_string += maze[index]
            else:
                if path.contains((x,y)):
                    end_string += '*'
                else:
                    end_string += '_'
            x += 1
        end_string += '\n'
        y += 1
    
    print(end_string)

test_bot = Bot((0,0),(0,0))
path = shortest_path(test_bot)
print(path.bad_path)
print_path(path)




