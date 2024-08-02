import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
ctk.set_appearance_mode("dark")


root = ctk.CTk()
root.geometry("800x600")
root.title("Start Game")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=15)
root.rowconfigure(0, weight=10)
root.rowconfigure(1, weight=5)
root.rowconfigure(2, weight=1)

#CTkFont
standard_font = ctk.CTkFont(family=("<Arial>", 12))

#button frame
button_frame = ctk.CTkFrame(root)
button_frame.grid(row=0, column=0, sticky="nsew")

button_frame.columnconfigure(0, weight=1)
button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(1, weight=1)
button_frame.rowconfigure(2, weight=1)
button_frame.rowconfigure(3, weight=1)
button_frame.rowconfigure(4, weight=1)

help_button = ctk.CTkButton(button_frame, text="Help", fg_color="gray")
help_button.grid(row=0, column=0)

inventory_button = ctk.CTkButton(button_frame, text="Inventory")
inventory_button.grid(row=1, column=0)

spells_button = ctk.CTkButton(button_frame, text="Spells")
spells_button.grid(row=2, column=0)

styles_button = ctk.CTkButton(button_frame, text="Styles")
styles_button.grid(row=3, column=0)

#status frame
status_frame = ctk.CTkFrame(root, bg_color="#212121")
status_frame.grid(row=1, column=0, rowspan = 2, sticky="nsew", padx=5, pady = (5,15))

label = ctk.CTkLabel(status_frame, bg_color="#212121", text="Status box", anchor="n",font=standard_font)
label.pack(expand=True, fill="both")

#game output frame
text_frame = ctk.CTkFrame(root)
text_frame.grid(row=0, column=1, rowspan = 2, sticky="nsew")

game_text = ctk.CTkTextbox(text_frame, height=200, 
                           width=200, fg_color ="#212121",
                           scrollbar_button_color="#161618",  
                            wrap="word",
                           font=standard_font
)
                           
game_text.pack(expand=True, fill='both')

#output to text box with optional text arguments
def game_out(text, font=standard_font, text_color="#b3afb1"):
    game_text.configure(state="normal", font=font, text_color=text_color)
    game_text.insert(ctk.END, f"{text}\n")
    game_text.configure(state="disabled")
    game_text.see(ctk.END)

#game input frame

#get content in text_entry and display in game_text with link to game_out()
def add_to_game_out(event=None):
    text = text_entry.get()
    if text:
        game_out(text)
        text_entry.delete(0, ctk.END)
        
entry_frame = ctk.CTkFrame(root)
entry_frame.grid(row=2, column=1, sticky="ew", padx=20)

entry_frame.columnconfigure(0, weight=15)
entry_frame.columnconfigure(1, weight=2)

text_entry = ctk.CTkEntry(entry_frame, placeholder_text="Press Enter or click Enter button to input commands")
text_entry.grid(row=0, column=0, sticky="nsew")
text_entry.focus()

text_entry.bind("<Return>", add_to_game_out)

enter_button = ctk.CTkButton(entry_frame, text="Enter", fg_color="gray", command=add_to_game_out)
enter_button.grid(row=0, column=1, sticky="nsew")

with open("startgame.txt") as start:
    for line in start:
        game_out(line, font=("<Times>", 18), text_color="#961113")
    
root.mainloop()


