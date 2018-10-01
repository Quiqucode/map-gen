import numpy as np
from random import randint, choice
from math import ceil, floor
from os import system
from time import sleep

class Dungeon:
  def __init__(self, mode="strd"):
    self.WIDTH = 138
    self.HEIGHT = 92
    self.BORDER = 8
    self.TOTAL_GENS = 80
    self.ROOM_DIMS = (6, 12)
    if mode == "strd":
      self.CORR_DIMS = (6, 12)
    elif mode == "cave":
      self.CORR_DIMS = (1, 2)
      self.ROOM_DIMS = (2, 12)
      self.TOTAL_GENS = 512
    else:
      pass
    self.dungeon = np.ones((self.HEIGHT, self.WIDTH), dtype=int)
    self.gen = 0

def gen_room(d):
  MIN = d.ROOM_DIMS[0]
  MAX = d.ROOM_DIMS[0]
  room = np.zeros((randint(MIN/2, MAX/2)*2, randint(MIN/2, MAX/2)*2))
  #print(room)
  return room

def add_feature(d):
  if d.gen == 0: #add a room to the middle
    room = gen_room(d)
    dims = list(map(int, [d.WIDTH/2-room.shape[0]/2, d.WIDTH/2+room.shape[0]/2, d.HEIGHT/2-room.shape[1]/2, d.HEIGHT/2+room.shape[1]/2]))
    d.dungeon[dims[0]:dims[1], dims[2]:dims[3]] = room

  elif d.gen > 0: #corridor
    MIN = d.CORR_DIMS[0]
    MAX = d.CORR_DIMS[1]
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
      if row > d.BORDER and row < d.HEIGHT-d.BORDER and col > d.BORDER and col < d.WIDTH-d.BORDER:
        d.dungeon[row, col] = 0

    room = gen_room(d)

    try:
      while row-floor(room.shape[0]/2) < d.BORDER:
        room = np.zeros((room.shape[0]-1 , room.shape[1]))
      while row+ceil(room.shape[0]/2) > d.HEIGHT-d.BORDER:
        room = np.zeros((room.shape[0]-1, room.shape[1]))
      while col-floor(room.shape[1]/2) < d.BORDER:
        room = np.zeros((room.shape[0], room.shape[1]-1))
      while col+ceil((room.shape[1]/2)) > d.WIDTH-d.BORDER:
        room = np.zeros((room.shape[0], room.shape[1]-1))

      #print(room.shape)
      d.dungeon[row-floor(room.shape[0]/2):row+ceil(room.shape[0]/2), col-floor(room.shape[1]/2):col+ceil(room.shape[1]/2)] = room
    except ValueError:
      return d.dungeon, d.gen

  else: #pass
    return d.dungeon, d.gen
      
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
  #np.set_printoptions(threshold=np.nan)
  d = Dungeon()
  while d.gen < d.TOTAL_GENS:
    #system("clear")
    try:
      d.dungeon, d.gen = add_feature(d)
    except IndexError:
      pass

  for row in range(d.HEIGHT):
    for col in range(d.WIDTH):
      if d.dungeon[row, col] == 1:
        print("#", end="")
      else:
        print(".", end="")
    print("")
    
    

#0 void
#1 empty
#2 wall
