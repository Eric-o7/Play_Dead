import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


root = ctk.CTk()
root.geometry("800x600")
root.title("Start Game")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=15)
root.rowconfigure(0, weight=10)
root.rowconfigure(1, weight=5)
root.rowconfigure(2, weight=1)

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

inventory_button = ctk.CTkButton(button_frame, text="Inventory", fg_color="gray")
inventory_button.grid(row=1, column=0)

spells_button = ctk.CTkButton(button_frame, text="Spells", fg_color="gray")
spells_button.grid(row=2, column=0)

styles_button = ctk.CTkButton(button_frame, text="Styles", fg_color="gray")
styles_button.grid(row=3, column=0)

#status frame
status_frame = ctk.CTkFrame(root)
status_frame.grid(row=1, column=0, rowspan = 2, sticky='nsew', padx=5, pady = 5)

label = ctk.CTkLabel(status_frame, bg_color="white", text="Status box", anchor="n",font=(("<Arial>"), 16))
label.pack(expand=True, fill='both')

#game output frame
text_frame = ctk.CTkFrame(root)
text_frame.grid(row=0, column=1, rowspan = 2, sticky="nsew")

label = ctk.CTkLabel(text_frame, bg_color="white", text="Game Output", anchor="s", font=(("<Arial>"), 22))
label.pack(expand=True, fill='both')

#game input frame
entry_frame = ctk.CTkFrame(root)
entry_frame.grid(row=2, column=1, sticky="ew", padx=20)

entry_frame.columnconfigure(0, weight=15)
entry_frame.columnconfigure(1, weight=2)

text_entry = ctk.CTkEntry(entry_frame)
text_entry.grid(row=0, column=0, sticky="nsew")

enter_button = ctk.CTkButton(entry_frame, text="Enter")
enter_button.grid(row=0, column=1, sticky='nsew')



root.mainloop()

