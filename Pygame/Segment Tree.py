import pygame as pg
import random
from math import log2, ceil


class Game():
    rows, cols = 20, 20
    gamew, gameh = 600, 600
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.lst = []
        self.score = 0
        self.isTakingInput = False
        self.inputPos = None
        self.inputNum = ""
        for i in range(self.rows):
            self.lst.append([random.randint(0, 99) for _ in range(self.cols)])
        self.buildTree()
        #format (x, y), goes by 0 based index system
        self.centerGrid = [self.cols//2, self.rows//2]
        self.radiusx, self.radiusy = 5, 5
        self.gamecan = pg.Surface((self.gamew, self.gameh))
        self.gamecanx, self.gamecany = 0, 0
        self.statcan = pg.Surface((200, 600))
        self.font = pg.font.SysFont("comicsans", 20)
        self.font2 = pg.font.SysFont("comicsans", 30)
        self.drawcan()
        self.setRange()

    def setRange(self):
        #add 1 because this goes by 1-based index
        self.ranX = (self.centerGrid[0] - self.radiusx + 1, self.centerGrid[0] + self.radiusx + 1)
        self.ranY = (self.centerGrid[1] - self.radiusy + 1, self.centerGrid[1] + self.radiusy + 1)
        self.countSum()

    def buildTree(self):
        self.cols2 = 2 ** ceil(log2(self.cols))
        self.rows2 = 2 ** ceil(log2(self.rows))
        self.segTree = []
        for i in range(self.rows2 * 2):
            self.segTree.append([0 for _ in range(self.cols2 * 2)])
        for i in range(self.rows):
            for j in range(self.cols):
                self.segTree[i + self.rows2][j + self.cols2] = self.lst[i][j]
        for i in range(self.rows2, self.rows2 * 2):
            for j in range(self.cols2 - 1, 0, -1):
                self.segTree[i][j] = self.segTree[i][j * 2] + self.segTree[i][j * 2 + 1]
        for i in range(self.rows2 - 1, 0, -1):
            for j in range(self.cols2 * 2):
                self.segTree[i][j] = self.segTree[2 * i][j] + self.segTree[2 * i + 1][j]
        """for i in self.segTree:
            print(i)"""

    def drawcan(self):
        self.gamecan.fill("#171717")
        for i in range(self.rows):
            for j in range(self.cols):
                self.drawtext(self.gamecan, self.font, f"{self.lst[i][j]}", j * 30 + 15, i * 30 + 15)

    def drawcover(self):
        startx, starty = self.centerGrid[0] - self.radiusx, self.centerGrid[1] - self.radiusy
        pg.draw.rect(self.screen, "#ffffff", (self.gamecanx + startx * 30, self.gamecany + starty * 30,
                                              30 * (2 * self.radiusx + 1), 30 * (2 * self.radiusy + 1)), 1)
        """
        pg.draw.rect(self.screen, "#000000", (self.gamecanx + self.centerGrid[0] * 30,
                                              self.gamecany + self.centerGrid[1] * 30,
                                              30, 30), 1)
        """

    def countSum(self):
        self.score = self.queryY(1, self.ranY[0], self.ranY[1], 1, self.rows2)

    def getAverage(self):
        ave = self.score / ((self.radiusx * 2 + 1) * (self.radiusy * 2 + 1))
        return "Average: " + "%.2f" % ave

    def queryX(self, rowInd, ind, s, e, cs, ce):
        if s <= cs and ce <= e:
            return self.segTree[rowInd][ind]
        elif s > ce or e < cs:
            return 0
        else:
            return self.queryX(rowInd, ind * 2, s, e, cs, (cs + ce)//2) + self.queryX(rowInd, ind * 2 + 1, s, e,
                                                                                      (cs + ce)//2 + 1, ce)

    def queryY(self, ind, s, e, cs, ce):
        if s <= cs and ce <= e:
            # return the whole node
            return self.queryX(ind, 1, self.ranX[0], self.ranX[1], 1, self.cols2)
        elif s > ce or e < cs:
            return 0
        else:
            return self.queryY(ind * 2, s, e, cs, (cs + ce)//2) + self.queryY(ind * 2 + 1, s, e, (cs + ce)//2+1, ce)

    def radUpdate(self, rdx, rdy):
        if rdy == -1:
            if self.radiusy > 0:
                self.radiusy -=1
                self.setRange()
        elif rdy == 1:
            if self.radiusy * 2 + 3 <= self.rows:
                self.radiusy += 1
                self.setRange()
                if self.centerGrid[1] + self.radiusy >= self.rows:
                    self.centerGrid[1] = self.rows - 1 - self.radiusy
                elif self.centerGrid[1] - self.radiusy < 0:
                    self.centerGrid[1] = self.radiusy
        if rdx == -1:
            if self.radiusx > 0:
                self.radiusx -=1
                self.setRange()
        elif rdx == 1:
            if self.radiusx * 2 + 3 <= self.cols:
                self.radiusx += 1
                self.setRange()
                if self.centerGrid[0] + self.radiusx >= self.cols:
                    self.centerGrid[0] = self.cols - 1 - self.radiusx
                elif self.centerGrid[0] - self.radiusx < 0:
                    self.centerGrid[0] = self.radiusx

    def moveCenter(self, dx, dy):
        if self.centerGrid[0] + dx - self.radiusx >= 0 and self.centerGrid[0] + dx < self.cols - self.radiusx:
            self.centerGrid[0] += dx
            self.setRange()
        if self.centerGrid[1] + dy - self.radiusy >= 0 and self.centerGrid[1] + dy < self.rows - self.radiusy:
            self.centerGrid[1] += dy
            self.setRange()

    def drawtext(self, canvas, font, text, x, y, color = "#ffffff", bg = None):
        surtext = font.render(text, 1, color, bg)
        trect = surtext.get_rect()
        trect.center = (x, y)
        canvas.blit(surtext, (trect.x, trect.y))

    def drawloop(self):
        self.screen.fill("#171717")
        self.screen.blit(self.gamecan, (self.gamecanx, self.gamecany))
        self.drawcover()
        pg.draw.rect(self.screen, "#ffffff", (self.gamecanx, self.gamecany, self.gamew, self.gameh), 1)
        self.statcan.fill("#000000")
        self.drawtext(self.statcan, self.font2, f"Total: {self.score}", self.statcan.get_width()//2,
                      self.statcan.get_height()//2)
        self.drawtext(self.statcan, self.font, self.getAverage(), self.statcan.get_width() // 2,
                      self.statcan.get_height() // 2 + 50)
        self.screen.blit(self.statcan, (self.gamecanx + self.gamew, self.gamecany))
        if self.inputPos is not None:
            pg.draw.rect(self.screen, "#ffffff", (self.gamecanx + 30 * self.inputPos[0] + 2,
                                                  self.gamecany + 30 * self.inputPos[1] + 2, 26, 26))
            self.drawtext(self.screen, self.font, self.inputNum, self.gamecanx + 30 * self.inputPos[0] + 15,
                          self.gamecany + 30 * self.inputPos[1] + 15, color="#000000")
        pg.display.update()

    def changeValue(self):
        if len(self.inputNum) == 0:
            self.inputPos = None
            self.isTakingInput = False
            return
        self.lst[self.inputPos[1]][self.inputPos[0]] = int(self.inputNum)
        self.updateTree(self.inputPos[1] + 1, self.inputPos[0] + 1, int(self.inputNum))
        self.inputPos = None
        self.isTakingInput = False
        self.inputNum = ""

    #Takes 1-based index input
    def updateTree(self, row, col, value):
        #Update a row
        cnode = self.cols2 + col - 1
        rnode = self.rows2 + row - 1
        self.segTree[rnode][cnode] = value
        while (cnode > 1):
            cnode //= 2
            self.segTree[rnode][cnode] = self.segTree[rnode][cnode * 2] + self.segTree[rnode][cnode * 2 + 1]
        while rnode > 1:
            rnode //= 2
            for i in range(self.cols2 * 2):
                self.segTree[rnode][i] = self.segTree[rnode * 2][i] + self.segTree[rnode * 2 + 1][i]
        self.updateBoard()
        self.countSum()

    def updateBoard(self):
        pg.draw.rect(self.gamecan, "#171717", (30 * self.inputPos[0], 30 * self.inputPos[1], 30, 30))
        self.drawtext(self.gamecan, self.font, str(int(self.inputNum)), 30 * self.inputPos[0] + 15,
                    30 * self.inputPos[1] + 15)

    def mousePressed(self, x, y):
        if self.inputPos is not None:
            self.inputPos = None
            self.isTakingInput = False
            self.inputNum = ""
            return
        gx, gy = (x - self.gamecanx)//30, (y - self.gamecany)//30
        if gx >= self.cols or gy >= self.rows:
            return
        self.inputPos = (gx, gy)
        self.isTakingInput = True

    def mainloop(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.MOUSEBUTTONDOWN:
                    if eve.button == 1:
                        self.mousePressed(eve.pos[0], eve.pos[1])
                if eve.type == pg.KEYDOWN:
                    if self.isTakingInput:
                        if eve.key == pg.K_RETURN:
                            self.changeValue()
                        if eve.unicode.isdigit() and len(self.inputNum) < 2:
                            self.inputNum += eve.unicode
                        if eve.key == pg.K_BACKSPACE:
                            self.inputNum = self.inputNum[:-1]
                    if eve.key == pg.K_w:
                        self.radUpdate(0, 1)
                    if eve.key == pg.K_s:
                        self.radUpdate(0, -1)
                    if eve.key == pg.K_a:
                        self.radUpdate(-1, 0)
                    if eve.key == pg.K_d:
                        self.radUpdate(1, 0)
                    if eve.key == pg.K_r:
                        self.radUpdate(1, 1)
                    if eve.key == pg.K_f:
                        self.radUpdate(-1, -1)
                    if eve.key == pg.K_UP:
                        self.moveCenter(0, -1)
                    if eve.key == pg.K_DOWN:
                        self.moveCenter(0, 1)
                    if eve.key == pg.K_LEFT:
                        self.moveCenter(-1, 0)
                    if eve.key == pg.K_RIGHT:
                        self.moveCenter(1, 0)
            self.drawloop()



pg.init()

screen = pg.display.set_mode((800, 600))
game = Game(screen)
game.mainloop()



