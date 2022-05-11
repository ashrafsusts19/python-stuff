from math import floor, ceil
import pygame as pg
import random
from copy import copy


SCREENMAP = [[0 for _ in range(10)] for _ in range(20)]
TYPES = ["i", "j", "l", "o", "s", "t", "z"]
BLOCKS = {"i": [(-1,0), (1,0), (2,0)], "j":[(-1,-1), (-1, 0), (1,0)], "l": [(-1,0), (1, 0), (1,-1)],
          "o": [(0,-1), (1, 0), (1,-1)], "s": [(-1,0), (0, -1), (1,-1)], "t": [(-1,0), (0, -1), (1,0)],
          "z": [(-1,-1), (0, -1), (1,0)]
          }
BSTATES = {"i":2, "j":4, "l":4, "o":1, "s":2, "t":4, "z":2}

class Blocks():
    cstate = 1
    def __init__(self, type):
        self.type = type
        self.shape = copy(BLOCKS[type])
        self.x = len(SCREENMAP[0]) // 2 - 1
        self.y = -min([0] + [tup[1] for tup in self.shape])
        self.states = BSTATES[type]
        self.maxl = max([0] + [abs(tup[0]) for tup in self.shape] + [abs(tup[1]) for tup in self.shape])

    def checkshape(self, shape):
        lx = min([0] + [tup[0] for tup in shape])
        rx = max([0] + [tup[0] for tup in shape])
        uy = min([0] + [tup[1] for tup in shape])
        dy = max([0] + [tup[1] for tup in shape])
        return (lx, rx, uy, dy)

    def draw(self, screen, sx, sy):
        pg.draw.rect(screen, "#4a00a4", (sx+self.x*20+1, sy+self.y*20+1, 18, 18))
        for (x, y) in self.shape:
            pg.draw.rect(screen, "#4a00a4", (sx + (self.x+x) * 20 + 1, sy + (self.y+y) * 20 + 1, 18, 18))

    def move(self, dx, dy):
        if self.avaibility(self.x+dx, self.y+dy, self.shape):
            self.x += dx
            self.y += dy
        elif dx==0 and dy==1:
            self.place()
            return False
        return True

    def place(self):
        for (x, y) in self.shape:
            SCREENMAP[self.y+y][self.x+x] = 1
        SCREENMAP[self.y][self.x] = 1

    def avaibility(self, cx, cy, shape):
        if not (0 <= cx < len(SCREENMAP[0])) or not (0 <= cy < len(SCREENMAP)):
            return False
        if SCREENMAP[cy][cx] != 0:
            return False
        for (x, y) in shape:
            if cx+x>=0 and cx+x<len(SCREENMAP[0]) and cy+y>=0 and cy+y<len(SCREENMAP):
                if SCREENMAP[cy+y][cx+x] != 0:
                    return False
            else:
                return False
        return True

    def alterrotate(self, rshape):
        lx, rx, uy, dy = self.checkshape(rshape)
        for dxy in range(self.maxl+1):
            for (x, y) in [(dxy, 0), (-dxy, 0), (0, -dxy), (0, dxy)]:
                if x >= lx and x <= rx and y >= uy and y <= dy:
                    if self.avaibility(self.x - x, self.y - y, rshape):
                        return (x, y)
        return (None, None)

    def rotate(self):
        if self.cstate < self.states:
            rshape = [(y, -x) for (x, y) in self.shape]
            if self.avaibility(self.x, self.y, rshape):
                self.shape = copy(rshape)
                self.cstate += 1
            else:
                x, y = self.alterrotate(rshape)
                if x != None:
                    self.x -= x
                    self.y -= y
                    self.shape = copy(rshape)
                    self.cstate += 1
        else:
            rshape = copy(self.shape)
            for _ in range(self.states-1):
                rshape = [(-y, x) for (x, y) in rshape]
            if self.avaibility(self.x, self.y, rshape):
                self.shape = copy(rshape)
                self.cstate = 1
            else:
                x, y = self.alterrotate(rshape)
                if x != None:
                    self.x -= x
                    self.y -= y
                    self.shape = copy(rshape)
                    self.cstate = 1

    def projecty(self):
        for yy in range(self.y, len(SCREENMAP)):
            if not self.avaibility(self.x, yy, self.shape):
                return yy - 1
        return len(SCREENMAP)-1

    def drawprojection(self, screen, sx, sy):
        proy = self.projecty()
        pg.draw.rect(screen, "#6200e3", (sx + self.x * 20 + 1, sy + proy * 20 + 1, 18, 18), 1)
        for (x, y) in self.shape:
            pg.draw.rect(screen, "#6200e3", (sx + (self.x + x) * 20 + 1, sy + (proy + y) * 20 + 1, 18, 18), 1)

    def smackdown(self):
        self.y = self.projecty()
        self.place()



