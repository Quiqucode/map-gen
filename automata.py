import random as rand
#import tkinter as tk
from copy import deepcopy

class Dungeon:
    def __init__(self):
        self.dungeon = None

    def init(self, h=200, w=200):
        self.dungeon = [[0 for x in range(h)] for y in range(w)] 

        self.height, self.width = h, w

    def generate(self, gen_passes=4, polish_passes=20):
        #ideal parameters
        #gen_passes = 4
        #polish_passes = 20
        self.randomize()

        curr_pass = 0
        
        while curr_pass < gen_passes:
            self.alg_pass(False)
            #print(self)
            #print("\n"*8)
            curr_pass += 1

        curr_pass = 0

        #80 is extremely smooth
        #20 is around the sweet spot
        while curr_pass < polish_passes:
            self.alg_pass(True)
            curr_pass += 1
        
        #print(self)

    def neighbors(self, ext, row, col):
        count = 0
        if not ext:
            for dis_h in [-1, 0, 1]:
                for dis_w in [-1, 0, 1]:
                    if self.isInRange(row+dis_h, col+dis_w):
                        #print(row, col, dis_h, dis_w)
                        if self.dungeon[row+dis_h][col+dis_w] == 1:
                            count += 1

        return count

    def isInRange(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def randomize(self):
        for i in range(2, self.height-2):
            for j in range(2, self.width-2):
                no = rand.randint(0, 20)
                if no in range(0,6):

                    self.dungeon[i].insert(j, 0)
                elif no in range(7, 20):
                    self.dungeon[i].insert(j, 1)

    def alg_pass(self, polish):
        #0 wall
        #1 open
        new_dung = [[0 for x in range(self.height)] for y in range(self.width)]        
        
        if not polish:
            for i in range(self.height):
                for j in range(self.width):
                    adj = self.neighbors(False, i, j)
                    adj_ext = self.neighbors(True, i, j)
                    #birth threshold
                    if adj >= 5 and self.dungeon[i][j] == 1:
                        new_dung[i].insert(j, 0)
                    elif adj_ext < 2 and self.dungeon[i][j] == 1:
                        new_dung[i].insert(j, 0)
                    else:
                        new_dung[i].insert(j, 1)
        else:
            for i in range(self.height):
                for j in range(self.width):
                    adj = self.neighbors(False, i, j)
                    adj_ext = self.neighbors(True, i, j)
                    #birth threshold
                    if adj >= 6 and self.dungeon[i][j] == 1:
                        new_dung[i].insert(j, 0)
                    elif adj_ext <= -1 and self.dungeon[i][j] == 1:
                        new_dung[i].insert(j, 0)
                    else:
                        new_dung[i].insert(j, 1)

        self.dungeon = deepcopy(new_dung)

    def __str__(self):
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                #print(i, j)
                if self.dungeon[i][j] == 0:
                    out += "#"
                elif self.dungeon[i][j] == 1:
                    out += " "
            out += "\n"
        return out

    def get_map(self):
        return self.dungeon
    '''
class Rectangle(object):
    def __init__(self, canvas, coords, fill, outline=None):
        self.canvas = canvas
        self.fill = fill
        self.outline = outline if outline is not None else self.fill
        self.canvas_id = self.canvas.create_rectangle(
            coords, outline=self.outline, fill=self.fill)'''

def test(height=80, width=80, gen_passes=4, polish_passes=12):
    #app = tk.Tk()
    #app.geometry("%sx%s" % (height*3+3, width*3+3))

    #canv = tk.Canvas(app, height=height*3+3, width=width*3+3)

    map = Dungeon()
    map.init(height, width)
    map.generate(gen_passes, polish_passes)
    return map.dungeon
    '''for i in range(map.height):
        for j in range(map.width):
            if map.dungeon[i][j] == 0:
                Rectangle(canv, (i*3, j*3, i*3+3, j*3+3), "black")

    canv.pack()

    app.mainloop(n=0)'''
