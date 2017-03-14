from tkinter import *

class Dialog():
    
    
    def __init__(self, parent, message):
        
        top = self.top = Toplevel(parent)

        Label(top, text=message).pack()


        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        
        
    def ok(self):

        self.top.destroy()
