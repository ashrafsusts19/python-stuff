from tkinter import *
from PIL import Image as PImage, ImageTk
import random


def calc(x1, y1):
    return (x1*32, y1*32+8, (x1+1)*32, (y1+1)*32+8)


def count(item):
    global slot_index
    tot = 0
    for i in slot_index:
        if i == item:
            tot += 1
    return tot


def select_slot(ind):
    global slot_index, slot_but, isselected, cb_reswap, tk_slot_images, game_score, game_tries
    global lb_tries, lb_score, lb_gameover, frame_score, matches_ind
    if ind in matches_ind or cb_reswap is not None:
        return
    if isselected is None:
        isselected = ind
        slot_but[ind].config(image = tk_slot_images[ind])
    else:
        slot_but[ind].config(image=tk_slot_images[ind])
        game_tries += 1
        lb_tries.config(text = f"Tries: {game_tries}")
        if slot_index[ind] == slot_index[isselected]:
            matches_ind.append(ind)
            matches_ind.append(isselected)
            game_score += 1
            lb_score.config(text = f"Score: {game_score}")
            if game_score == 32:
                lb_gameover = Label(frame_score, text= "You Have Won!")
                lb_gameover.grid(row=2, column=0)
        if slot_index[ind] != slot_index[isselected]:
            cb_reswap = root.after(200, lambda: reswap(ind))
        else:
            isselected = None



def reswap(ind):
    global cb_reswap, isselected, slot_but
    cb_reswap = None
    slot_but[ind].config(image = tk_grass)
    slot_but[isselected].config(image = tk_grass)
    isselected = None


matches_ind = []
game_score = 0
game_tries = 0
isselected = None
cb_reswap = None

root = Tk()

frame_game = LabelFrame(root)
frame_game.grid(row=0, column=0)
frame_score = LabelFrame(root)
frame_score.grid(row=1, column=0)

lb_score = Label(frame_score, text = f"Score: {game_score}")
lb_tries = Label(frame_score, text = f"Tries: {game_tries}")
lb_score.grid(row=0, column=0)
lb_tries.grid(row=1, column=0)

sprites = PImage.open("sprites\\screen_cap_1.png")

sprites_index = [(x, 10) for x in range(11)]
sprites_index += [(11, 7), (1,11), (2,11), (3,11), (2,3), (3,3), (4,3)] + [(x, 4) for x in range(2,10)]
sprites_index += [(x, 3) for x in [7, 8, 10, 11]] + [(x, 5) for x in [2, 4, 6]]

sp_grass = sprites.crop(calc(0,1))
tk_grass = ImageTk.PhotoImage(sp_grass)

slot_index = []

while len(slot_index) < 32:
    slot_item = random.choice(sprites_index)
    if count(slot_item) < 2:
        slot_index.append((slot_item))

slot_index *= 2

random.shuffle(slot_index)

sp_slot_images = []
tk_slot_images = []


for index in slot_index:
    sp_slot_images.append(sprites.crop(calc(index[0], index[1])))

for sp_slot_image in sp_slot_images:
    tk_slot_images.append(ImageTk.PhotoImage(sp_slot_image))



slot_but = []

for i in range(64):
    slot_but.append(Button(frame_game, image= tk_grass, command= lambda x=i: select_slot(x)))
    slot_but[i].grid(row=i//8, column = i%8)

root.mainloop()

