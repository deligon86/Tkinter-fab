from tkinter import Label
import time


class FABHover:
    """For annimation of button text"""
    def __init__(self, widget, parent, color, anim_duration):
        self.parent = parent
        self.widget = widget # the buttons floating
        self.color = color#Colors("Icons/plus.png").extract_transform()
#print(self.color)
        self.anim_duration = anim_duration

        self.widget.bind('<Enter>', self.animate)
        self.widget.bind('<Leave>', self.stop)

    def animate(self, event):
        x,y = self.widget.winfo_x(), self.widget.winfo_y()

        xpos = x - 190
        ypos = y + 9
        
        self.lbl = Label(self.parent, text=self.widget['text'], font=("times new roman", 18), width=0, height=2, bg=self.color)
        self.lbl.place(x=xpos, y=ypos, relheight=0.05)
        for width in range(15):
            self.lbl.configure(width=width)
            self.parent.update()
            time.sleep(self.anim_duration)

    def stop(self, event):
        self.lbl.destroy()