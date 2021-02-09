#This Code is poorly written, up for optimiztion

from tkinter import *
import numpy as np
from PIL import Image as PImage, ImageTk

class Board():
    rows = 5
    cols = 5
    colors = ["#A66D4F", "#DDB88C"]
    splength = 32
    turn = 0
    grid = np.zeros((5, 5), dtype="int32")
    draw = False

    def __init__(self, root, cross, circle):
        self.value = [cross, circle]
        self.board = Canvas(root, width = self.splength*self.cols, height=self.splength*self.rows, bg=self.colors[0])
        self.board.bind('<Button-1>', self.gridclicked)
        self.root = root
        self.drawboard()

    def drawboard(self):
        i = 1
        for row in range(self.rows):
            for col in range(self.cols):
                self.board.create_rectangle(row*32, col*32, (row+1)*32, (col+1)*32, fill = self.colors[i])
                i = 1-i
        self.board.grid(row=1, column=0)

    def gridclicked(self, event):
        sel_col, sel_row = event.x//self.splength, event.y//self.splength
        if self.grid[sel_row, sel_col] != 0 or gameover == True:
            return
        ln = self.splength
        self.grid[sel_row, sel_col] = 1 + self.turn
        self.board.create_image(sel_col*ln+ln/2, sel_row*ln+ln/2, image= self.value[self.turn])
        if self.wincheck():
            Label(self.root, text=f"Player {self.turn + 1} Won").grid(row=2, column=0)
            self.gameover()
        elif 0 not in self.grid:
            self.draw = True
            self.tiebreaker()
            self.gameover()
        self.turn = 1 - self.turn

    def winningline(self, x1, y1, x2, y2):
        self.board.create_line(x1*32+16, y1*32+16, x2*32+16, y2*32+16, fill="#ff0000")

    def wincheck(self):
        for i in range(5):
            if np.all(self.grid[i,:]==1) or np.all(self.grid[i,:]==2):
                self.winningline(0, i, 4, i)
                return True
            elif np.all(self.grid[:,i]==1) or np.all(self.grid[:,i]==2):
                self.winningline(i, 0, i, 4)
                return True
        if np.all(self.grid[[range(5)], [range(5)]] == 1) or np.all(self.grid[[range(5)], [range(5)]] == 2):
            self.winningline(0, 0, 4, 4)
            return True
        elif np.all(self.grid[[range(4,-1,-1)], [range(5)]] == 1):
            self.winningline(0, 4, 4, 0)
            return True
        elif np.all(self.grid[[range(4,-1,-1)], [range(5)]] == 2):
            self.winningline(0, 4, 4, 0)
            return True
        return False

    def gameover(self):
        global gameover
        gameover = True

    def tiebreaker(self):
        score = [0,0]
        for i in range(5):
            mat = 1
            for lst in self.grid[i, :], self.grid[:, i]:
                for j in range(1,5):
                    if lst[j] == lst[j-1]:
                        mat += 1
                    else:
                        if mat >= 3:
                            score[lst[j-1]-1] += mat*2 + 2*(mat-3)
                        mat = 1
                if mat >= 3:
                    score[lst[j] - 1] += mat * 2 + 2 * (mat - 3)
                mat = 1
        for i, j in zip([0,1,2,0,0], [4, 4, 4, 3, 2]):
            mat = 1
            lst = self.grid[[range(i, j+1)], [range(4-j,4-i+1)]][0]
            for k in range(1, len(lst)):
                if lst[k] == lst[k-1]:
                    mat += 1
                else:
                    if mat >= 3:
                        score[lst[k-1]-1] += mat*2 + 2*(mat-3)
                    mat = 1
            if mat >= 3:
                score[lst[k] - 1] += mat * 2 + 2 * (mat - 3)
        for i, j in zip([2, 3, 4, 4, 4], [0, 0, 0, 1, 2]):
            mat = 1
            lst = self.grid[[range(i, j-1, -1)], [range(j, i+1)]][0]
            for k in range(1, len(lst)):
                if lst[k] == lst[k-1]:
                    mat += 1
                else:
                    if mat >= 3:
                        score[lst[k-1]-1] += mat*2 + 2*(mat-3)
                    mat = 1
            if mat >= 3:
                score[lst[k] - 1] += mat * 2 + 2 * (mat - 3)
        if score[0] == score[1]:
            Label(self.root, text = "Match Tied").grid(row=2, column=0)
        else:
            Label(self.root, text = f"Player {score.index(max(score))+1} has won!").grid(row=2, column=0)
        Label(self.root, text = f"P1: {score[0]}, P2: {score[1]}").grid(row=3, column=0)

gameover = False
root = Tk()

sp_cross = PImage.open("Cross2.png")
tk_cross = ImageTk.PhotoImage(sp_cross)
sp_circle = PImage.open("Circle2.png")
tk_circle = ImageTk.PhotoImage(sp_circle)

board = Board(root, tk_cross, tk_circle)
root.mainloop()
