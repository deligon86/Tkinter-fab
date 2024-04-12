from tkinter import Label, Button, Tk, PhotoImage
import time
from threading import Thread
from PIL import Image, ImageTk
from assestloader import Load
from coloring import PilDetector
from hovering import FABHover


class BButton(Button):
    """The floating buttons"""
    def __init__(self, parent, icon, x,y, text=None, command=None):
        Button.__init__(self, parent, text=text, command=command)
        self.config(image=icon, bg=parent['bg'], activebackground=parent['bg'], bd=0, highlightthickness=0)


icon_image = None


class FloatingSpeedDial(Button):
    """Button placed on root window usage\n
    icon_data = {'icon_path':'text','icon_path'}\n
    icon = "icon_path for the action button"\n
    FloatingSpeedDial(root, data=icon_data, icon=icon)\n

    """
    def __init__(self, parent:Tk, data:dict, animate=False, icon=None, icon_size=55, open_duration=0.001, anim_duration=0.01,
                    on_release=None, rotate_icon=False):
        self.parent = parent
        self.data = data
        self.animate = animate
        self.icon_size = icon_size
        self.open_duration = open_duration
        self.anim_duration = anim_duration
        self.on_release = on_release
        self.rotate_icon = rotate_icon

        # get the actual app size
        self.parent.update()
        x, y = self.parent.winfo_width() - 100, self.parent.winfo_height() - 100

        self.initial_width = self.parent.winfo_width()  # if changes the button placement will be adjusted
        self.initial_height = self.parent.winfo_height()

        Button.__init__(self, parent,  bg="grey25", activebackground="grey25", bd=0, highlightthickness=0, command=self.pack_data)
        self.place(x=x, y=y)
        self.open = False
        self.widgets = []
        self.image_icon = "" # for loading the icons

        self.plus_icon = icon
        self.icon_bg_color = PilDetector(self.plus_icon).detect_hybrid(hex=True)
        
        self.plus_icon_im = Load(self.plus_icon, (self.icon_size,self.icon_size)).load_and_transform()

        self.configure(image=self.plus_icon_im)

    def pack_data(self):
        """display the buttons"""
        if not self.open:
            x, y = self.winfo_x(), self.winfo_y() # get the position of main floating action button
            count = 0
            for key, var in self.data.items():
                count += 1
                y -= 60
                icon_image = self.process_icons(key)
                self.b = BButton(parent=self.parent, icon=icon_image, text=var, x=x, y=y, command=lambda: self.on_press(var))
                self.b.image = icon_image
                self.b.place(x=x, y=y)
                if self.animate is True:
                    pass
                else:
                    self.yt = Label(self.parent, text=var, font=("times new roman", 16), width=15, bg=self.icon_bg_color)
                    self.yt.place(x=(x-190), y=(y+8), relheight=0.05)
                    self.widgets.append(self.yt)
                self.widgets.append(self.b)
                self.parent.update()
                time.sleep(self.open_duration)
                

            self.close_icon_ = self.generate_closure_icon(self.plus_icon)
            self.configure(image=self.close_icon_)
            if self.animate:
                for wigd in self.widgets:
                    FABHover(widget=wigd, parent=self.parent, color=self.icon_bg_color, anim_duration=self.anim_duration)

            self.open = True
        else:
            #print(self.widgets)
            for widget in self.widgets:
                widget.destroy()

            self.open = False
            self.configure(image=self.plus_icon_im)
            self.widgets.clear()

    def generate_closure_icon(self, icon):
        """this rotates the plus icon 45%"""
        image = Image.open(icon)
        image = image.resize(size=(self.icon_size,self.icon_size), resample=Image.ANTIALIAS)
        if self.rotate_icon:
            image = image.rotate(45)
        return ImageTk.PhotoImage(image)

    # process icons
    def process_icons(self, icon) -> PhotoImage:
        icon_image = Load(icon, (self.icon_size,self.icon_size)).load_and_transform()
    
        return icon_image
    
    # adjust_placement method
    def adjust_placement(self):
    
        self.parent.update()
        w,h = self.parent.winfo_width(), self.parent.winfo_height()

        if w != self.initial_width:
            x,y = w - 100, h -100
            self.place(x=x, y=y)
            self.update()
            self.parent.update()
        elif h != self.initial_height:
            x,y = w - 100, h -100
            self.place(x=x, y=y)
            self.update()
            self.parent.update()
        
        elif h != self.initial_height and w != self.initial_width:
            x,y = w - 100, h -100
            self.place(x=x, y=y)
            self.update()
            self.parent.update()

        self.initial_width = w
        self.initial_height = h

    
    def adjustment_thread(self):
        Thread(target=self.adjust_placement, daemon=True).start()

    def on_press(self, instance_text):
        if self.on_release:
            # send to the outside function to process actions
            self.on_release(instance_text)


if __name__ == '__main__':
    class Example(Tk):
        def __init__(self):
            super().__init__()
            self.title("FAB")
            self.geometry("500x500")
            self.config(bg="grey15")

            data = {
                "icons/close.png": "Exit",
                "icons/cog.png": "Settings",
                "icons/bell-ring.png": "Notifications",
                "icons/account.png": "Account"
            }
            self.fab = FloatingSpeedDial(parent=self, data=data, animate=True, icon="plus.png")

    
    Example().mainloop()