class MiniScreen():
    def __init__(self, screen, x, y, rows, cols):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.screen = screen


class GameScreen(MiniScreen):
    score = 0
    level = 1

    def drawboard(self):
        pg.draw.rect(self.screen, "#190025", (self.x, self.y, 20*self.cols, 20*self.rows))
        for i in range(len(SCREENMAP)):
            for j in range(len(SCREENMAP[0])):
                if SCREENMAP[i][j] != 0:
                    pg.draw.rect(self.screen, "#4a00a4", (self.x+j*20+1, self.y+i*20+1, 18, 18))

    def checkscore(self):
        rowsclr = 0
        for i in range(len(SCREENMAP)):
            if 0 not in SCREENMAP[i]:
                SCREENMAP.pop(i)
                SCREENMAP.insert(0, [0 for i in range(len(SCREENMAP[-1]))])
                rowsclr += 1
        if rowsclr > 0:
            self.score += 40 * (3 ** (rowsclr - 1))


class ScoreScreen(MiniScreen):
    def draw(self, score, font):
        pg.draw.rect(self.screen, "#190025", (self.x, self.y, 20*self.cols, 20*self.rows))
        scoretext = font.render("Score", 1, "#ffffff")
        scoretext2 = font.render(f"{score}", 1, "#ffffff")
        xst = self.x + self.cols * 10 - scoretext.get_width()/2
        xst2 = self.x + self.cols * 10 - scoretext2.get_width()/2
        self.screen.blit(scoretext, (xst, self.y + 20))
        self.screen.blit(scoretext2, (xst2, self.y + floor(self.rows/2) * 20))


class NextScreen(MiniScreen):
    def __init__(self, screen, x, y, rows, cols):
        super().__init__(screen, x, y, rows, cols)
        self.cx = cols//2
        self.cy = rows//2
    def draw(self, type):
        pg.draw.rect(self.screen, "#190025", (self.x, self.y, 20 * self.cols, 20 * self.rows))
        for (x, y) in BLOCKS[type]:
            xx = self.x + (self.cx + x) * 20 - 1
            yy = self.y + (self.cy + y) * 20 - 1
            pg.draw.rect(self.screen, "#4a00a4", (xx, yy, 18, 18))
        pg.draw.rect(self.screen, "#4a00a4", (self.x + self.cx * 20- 1, self.y + self.cy * 20 - 1, 18, 18))


def drawscreen():
    screen.fill("#311a30")
    game.drawboard()
    if gameover:
        screen.blit(txtgo, (225 - txtgo.get_width()/2, 460))
    else:
        blocks[1].drawprojection(screen, game.x, game.y)
    blocks[1].draw(screen, game.x, game.y)
    scoreboard.draw(game.score, font)
    nextblock.draw(blocks[0].type)

    pg.display.update()


def reset():
    global SCREENMAP, blocks, gameover, btimer
    SCREENMAP = [[0 for _ in range(10)] for _ in range(20)]
    blocks = [Blocks(random.choice(TYPES)), Blocks(random.choice(TYPES))]
    btimer = 0
    gameover = False
    game.score = 0
    game.level = 1


def postplacement():
    global btimer, gameover
    game.checkscore()
    blocks.pop()
    blocks.insert(0, Blocks(random.choice(TYPES)))
    btimer = 0
    if not blocks[1].avaibility(blocks[1].x, blocks[1].y, blocks[1].shape):
        gameover = True



pg.init()


screen = pg.display.set_mode((450, 500))
clock = pg.time.Clock()
game = GameScreen(screen, 50,50,20,10)
scoreboard = ScoreScreen(screen, 300, 200, 5, 5)
nextblock = NextScreen(screen, 300, 50, 5, 5)

font = pg.font.SysFont("comicsans", 20, False, False)
txtgo = font.render("GAME OVER! PRESS SPACE TO RESTART", 1, "#ffffff")
gameover = False
blocks = [Blocks(random.choice(TYPES)), Blocks(random.choice(TYPES))]
btimer = 0

running = True
while running:
    clock.tick(30)
    for eve in pg.event.get():
        if eve.type == pg.QUIT:
            running = False
        if eve.type == pg.KEYDOWN:
            if not gameover:
                if eve.key == pg.K_RIGHT:
                    blocks[1].move(1, 0)
                if eve.key == pg.K_LEFT:
                    blocks[1].move(-1, 0)
                if eve.key == pg.K_DOWN:
                    if blocks[1].move(0, 1)==False:
                        postplacement()
                if eve.key == pg.K_UP:
                    blocks[1].rotate()
                if eve.key == pg.K_SPACE:
                    blocks[1].smackdown()
                    postplacement()
            else:
                if eve.key == pg.K_SPACE:
                    reset()
    btimer = (btimer + 1) % 20
    if btimer == 0 and not gameover:
        if blocks[1].move(0, 1)==False:
            postplacement()
    drawscreen()
