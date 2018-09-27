import numpy as np
from random import randint, choice
from math import ceil, floor
from os import system
from time import sleep

class Dungeon:
  def __init__(self):
    self.WIDTH = 64
    self.HEIGHT = 64
    self.dungeon = np.ones((self.WIDTH, self.HEIGHT), dtype=int)
    self.gen = 0

def gen_room():
  MIN = 4
  MAX = 12
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
    MAX = 12
    row, col = choose_wall(d, (2, 3))
    d.dungeon[row, col] = 0
    dirs = []
    if d.dungeon[row, col+1] != 0: dirs.append((0, 1)) 
    if d.dungeon[row, col-1] != 0: dirs.append((0, -1)) 
    if d.dungeon[row+1, col] != 0: dirs.append((1, 0)) 
    if d.dungeon[row-1, col] != 0: dirs.append((-1, 0)) 
    direction = choice(dirs)
    length = randint(MIN, MAX)
    for _ in range(length):
      row+=direction[0]
      col+=direction[1]
      if row > 0 and row < d.HEIGHT and col > 0 and col < d.WIDTH:
        d.dungeon[row, col] = 0

  elif d.gen % 2 == 0: #room
    row, col = choose_wall(d, (3, 3))
    d.dungeon[row, col] = 0
    room = gen_room()
    dirs = fits(d, room, row, col)
    if len(dirs) > 0:
      direction = choice(dirs)
    else:
      return d.dungeon, d.gen
    print(row, col, direction, room.shape)

    if direction == (-1, 0): #GOING UP
      row-=(room.shape[0])
      col-=randint(-1*ceil(room.shape[1]/2)+1, ceil(room.shape[1]/2)-1)
      print("up", row, "+", room.shape[0], col, "+", room.shape[1])
    elif direction == (0, -1): #GOING LEFT
      col-=(room.shape[1])
      row-=randint(-1*ceil(room.shape[0]/2)+1, ceil(room.shape[0]/2)-1)
      print("left", row, "+", room.shape[0], col, "+", room.shape[1])
    elif direction == (1, 0): #GOING DOWN
      row-=1
      col-=randint(-1*ceil(room.shape[1]/2)+1, ceil(room.shape[1]/2)-1)
      print("down", row, "+", room.shape[0], col, "+", room.shape[1])
    elif direction == (0, 1): #GOING RIGHT
      row-=randint(-1*ceil(room.shape[0]/2)+1, ceil(room.shape[0]/2)-1)
      print("right", row, "+", room.shape[0], col, "+", room.shape[1])
    else:
      return d.dungeon, d.gen

    d.dungeon[row:row+room.shape[0], col:col+room.shape[1]] = room



  else: #pass
    return d.dungeon, d.gen
      
  return d.dungeon, d.gen+1

def fits(d, room, row, col):
  valid = []
  #NORTH
  dims=[row-room.shape[0]-1, row-1, ceil(col-room.shape[1]/2), floor(col+room.shape[1]/2)]
  temp = d.dungeon[dims[0]:dims[1], dims[2]:dims[3]]
  if np.array_equal(np.ones((abs(dims[1]-dims[0]), abs(dims[3]-dims[2])), dtype=int), temp):
    valid.append((-1, 0))
  #SOUTH
  dims=[row+room.shape[0]+1, row+1, ceil(col-room.shape[1]/2), floor(col+room.shape[1]/2)]
  temp = d.dungeon[dims[0]:dims[1], dims[2]:dims[3]]
  if np.array_equal(np.ones((abs(dims[0]-dims[1]), abs(dims[3]-dims[2])), dtype=int), temp):
    valid.append((1, 0))
  #WEST
  dims=[ceil(row-room.shape[0]/2), floor(row+room.shape[0]/2), col-room.shape[1]-1, col-1]
  temp = d.dungeon[dims[0]:dims[1], dims[2]:dims[3]]
  if np.array_equal(np.ones((abs(dims[1]-dims[0]), abs(dims[3]-dims[2])), dtype=int), temp):
    valid.append((0, -1))
  #EAST
  dims=[ceil(row-room.shape[0]/2), floor(row+room.shape[0]/2), col+room.shape[1]+1, col+1]
  temp = d.dungeon[dims[0]:dims[1], dims[2]:dims[3]]
  if np.array_equal(np.ones((abs(dims[1]-dims[0]), abs(dims[3]-dims[2])), dtype=int), temp):
    valid.append((0, 1))


  return valid

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
  for i in range(40):
    system("cls")
    try:
      d.dungeon, d.gen = add_feature(d)
    except IndexError:
      i += 1

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
