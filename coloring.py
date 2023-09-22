import random
from PIL import Image
from matplotlib.colors import rgb2hex


def convert_to_hex(color:list):

    return rgb2hex(c=color)



class PilDetector:
    """detect backgound of image using pillow and algorithm I implemented"""
    def __init__(self, path):
        self.image_path = path
        self.rgb_color = None
        self.hex_color = None

        try:
            self.image = Image.open(self.image_path)
        except Exception as e:
            print("[+] could not load image due to: ", str(e))

    def detect_max(self, hex=False):
        count, color = max(self.image.getcolors(self.image.size[0]*self.image.size[1]))
        color = list(color)
        n, color = color
        color = self.__transform_color(color, hex)

    def detect_least(self, hex=False):
        colors = sorted(self.image.getcolors(self.image.size[0]*self.image.size[1]))
        color_ = min(colors)
        count, color = color_
        color = self.__transform_color(color, hex)

        return color

    def detect_hybrid(self, threshold=2, hex=False):
        """I use this for my music player applications for determining bg color and text color 
        to use from the album art by adjisting the threshold"""
        colors = sorted(self.image.getcolors(self.image.size[0]*self.image.size[1]))
        color = self._find_color(colors=colors, tr=threshold)
        color = self.__transform_color(color, hex)

        return color
    
    def _find_color(self, colors, tr=2):
        items = len(colors)
        if tr % 2 == 0:
            factor = items // tr
            first_half = colors[:factor]
            sec_half = colors[factor:]
            color = random.choice([first_half[-1], sec_half[0]])
            count, color = color
        elif tr % 3 == 0:
            factor = items // tr
            count, color = colors[factor]

        return color

    def __transform_color(self, color, hex=False):
        """ The default color is rgb change hex to True to transform to hex value """
        if isinstance(color, tuple):
            color = list(color)
        if len(color) > 3:
            color.pop(3)
            # color.append(1)
        
        if hex:
            color.pop(2)
            color = [c/255 for c in color]
            color.append(1)
            color = convert_to_hex(color)

        return color

