import tkinter as tk
from tkinter import ttk


class Window(tk.Tk):
    def __init__(self, title, size):
        
        #main set up
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        
        #frames and widgets
        self.text_window = Text_frame(self)
        
        
        self.mainloop()
        
class Text_frame(ttk.Frame):
    def __init__(self, parent, output=None):
        super().__init__(parent)
        output = ttk.Label(self, background='black', text=self.update_text).pack(expand=True, fill='both')
        self.output = output
        self.place(x = 0, y = 0, relwidth = 1, relheight = 0.8)
    
    @classmethod    
    def update_text(self, input):
        self.output.configure(text="potato wedges")
        self.update()
        self.update_idletasks()
        
    def create_widgets(self):
        pass
    
    def create_layout(self):
        pass

# class Text_label(Text_frame):
#     def __init__(self, output=None):
#         self.output = output
        

# Text_frame.update_text("potatoes")


Window("Class based Tkinter", (800,600))