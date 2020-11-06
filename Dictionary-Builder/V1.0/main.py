from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import re
import json

specialwords = 4
specialcommands = ["_Cusd?_", "_Lang1_", "_Lang2_", "_Rwordlist_"]

def save_button():
    global button_save, dicfile, wordlist, rwordlist, save_location
    fname = entry_filename.get()
    if len(fname) < 1:
        messagebox.showerror("Error!", "File Name Required!")
        return
    location = filedialog.askdirectory()
    if len(location) < 1:
        return
    lang1 = entry_name1.get()
    if len(lang1) < 1:
        lang1 = "Language 1"
    lang2 = entry_name2.get()
    if len(lang2) < 1:
        lang2 = "Language 2"
    save_location = location + "/" + fname + ".json"
    wordlist = {}
    wordlist["_Lang1_"] = lang1
    wordlist["_Lang2_"] = lang2
    wordlist["_Cusd?_"] = True
    wordlist["_Rwordlist_"] = {}
    rwordlist = {}
    with open(save_location, "w+") as fle:
        json.dump(wordlist, fle)
    label_name1.destroy()
    entry_name1.destroy()
    label_name2.destroy()
    entry_name2.destroy()
    label_filename.destroy()
    entry_filename.destroy()
    button_save.destroy()
    openfile(wordlist["_Lang1_"], wordlist["_Lang2_"])
    button_save = Button(root, text="Save", command=resave_button)
    button_save.grid(row=4, column=2)


def resave_button():
    global wordlist, save_location, rwordlist
    response = messagebox.askyesno("Save", "Save and Overwrite?")
    wordlist["_Rwordlist_"] = {}
    wordlist["_Rwordlist_"] = rwordlist.copy()
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

    button_list_of_words = Button(root, text="Words", command=list_of_words_button)
    button_list_of_words.grid(row=5, column=1)


def translate():
    global wordlist, rwordlist, stat_wordcount, stat_rwordcount, specialwords
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
            stat_wordcount = Label(stat_window, text=str(len(wordlist) - specialwords))
            stat_wordcount.grid(row=0, column=1)
            stat_rwordcount = Label(stat_window, text=str(len(rwordlist)))
            stat_rwordcount.grid(row=1, column=1)
        except:
            pass
    elif len(word1) == 0:
        try:
            eword1.insert(0, rwordlist[word2][0])
        except:
            messagebox.showerror("Error!", "Word Not Found")
    else:
        try:
            eword2.insert(0, wordlist[word1][0])
        except:
            messagebox.showerror("Error!", "Word Not Found")


def load_button():
    global wordlist, rwordlist, save_location
    global label_name1, entry_name1, label_name2, entry_name2, label_filename, entry_filename, button_save
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
                try:
                    rwordlist = wordlist["_Rwordlist_"].copy()
                except:
                    wordlist = None
                    save_location = None
                    messagebox.showerror("Error Code 2", "Incompatible Version")
                    return

        except:
            messagebox.showerror("Error Code 3", "Invalid File")
            return
        label_name1.destroy()
        entry_name1.destroy()
        label_name2.destroy()
        entry_name2.destroy()
        label_filename.destroy()
        entry_filename.destroy()
        button_save.destroy()
        openfile(wordlist["_Lang1_"], wordlist["_Lang2_"])
        button_save = Button(root, text="Save", command=resave_button)
        button_save.grid(row=4, column=2)


def stats_button():
    global stat_window, stat_wordcount, stat_rwordcount, wordlist, rwordlist, stat_lang1, stat_lang2, specialwords
    stat_window = Toplevel()
    stat_lang1 = Label(stat_window, text=wordlist["_Lang1_"] + ":")
    stat_lang1.grid(row=0, column=0)
    stat_lang2 = Label(stat_window, text=wordlist["_Lang2_"] + ":")
    stat_lang2.grid(row=1, column=0)
    stat_wordcount = Label(stat_window, text=str(len(wordlist) - specialwords))
    stat_wordcount.grid(row=0, column=1)
    stat_rwordcount = Label(stat_window, text=str(len(rwordlist)))
    stat_rwordcount.grid(row=1, column=1)

    """Debug"""
    """
    print(wordlist)
    print(rwordlist)
    """

def list_of_words_button():
    global words_window, wordlist, button_words, specialcommands
    global frame_words, frame_meanings, list_words, list_meanings, frame_ww_buttons
    words_window = Toplevel()

    frame_words = LabelFrame(words_window, text="Word List")
    frame_words.grid(row=0, column=0)

    frame_meanings = LabelFrame(words_window, text="Meanings")
    frame_meanings.grid(row=0, column=1)

    scroll_words = Scrollbar(frame_words)
    scroll_words.pack(side=RIGHT, fill=Y)

    list_words = Listbox(frame_words, height = 20, width = 30, yscrollcommand = scroll_words.set)
    list_words.bind("<Double-Button-1>", generate_meaning_list)
    list_words.pack()

    scroll_words.config(command = list_words.yview)

    for (i, j) in wordlist.items():
        if i in specialcommands:
            continue
        list_words.insert(END, i)

    scroll_meanings = Scrollbar(frame_meanings)
    scroll_meanings.pack(side = RIGHT, fill = Y)

    list_meanings = Listbox(frame_meanings, height = 20, width = 30, yscrollcommand = scroll_meanings.set)
    list_meanings.pack()

    scroll_meanings.config(command = list_meanings.yview)



def generate_meaning_list(event):
    global wordlist, list_meanings, list_words
    list_meanings.delete(0, END)
    for i in wordlist[list_words.get(ANCHOR)]:
        list_meanings.insert(END, i)



root = Tk()


label_name1 = Label(root, text="Language 1")
label_name1.grid(row=0, column=0)

entry_name1 = Entry(root)
entry_name1.grid(row=0, column=1, columnspan=2)

label_name2 = Label(root, text="Language 2")
label_name2.grid(row=1, column=0)

entry_name2 = Entry(root)
entry_name2.grid(row=1, column=1, columnspan=2)

label_filename = Label(root, text="File name")
label_filename.grid(row=2, column=0)

entry_filename = Entry(root)
entry_filename.grid(row=2, column=1, columnspan=2)

button_load = Button(root, text="Load", command=load_button)
button_load.grid(row=4, column=0)

button_save = Button(root, text="Save", command=save_button)
button_save.grid(row=4, column=2)



root.mainloop()

"""
Variables:
    main menu:
        name1, name2, filename = lang 1, lang 2, file name Label
        name1e, name2e, efilename = entry field
        load, save = load and save button
"""
