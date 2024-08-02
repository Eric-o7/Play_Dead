import tkinter as tk
from tkinter import ttk
from random import randint, choice

root2 = tk.Tk()


# root2.mainloop()

with open("text_files/narrative.txt") as start:
    start = start.readlines()
    count = 0
    beginning = "***TitleStart***"
    end = "***TitleEnd***"
    section = []
    for line in start:
        if beginning in line:
            section.append(count)
        if end in line:
            section.append(count)
        count += 1
    print(section)
    print(start[section[0]:section[1]])
#frame usage makes it easier to re-use widgets