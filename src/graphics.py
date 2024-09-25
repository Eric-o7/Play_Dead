import tkinter as tk
from tkinter import ttk, Toplevel


root = tk.Tk()
root.geometry("800x600")
root.title("Play Dead")
icon = tk.PhotoImage(file="exe/Opossum_Icon.png")
root.iconphoto(True, icon)


root.configure(background = "#212121")

root.columnconfigure(0, weight = 5)
root.columnconfigure(1, weight = 5)
root.rowconfigure(0, weight = 5)
root.rowconfigure(1, weight = 5)
root.rowconfigure(2, weight = 2)

#button frame

button_frame = tk.Frame(root, background = "#212121")
button_frame.grid(row = 0, column = 0, sticky = "nsew")

button_frame.columnconfigure(0, weight = 1)
button_frame.rowconfigure(0, weight = 1)
button_frame.rowconfigure(1, weight = 1)
button_frame.rowconfigure(2, weight = 1)
button_frame.rowconfigure(3, weight = 1)
button_frame.rowconfigure(4, weight = 1)

def close_window(window):
    window.destroy()

def help_read():
    open_help = open("text_files/help.txt")
    read_help = open_help.read()
    return read_help

def help_click():

    pophelp = Toplevel(root)
    pophelp.title("Play Dead Information")
    pophelp.geometry("650x800")
    pophelp.config(bg="#212121")
    
    my_frame = tk.Frame(pophelp, bg="#212121")
    my_frame.pack(expand = True, fill = 'both')
    
    help_info = tk.StringVar(pophelp)
    help_info.set(help_read())
    
    pophelp_text = tk.Label(my_frame, textvariable= help_info, bg="#212121", fg="#6a8758", justify="left", font=("Times", 10, "bold"), wraplength=650)
    pophelp_text.pack(expand=True, fill = 'both')
    
    ok_but = tk.Button(my_frame, text= "Ok", bg="#9c0514", command= lambda: close_window(pophelp))
    ok_but.pack(pady=1)

help_button = tk.Button(button_frame, text = "Help", activebackground="#6a8758", bg="#5d9639", bd=0, relief="groove", command=help_click)
help_button.grid(row = 0, column = 0)

def equip_read():
    import main
    if main.player:
        if main.player.equipment["Mhand"]:
            info = (f"""
    Main Hand: {main.player.equipment["Mhand"].name}\n
    Off Hand: {main.player.equipment["Ohand"].name}\n
    Armor: {main.player.equipment["Armor"].name}\n""")
            return info
    else:
        return "You haven't chosen equipment yet."
        
  
def equip_click():
    popequip = Toplevel(root)
    popequip.title("Equipment")
    popequip.geometry("300x200")
    popequip.config(bg="#212121")
        
    my_frame = tk.Frame(popequip, bg="#212121")
    my_frame.pack(pady=10)
    
    equip_info = tk.StringVar(popequip)
    equip_info.set(equip_read())
    
    popequip_label = tk.Label(my_frame, textvariable=equip_info, bg="#212121", fg="#d9d5e3", justify="left", font=("Times", 12))
    popequip_label.pack(expand=True, fill = 'both')

    ok_but = tk.Button(my_frame, text= "Ok", bg="#9c0514", command= lambda: close_window(popequip))
    ok_but.pack(pady=1)

equipment_button = tk.Button(button_frame, text = "Equipment", activebackground= "#d9d5e3", bg = "#554c73",command=equip_click)
equipment_button.grid(row = 1, column = 0)

def spells_read():
    import main
    if main.player:
        if len(main.player.spells) > 0:
            info = (f"""
Spell List:\n
{[spell.name for spell in main.player.spells]}""")
            return info
    else:
        return "You haven't chosen any spells yet."

def spells_click():
    popspells = Toplevel(root)
    popspells.title("Spells")
    popspells.geometry("300x200")
    popspells.config(bg="#212121")
    
    my_frame = tk.Frame(popspells, bg="#212121")
    my_frame.pack(pady=10)
    
    spells_info = tk.StringVar(popspells)
    spells_info.set(spells_read())
    
    popspells_label = tk.Label(my_frame, textvariable=spells_info, bg="#212121", fg="#1587cf", justify="left", font=("Times", 12))
    popspells_label.pack(expand=True, fill = 'both')
    
    ok_but = tk.Button(my_frame, text= "Ok", bg="#9c0514", command= lambda: close_window(popspells))
    ok_but.pack(pady=1)

spells_button = tk.Button(button_frame, text = "Spells",activebackground= "#d9d5e3", bg="#1587cf", command=spells_click)
spells_button.grid(row = 2, column = 0)

def styles_read():
    import main
    if main.player:
        if len(main.player.styles) > 0:
            info = (f"""
Styles List:\n
{[style.name for style in main.player.styles]}""")
            return info
    else:
        return "You haven't chosen any styles yet."

def styles_click():
    popstyles = Toplevel(root)
    popstyles.title("Styles")
    popstyles.geometry("300x200")
    popstyles.config(bg="#212121")
    
    my_frame = tk.Frame(popstyles, bg="#212121")
    my_frame.pack(pady=10)
    
    styles_info = tk.StringVar(popstyles)
    styles_info.set(styles_read())
    
    popstyles_label = tk.Label(my_frame, textvariable=styles_info, bg="#212121", fg="#20ab81", justify="left", font=("Times", 12))
    popstyles_label.pack(expand=True, fill = 'both')
    
    ok_but = tk.Button(my_frame, text= "Ok", bg="#9c0514", command= lambda: close_window(popstyles))
    ok_but.pack(pady=1)

