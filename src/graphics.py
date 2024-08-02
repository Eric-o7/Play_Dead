import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("800x600")
root.title("Start Game")
root.configure(background = "#212121")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 5)
root.rowconfigure(0, weight = 5)
root.rowconfigure(1, weight = 5)
root.rowconfigure(2, weight = 2)



#button frame

button_frame = ttk.Frame(root, style = "primary.TFrame")
button_frame.grid(row = 0, column = 0, sticky = "nsew")

button_frame.columnconfigure(0, weight = 1)
button_frame.rowconfigure(0, weight = 1)
button_frame.rowconfigure(1, weight = 1)
button_frame.rowconfigure(2, weight = 1)
button_frame.rowconfigure(3, weight = 1)
button_frame.rowconfigure(4, weight = 1)

help_button = ttk.Button(button_frame, text = "Help")
help_button.grid(row = 0, column = 0)

inventory_button = ttk.Button(button_frame, text = "Inventory")
inventory_button.grid(row = 1, column = 0)

spells_button = ttk.Button(button_frame, text = "Spells")
spells_button.grid(row = 2, column = 0)

styles_button = ttk.Button(button_frame, text = "Styles")
styles_button.grid(row = 3, column = 0)

#status frame
status_frame = ttk.Frame(root)
status_frame.grid(row = 1, column = 0, rowspan = 2, 
                  sticky = "nsew", padx = 5, pady = (5,15))

label = ttk.Label(status_frame, background = "#373737", 
                  text = "Status box", anchor = "n")
label.pack(expand = True, fill = "both")

#game output frame
text_frame = ttk.Frame(root)
text_frame.grid(row = 0, column = 1, rowspan = 2, sticky = "nsew")

game_text = tk.Text(text_frame, background = "#212121", 
                            wrap = "word"
)                  
game_text.pack(expand = True, fill = 'both')

#output tags
game_text.tag_configure("title", background = "#212121", 
                        font=("Times New Roman", 12, "bold"), 
                        foreground = "#9B61AB")
game_text.tag_configure("user", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#D7D7D7")
game_text.tag_configure("output", background = "#212121",
                        font=("Times New Roman", 12, "bold"),
                        foreground = "#759EE0")

#output to text box with optional text arguments
def game_out(text, tags = "user"):
    game_text.configure(state = "normal")
    game_text.insert(tk.END, f"{text}\n", tags)
    game_text.configure(state = "disabled")
    game_text.see(tk.END)

#display content and progress game using gamestate()
def add_to_game_out(event=None):
    from main import gamestate, gstate
    text = text_entry.get()
    text_entry.delete(0, tk.END)
    print(f"State: {gstate}")
    return gamestate(text)

#title/credits printed upon execution
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
    for line in range(section[0]+1, section[1]):
        game_out(start[line], "title")


#game input frame    
entry_frame = ttk.Frame(root)
entry_frame.grid(row = 2, column = 1, sticky = "ew", padx = 20)

entry_frame.columnconfigure(0, weight = 25)
entry_frame.columnconfigure(1, weight = 2)

text_entry = ttk.Entry(entry_frame)
text_entry.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")
text_entry.focus()

text_entry.bind("<Return>", add_to_game_out)

enter_button = ttk.Button(entry_frame, text = "Enter", command = add_to_game_out())
enter_button.grid(row = 0, column = 1, sticky = "nsew")







