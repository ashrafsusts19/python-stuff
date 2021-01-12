from tkinter import *
import random

def click(index):
    global mfield, map, fr_dbar, stack, closed, row, col, bomb, isgameover, flag_map, flags, lab_flag
    if index in closed or isgameover or index in flag_map:
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
    for i in flag_map:
        if i in closed:
            mfield[i].config(text="   ", fg="black")
            flags += 1
            flag_map.remove(i)
    lab_flag.config(text="Flags: " + str(flags))
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
    global map, row, col, bomb, mfield, lab_flag, flags
    map = ["b" for i in range(bomb)] + ["" for i in range(row * col - bomb)]
    random.shuffle(map)
    while map[index] == "b":
        random.shuffle(map)
    for i in range(row * col):
        mfield[i].config(command=lambda x=i: click(x))
        mfield[i].bind('<Button-3>', lambda eff, x=i: rightclick(event=eff, index=x))
    lab_flag.config(text="Flags: "+str(flags))
    click(index)


def game_over():
    global isgameover
    isgameover = True
    for i in range(row*col):
        if map[i] == "b":
            mfield[i].config(text="B", fg= "red")


def rightclick(event, index):
    global flag_map, closed, mfield, flags, lab_flag
    if index in closed or isgameover:
        return
    if index in flag_map:
        mfield[index].config(text="   ", fg = "black")
        flags += 1
        flag_map.remove(index)
    elif flags>0:
        mfield[index].config(text=" ! ", fg="blue")
        flags -= 1
        flag_map.append(index)
    lab_flag.config(text="Flags: "+str(flags))


isgameover = False
row = 10
col = 10
bomb = 10
flags = bomb

root = Tk()

fr_tbar = LabelFrame(root)
fr_tbar.grid(row=0, column=0)

fr_game = LabelFrame(root)
fr_game.grid(row=1, column=0)

fr_dbar = LabelFrame(root)
fr_dbar.grid(row=2, column=0)

lab_flag = Label(fr_tbar, text = "Flags: --")
lab_flag.grid(row=0, column=0)

stack = []
closed = []
flag_map = []

mfield = []
for i in range(row*col):
    mfield.append(Button(fr_game, text= "   ", command= lambda x=i: first_click(x)))
    mfield[i].grid(row=i//col, column= i%col)

root.mainloop()
