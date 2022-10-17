from PIL import Image,ImageTk


class Load:
    '''class to load icons\n
    path=path to icon, size=(w,h)'''
    def __init__(self, path=None,size=(40,35)):
        self.path= path
        self.size = size

    def load_and_transform(self):
        self.image = Image.open(self.path)
        self.image = self.image.resize(self.size,Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)

        return self.tk_image