import pygame as pg
import numpy as np

class Game():
    color = ["#ffffff", "#91ade6"]
    blockSelected = None
    takingInput = True
    invalidAnimation = None
    invalidTimer = 6
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.board = np.zeros((9, 9))
        self.gamecan = pg.Surface((360, 360))
        self.gX, self.gY = 0, 0
        self.drawGameCan()
        self.font = pg.font.SysFont("comicsans", 40, 0, 0)
        self.aifont = pg.font.SysFont("comicsans", 30, 0, 0)

    def drawGameCan(self):
        self.gamecan.fill("#200020")
        for i in range(9):
            for j in range(9):
                pg.draw.rect(self.gamecan, self.color[(i*9+j)%2], (j*40, i*40, 40, 40))
        pg.draw.line(self.gamecan, "#000000", (40 * 3, 0), (40 * 3, 360))
        pg.draw.line(self.gamecan, "#000000", (40 * 6, 0), (40 * 6, 360))
        pg.draw.line(self.gamecan, "#000000", (0, 40 * 3), (360, 40 * 3))
        pg.draw.line(self.gamecan, "#000000", (0, 40 * 6), (360, 40 * 6))

    def drawloop(self):
        self.screen.fill("#000020")
        self.screen.blit(self.gamecan, (self.gX, self.gY))
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.drawtext(self.font, self.screen, str(int(self.board[i][j])), "#000000",
                                  self.gX + j * 40 + 20, self.gY + i * 40 + 20)
        if self.blockSelected is not None:
            x, y = self.blockSelected
            pg.draw.rect(self.screen, "#000000", (self.gX + x * 40, self.gY + y * 40, 40, 40), 2)
        if self.invalidAnimation is not None:
            x, y = self.invalidAnimation
            pg.draw.rect(self.screen, "#ff0000", (self.gX + x * 40, self.gY + y * 40, 40, 40), 2)
            self.invalidTimer -= 1
            if self.invalidTimer <= 0:
                self.invalidTimer = 6
                self.invalidAnimation = None
        pg.display.update()

    def gridSelected(self, mousex, mousey):
        if not self.takingInput:
            return
        x = (mousex - self.gX)//40
        y = (mousey - self.gY)//40
        if 0 <= x < 9 and 0 <= y < 9:
            if self.blockSelected == (x, y):
                self.blockSelected = None
            else:
                self.blockSelected = (x, y)

    def isValidMove(self, num, row, col):
        if num == 0:
            return True
        if num in self.board[row, :] or num in self.board[:, col]:
            return False
        for i in range(3):
            for j in range(3):
                if self.board[(row//3)*3 + i][(col//3)*3 + j] == num:
                    return False
        return True

    def gridInput(self, num):
        if self.blockSelected is None or not self.takingInput:
            return
        x, y = self.blockSelected
        if self.board[y][x] == num:
            return
        if self.isValidMove(num, y, x):
            self.board[y][x] = num
        else:
            self.invalidAnimation = (x, y)

    def drawtext(self, font, canvas, text, color, x, y):
        text_box = font.render(text, 1, color)
        text_rect = text_box.get_rect()
        text_rect.center = (x, y)
        canvas.blit(text_box, (text_rect.x, text_rect.y))

    def backtrack(self, ind):
        while ind < 81 and self.board[ind//9][ind%9] != 0:
            ind += 1
        if ind == 81:
            return True
        for number in range(1,10):
            if self.isValidMove(number, ind//9, ind%9):
                self.board[ind//9][ind%9] = number
                self.aiWrite(number, ind)
                result = self.backtrack(ind + 1)
                if result == True:
                    return True
                self.board[ind // 9][ind % 9] = 0
        pg.draw.rect(self.screen, self.color[ind % 2], (self.gX + (ind % 9) * 40 + 1,
                                                        self.gY + (ind // 9) * 40 + 1, 38, 38))
        pg.display.update()
        return False

    def aiWrite(self, num, ind):
        col, row = ind%9, ind//9
        pg.draw.rect(self.screen, self.color[ind%2], (self.gX + col*40 + 1, self.gY + row*40 + 1, 38, 38))
        self.drawtext(self.aifont, self.screen, str(num), "#900000",
                      self.gX + col * 40 + 20, self.gY + row * 40 + 20)
        pg.display.update()

    def mainloop(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.MOUSEBUTTONDOWN:
                    if eve.button == 1:
                        self.gridSelected(eve.pos[0], eve.pos[1])
                if eve.type == pg.KEYDOWN:
                    if eve.unicode.isdigit():
                        self.gridInput(int(eve.unicode))
                    if eve.key == pg.K_F1:
                        print("\n", self.board, "\n")
                    elif eve.key == pg.K_SPACE:
                        self.takingInput = False
                        self.backtrack(0)
                        self.takingInput = True
            self.drawloop()

pg.init()

screen = pg.display.set_mode((360, 360))
pg.display.set_caption("Sudoko Solver using Backtracking")
game = Game(screen)
game.mainloop()