styles_button = tk.Button(button_frame, text = "Styles",activebackground= "#d9d5e3", bg="#20ab81",command=styles_click)
styles_button.grid(row = 3, column = 0)

#status frame
status_frame = tk.Frame(root)
status_frame.grid(row = 1, column = 0, rowspan = 2, 
                  sticky = "nsew", padx = 5, pady = (5,15))

char_stats = tk.StringVar()

label = tk.Label(status_frame, background = "#373737", foreground = "#b5880b",
                 textvariable = char_stats, height = 13,
                  anchor = tk.NW, borderwidth = 2, relief = "groove",
                  justify = tk.LEFT, font = ("Times", 11, "bold"))
label.pack(expand = True, fill = "both")

#game output frame
text_frame = tk.Frame(root)
text_frame.grid(row = 0, column = 1, rowspan = 2, sticky = "nsew")

game_text = tk.Text(text_frame, background = "#212121", 
                            wrap = "word"
)                  
game_text.pack(expand = True, fill = 'both')

#output tags
game_text.tag_configure("purple_bold", background = "#212121", 
                        font=("Times New Roman", 12, "bold"), 
                        foreground = "#9B61AB")
game_text.tag_configure("user", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#D7D7D7")
game_text.tag_configure("blue_bold", background = "#212121",
                        font=("Times New Roman", 12, "bold"),
                        foreground = "#759EE0")
game_text.tag_configure("blue", background = "#212121",
                        font=("Times New Roman", 11),
                        foreground = "#759EE0")
game_text.tag_configure("purple", background = "#212121", 
                        font=("Times New Roman", 12), 
                        foreground = "#9B61AB")
game_text.tag_configure("error", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#e02012")
game_text.tag_configure("dot", background = "#e6dada", 
                        font=("Times New Roman", 9, "bold"), 
                        foreground = "#910606")
game_text.tag_configure("combat", background = "#661209", 
                        font=("Times New Roman", 11, "bold"), 
                        foreground = "#bdaeb2")
game_text.tag_configure("combat_npc", background = "#661209", 
                        font=("Times New Roman", 11), 
                        foreground = "#e86427")
game_text.tag_configure("combat_pc", background = "#241773", 
                        font=("Times New Roman", 11), 
                        foreground = "#bdaeb2")
game_text.tag_configure("combat_pc_question", background = "#241773", 
                        font=("Times New Roman", 11, "bold"), 
                        foreground = "#9E7C0C")
game_text.tag_configure("effects", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#9E7C0C")
game_text.tag_configure("spells", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#1587cf")
game_text.tag_configure("styles", background = "#212121", 
                        font=("Times New Roman", 11), 
                        foreground = "#20ab81")
game_text.tag_configure("damage", background = "#212121", 
                        font=("Times New Roman", 11, "bold"), 
                        foreground = "#bd1f11")




#output to text box with optional text arguments
def game_out(text, tags = "user"):
    game_text.configure(state = "normal")
    game_text.insert(tk.END, f"{text}\n", tags)
    game_text.configure(state = "disabled")
    game_text.see(tk.END)
    
def typing_animation(text, tags = "user", text_index = 0):
    if text_index < len(text):
        tag_arg = tags
        letter = text[text_index]
        game_text.configure(state = "normal")
        game_text.insert(tk.END, letter, tags)
        game_text.configure(state = "disabled")
        game_text.see(tk.END)
        text_index += 1
        game_text.after(30, typing_animation, text, tag_arg, text_index)
    return


#display content and progress game using gamestate()
def add_to_game_out(event=None):
    from main import gamestate_bus, combatstate, combatstate_bus,  restart_combat, combat_order, reset_game
    if text_entry.get():
        text = text_entry.get()
        if text.lower() in {"reset", "restart"}:
            if text.lower() == "reset":
                reset_game()
            else:
                if combatstate > 1:
                    restart_combat()
                else:
                    game_out(f"You're currently not in combat", "error")
            text_entry.delete(0, tk.END)
            return
        text_entry.delete(0, tk.END)
        # print(f"State: {gamestate}")
        if combatstate > 1:
            return combatstate_bus(text)
        return gamestate_bus(text)
    
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
    for line in range(section[0]+1, section[1]):
        game_out(start[line], "purple_bold")

#game input frame    
entry_frame = tk.Frame(root, background = "#212121")
entry_frame.grid(row = 2, column = 1, sticky = "ew", padx = (15,5))

entry_frame.columnconfigure(0, weight = 25)
entry_frame.columnconfigure(1, weight = 2)

text_entry = ttk.Entry(entry_frame)
text_entry.grid(row = 0, column = 0, sticky = "nsew")
text_entry.focus()

text_entry.bind("<Return>", add_to_game_out)

enter_button = tk.Button(entry_frame, bg="#241773", fg="white", text = "Enter", command = add_to_game_out)
enter_button.grid(row = 0, column = 1, sticky = "nsew", padx = 10)

