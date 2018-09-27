import numpy as np
from random import randint, choice
from math import ceil

class Dungeon:
  def __init__(self):
    self.WIDTH = 32
    self.HEIGHT = 32
    self.dungeon = np.ones((self.WIDTH, self.HEIGHT), dtype=int)
    self.gen = 0

def gen_room():
  MIN = 2
  MAX = 6
  room = np.zeros((randint(MIN, MAX), randint(MIN, MAX)))
  #print(room)
  return room

def add_feature(d):
  if d.gen == 0: #add a room to the middle
    room = gen_room()
    dims = list(map(int, [d.WIDTH/2-room.shape[0], d.WIDTH/2, d.HEIGHT/2-room.shape[1], d.HEIGHT/2]))
    d.dungeon[dims[0]:dims[1], dims[2]:dims[3]] = room

  elif d.gen % 2 == 1: #corridor
    MIN = 4
    MAX = 10
    row, col = choose_wall(d, (2, 3))
    d.dungeon[row, col] = 0
    dirs = []
    if d.dungeon[row, col+1] != 0: dirs.append((0, 1)) 
    if d.dungeon[row, col-1] != 0: dirs.append((0, -1)) 
    if d.dungeon[row+1, col] != 0: dirs.append((1, 0)) 
    if d.dungeon[row-1, col] != 0: dirs.append((-1, 0)) 
    direction = choice(dirs)
    length = randint(MIN, MAX)
    for i in range(length):
      row+=direction[0]
      col+=direction[1]
      if row > 0 and row < d.HEIGHT and col > 0 and col < d.WIDTH:
        d.dungeon[row, col] = 0
    new_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    new_dirs.remove(direction)
    new_dir = choice(new_dirs)

    row+=new_dir[0]
    col+=new_dir[1]

    if row < 0: row = 1
    if col < 0: col = 1
    if row > d.HEIGHT: row = d.HEIGHT-1
    if col > d.WIDTH: col = d.WIDTH-1
    try:
      d.dungeon[row, col] = 0
    except IndexError:
      print(row, col)

    room = gen_room()
    if new_dir == (-1, 0): #GOING UP
      row-=(room.shape[0])
      col-=randint(-1*ceil(room.shape[1]/2), ceil(room.shape[1]/2))
      print("up", row, "+", room.shape[0], col, "+", room.shape[1])
    elif new_dir == (0, -1): #GOING LEFT
      col-=(room.shape[1])
      row-=randint(-1*ceil(room.shape[0]/2), ceil(room.shape[0]/2))
      print("left", row, "+", room.shape[0], col, "+", room.shape[1])
    elif new_dir == (1, 0): #GOING DOWN
      row-=1
      col-=randint(-1*ceil(room.shape[1]/2), ceil(room.shape[1]/2))
      print("down", row, "+", room.shape[0], col, "+", room.shape[1])
    elif new_dir == (0, 1): #GOING RIGHT
      row-=randint(-1*ceil(room.shape[0]/2), ceil(room.shape[0]/2))
      print("right", row, "+", room.shape[0], col, "+", room.shape[1])
    else:
      return d.dungeon, d.gen
    
    if row < 0: row = room.shape[0]
    if col < 0: col = room.shape[1]
    if row > d.HEIGHT: row = d.HEIGHT-room.shape[0]
    if col > d.WIDTH: col = d.WIDTH-room.shape[1]
    try:
      d.dungeon[row:row+room.shape[0], col:col+room.shape[1]] = room
    except ValueError or IndexError:
      print(row, row+room.shape[0], col, col+room.shape[1])

  elif d.gen % 2 == 0: #room
    '''
    room = gen_room()
    row, col = choose_wall(d, (1, 1))
    print(row, col)
    try:
      dims = list(map(int, [row-room.shape[0]/2, row+room.shape[0]/2, col-room.shape[1]/2, col+room.shape[1]/2]))
      
      d.dungeon[dims[0]:dims[1], dims[2]:dims[3]] = room
    except ValueError:
      return d.dungeon, d.gen'''

  else: #pass
    return
      
  return d.dungeon, d.gen+1

def choose_wall(d, arr):
  while True:
    row, col = randint(1, d.HEIGHT), randint(1, d.WIDTH)
    if (get_neighbors(d, row, col) in arr) and d.dungeon[row, col] == 1:
      return row, col

def get_neighbors(d, row, col):
  count = 0

  adj = [
    (row+1, col),
    (row-1, col),
    (row, col+1),
    (row, col-1),
    (row+1, col-1),
    (row-1, col-1),
    (row+1, col+1),
    (row-1, col+1),
  ]
  for coord in adj:
    if in_range(d, coord[0], coord[1]):
      if d.dungeon[coord[0], coord[1]] == 0:
        count += 1

  return count

def in_range(d, row, col):
  return 0 < row < d.HEIGHT and 0 < col < d.WIDTH

if __name__ == '__main__':
  np.set_printoptions(threshold=np.nan)
  d = Dungeon()
  for _ in range(12):
    d.dungeon, d.gen = add_feature(d)

  for row in range(d.HEIGHT):
    for col in range(d.WIDTH):
      if d.dungeon[row, col] == 1:
        print(" ", end="")
      else:
        print("#", end="")
    print("")

#0 void
#1 empty
#2 wall
