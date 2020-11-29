from tkinter import *
from PIL import Image as PImage, ImageTk, ImageDraw
import random


def calc(x1, y1, x2, y2):
    return (x1*32, y1*32+8, x2*32, y2*32+8)


def retry():
    global lab_res, but_re, isstopped, isstarted
    lab_res.destroy()
    but_re.destroy()
    isstarted = False
    for i in range(slot_num):
        isstopped[i] = False



def result():
    global win_slot, slot_index, lab_res, but_re
    win_slot = slot_index[0]
    i = 0
    while i < len(slot_index) and slot_index[i] == win_slot:
        i += 1
    if i == slot_num:
        lab_res = Label(root, text = "You Won!")
    else:
        lab_res = Label(root, text = "You lost!")
    lab_res.grid(row=1, column=0, columnspan = 4)
    but_re = Button(root, text="Retry", command = retry)
    but_re.grid(row=2, column=0)

def start():
    global isstopped, but_slots, tk_slot_images, isstarted, callback_start
    isstarted = True
    for i in range(len(but_slots)):
        if isstopped[i] == False:
            j = random.randint(0, len(tk_slot_images)-1)
            slot_index[i] = j
            but_slots[i].config(image = tk_slot_images[j])
    if False in isstopped:
        callback_start = root.after(100, start)
    else:
        result()


def slot_select(i):
    global isstopped
    isstopped[i] = True


root = Tk()

slot_num = 3
isstarted = False
isstopped = []
for i in range(slot_num):
    isstopped.append(False)

slot_index = []
for i in range(slot_num):
    slot_index.append(-1)

sprites = PImage.open("sprites\\screen_cap_1.png")

sp_slot_images = []

for i in range(11):
    if i==4:
        continue
    sp_slot_images.append(sprites.crop(calc(i, 10, i + 1, 11)))

tk_slot_images = []

for sp_slot_image in sp_slot_images:
    tk_slot_images.append(ImageTk.PhotoImage(sp_slot_image))

but_start = Button(root, text = "Start", command=start)
but_start.grid(row =0, column =0)

but_slots = []
for i in range(slot_num):
    but_slots.append(Button(root, text = "     ", command = lambda x=i: slot_select(x)))
    but_slots[i].grid(row=0, column=i+1)

root.mainloop()
