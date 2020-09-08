from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import re
import json


def save_button():
    global save, dicfile, wordlist, rwordlist, save_location
    fname = efilename.get()
    if len(fname) < 1:
        messagebox.showerror("Error!", "File Name Required!")
        return
    location = filedialog.askdirectory()
    if len(location) < 1:
        return
    lang1 = name1e.get()
    if len(lang1) < 1:
        lang1 = "Language 1"
    lang2 = name2e.get()
    if len(lang2) < 1:
        lang2 = "Language 2"
    save_location = location + "/" + fname + ".json"
    wordlist = {}
    wordlist["_Lang1_"] = lang1
    wordlist["_Lang2_"] = lang2
    wordlist["_Cusd?_"] = True
    rwordlist = {}
    with open(save_location, "w+") as fle:
        json.dump(wordlist, fle)
    name1.destroy()
    name1e.destroy()
    name2.destroy()
    name2e.destroy()
    filename.destroy()
    efilename.destroy()
    save.destroy()
    openfile(wordlist["_Lang1_"], wordlist["_Lang2_"])
    save = Button(root, text="Save", command=resave_button)
    save.grid(row=4, column=2)


def resave_button():
    global wordlist, save_location
    response = messagebox.askyesno("Save", "Save and Overwrite?")
    if response == True:
        with open(save_location, "w+") as fle:
            json.dump(wordlist, fle)


def openfile(str1, str2):
    global lan1, lan2, eword1, eword2, trans, gap1, gap2, bstats
    lan1 = Label(root, text=str1)
    lan1.grid(row=0, column=0)

    lan2 = Label(root, text=str2)
    lan2.grid(row=0, column=2)

    eword1 = Entry(root)
    eword1.grid(row=1, column=0)

    eword2 = Entry(root)
    eword2.grid(row=1, column=2)

    trans = Button(root, text="<<->>", command=translate)
    trans.grid(row=1, column=1)

    gap1 = Label(root).grid(row=2, column=0)
    gap2 = Label(root).grid(row=3, column=0)

    bstats = Button(root, text="Stats", command=stats_button)
    bstats.grid(row=4, column=1)


def translate():
    global wordlist, rwordlist, stat_wordcount, stat_rwordcount
    word1 = eword1.get().lower()
    word2 = eword2.get().lower()
    if len(word1) > 0 and len(word2) > 0:
        try:
            if word2 not in wordlist[word1]:
                wordlist[word1].append(word2)
        except:
            wordlist[word1] = [word2]
        try:
            if word1 not in rwordlist[word2]:
                rwordlist[word2].append(word1)
        except:
            rwordlist[word2] = [word1]
        try:
            stat_wordcount.destroy()
            stat_rwordcount.destroy()
            stat_wordcount = Label(stat_window, text=str(len(wordlist) - 3))
            stat_wordcount.grid(row=0, column=1)
            stat_rwordcount = Label(stat_window, text=str(len(rwordlist)))
            stat_rwordcount.grid(row=1, column=1)
        except:
            pass
    elif len(word1) == 0:
        try:
            eword1.insert(0, rwordlist[word2[0]])
        except:
            messagebox.showerror("Error!", "Word Not Found")
    else:
        try:
            eword2.insert(0, wordlist[word1[0]])
        except:
            messagebox.showerror("Error!", "Word Not Found")


def load_button():
    global wordlist, rwordlist, save_location
    global name1, name1e, name2, name2e, filename, efilename, save
    save_location = filedialog.askopenfilename(title="Load File", filetypes=(("JSON File", "*.*"), ("All files", "*.*")))
    if len(save_location) > 0:
        try:
            with open(save_location, "r+") as fle:
                wordlist = json.load(fle)
                try:
                    if wordlist["_Cusd?_"] != True:
                        wordlist = None
                        save_location = None
                        messagebox.showerror("Error Code 0", "Invalid File")
                        return
                except:
                    wordlist = None
                    save_location = None
                    messagebox.showerror("Error Code 1", "Invalid File")
                    return
                rwordlist = {}
                for key in wordlist:
                    if key == "_Cusd?_" or key == "_Lang1_" or key == "_Lang2_":
                        continue
                    for item in wordlist[key]:
                        try:
                            rwordlist[item].append(key)
                        except:
                            rwordlist[item] = [key]
        except:
            messagebox.showerror("Error Code 3", "Invalid File")
            return
        name1.destroy()
        name1e.destroy()
        name2.destroy()
        name2e.destroy()
        filename.destroy()
        efilename.destroy()
        save.destroy()
        openfile(wordlist["_Lang1_"], wordlist["_Lang2_"])
        save = Button(root, text="Save", command=resave_button)
        save.grid(row=4, column=2)


def stats_button():
    global stat_window, stat_wordcount, stat_rwordcount, wordlist, rwordlist, stat_lang1, stat_lang2
    stat_window = Toplevel()
    stat_lang1 = Label(stat_window, text=wordlist["_Lang1_"] + ":")
    stat_lang1.grid(row=0, column=0)
    stat_lang2 = Label(stat_window, text=wordlist["_Lang2_"] + ":")
    stat_lang2.grid(row=1, column=0)
    stat_wordcount = Label(stat_window, text=str(len(wordlist) - 3))
    stat_wordcount.grid(row=0, column=1)
    stat_rwordcount = Label(stat_window, text=str(len(rwordlist)))
    stat_rwordcount.grid(row=1, column=1)
    print(wordlist)
    print(rwordlist)


root = Tk()

name1 = Label(root, text="Language 1")
name1.grid(row=0, column=0)

name1e = Entry(root)
name1e.grid(row=0, column=1, columnspan=2)

name2 = Label(root, text="Language 2")
name2.grid(row=1, column=0)

name2e = Entry(root)
name2e.grid(row=1, column=1, columnspan=2)

filename = Label(root, text="File name")
filename.grid(row=2, column=0)

efilename = Entry(root)
efilename.grid(row=2, column=1, columnspan=2)

load = Button(root, text="Load", command=load_button)
load.grid(row=4, column=0)

save = Button(root, text="Save", command=save_button)
save.grid(row=4, column=2)

root.mainloop()
