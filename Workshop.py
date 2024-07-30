import tkinter as tk
from tkinter import ttk


#helper function - window pop up to test tkinter is installed and ready to use
# tk._test()

# def on_click():
#     lbl.config(text="Button Clicked")
#     #a method to print to GUI

# lbl = tk.Label(root, text="Label 1", bg="green", relief="raised")
# lbl.grid(row=0, column=0)

# #keys available to a widget, in this case lbl = Label.
# print(lbl.config().keys())

# btn = tk.Button(root, text="Button 1", command=on_click)
# btn.grid(row=0, column=1)

root = tk.Tk()
root.title("Testing Tkinter")

#event argument to allow event to control the function - must also add the function to the entry.bind() method
#event=None is the argument for the function
#or can use lambda within the bind function
def add_to_list(event=None):
    text = entry.get()
    if text:
        text_list.insert(tk.END, text)
        entry.delete(0, tk.END)
        #tk.END is a special index adding to the last place in the index

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#weights are arbitrary numbers. The sum of the weights / individual weight is the percentage of the window that is used
#e.g. two columns, weight 3 and weight 1, weight 3 will take up 75% of the resized space, weight 1 will take up the remaining 25%

#a frame is a container for other widgets
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

#frame is the parent window, entry is a text entry field
entry = ttk.Entry(frame)
entry.grid(row=0, column=0, sticky="ew")
#I want the entry box to stick but not the button, so I dont make the entire row sticky, just the box

entry.bind("<Return>", add_to_list)

entry_btn = ttk.Button(frame, text="Add to list", command=add_to_list)
entry_btn.grid(row=0, column=1)

text_list = tk.Listbox(frame)
text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
#sticky="ew" means east & west, the widget then sticks to the sides


root.mainloop()


#frame usage makes it easier to re-use widgets