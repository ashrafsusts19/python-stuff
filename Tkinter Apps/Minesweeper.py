"""
stack = list of index to check
closed = list of buttons disabled
examine(index) = examines the surrounding of map[index]
    examine doesn't pop
"""

from tkinter import *
import random

def click(index):
    global mfield, map, fr_dbar, stack, closed, row, col, bomb, isgameover
    if index in closed or isgameover:
        return
    if map[index] == "b":
        lab_over = Label(fr_dbar, text = "Game Over! You lost")
        lab_over.pack()
        game_over()
        return
    stack.append(index)
    while len(stack) > 0:
        cl_ind = stack[-1]
        cl_exam = examine(cl_ind)
        closed.append(cl_ind)
        stack.pop()
        if cl_exam == 0:
            for i in surrounding(cl_ind):
                if i not in closed and i not in stack:
                    stack.append(i)
            mfield[cl_ind].config(bg = "grey")
        else:
            mfield[cl_ind].config(text = str(cl_exam))
    if len(closed) == row*col-bomb:
        lab_over = Label(fr_dbar, text="You Won!")
        lab_over.pack()
        game_over()


def surrounding(index):
    global row, col
    tst = []
    for c in [-col,0,col]:
        if index + c <0 or index+c >= row*col:
            continue
        for i in [-1,0,1]:
            if index//col != (index+i)//col:
                continue
            tst.append(index+c+i)
    tst.remove(index)
    return tst


def examine(index):
    tot = 0
    for i in surrounding(index):
        if map[i]=="b":
            tot+=1
    return tot



def first_click(index):
    global map, row, col, bomb, mfield
    map = ["b" for i in range(bomb)] + ["" for i in range(row * col - bomb)]
    random.shuffle(map)
    while map[index] == "b":
        random.shuffle(map)
    for i in range(row * col):
        mfield[i].config(command=lambda x=i: click(x))
    click(index)


def game_over():
    global isgameover
    isgameover = True
    for i in range(row*col):
        if map[i] == "b":
            mfield[i].config(text="B")


isgameover = False
row = 10
col = 10
bomb = 10

root = Tk()

fr_game = LabelFrame(root)
fr_game.grid(row=1, column=0)

fr_dbar = LabelFrame(root)
fr_dbar.grid(row=2, column=0)


stack = []
closed = []

map = ["b" for i in range(bomb)] + ["" for i in range(row*col-bomb)]
random.shuffle(map)

mfield = []
for i in range(row*col):
    mfield.append(Button(fr_game, text= "   ", command= lambda x=i: first_click(x)))
    mfield[i].grid(row=i//col, column= i%col)

root.mainloop()
