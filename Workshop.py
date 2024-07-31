import tkinter as tk
from tkinter import ttk
from random import randint, choice


root2 = tk.Tk()
root2.geometry("300x300")
root2.title("StartGame")
canvas = tk.Canvas(root2, bg="gray", scrollregion=(0,0,2000,5000))
canvas.create_line(0,0,2000,5000, width=10)
for i in range(100):
    l = randint(0,2000)
    t = randint(0,5000)
    r = l+randint(10,500)
    b = t+randint(10,500)
    color = choice(('red', 'green', 'blue', 'yellow'))
    canvas.create_rectangle(l,t,r,b, fill=color)
canvas.pack(expand=True, fill="both")

#mousewheel scrolling
canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(event.delta / 60), "units"))
canvas.bind('<Control MouseWheel>', lambda event: canvas.xview_scroll(int(event.delta / 60), "units"))

#scrollbar
scrollbar = ttk.Scrollbar(root2, orient = 'vertical', command = canvas.yview)
canvas.configure(yscrollcommand = scrollbar.set)
scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor= 'ne')

scrollbar2 = ttk.Scrollbar(root2, orient= 'horizontal', command = canvas.xview)
canvas.configure(xscrollcommand = scrollbar2.set)
scrollbar2.place(relx = 0, rely = 1, relwidth = 1, anchor = 'sw')



root2.mainloop()



#frame usage makes it easier to re-use widgets