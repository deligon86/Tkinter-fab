import random
from PIL import Image
from matplotlib.colors import rgb2hex


def convert_to_hex(color:list):

    return rgb2hex(c=color)

"""
class BackgroundDetector:

    def __init__(self, path):
        self.img = cv2.imread(path, 1)
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w * self.h

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_count(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample

        print("Average for top ten RGB", average_red, average_green, average_blue)

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        '''for rgb, value in self.number_counter:
            print(rgb, value, ((float(value)/self.total_pixels))*100)'''

    def detect(self):
        self.twenty_most_common()
        ''' self.percentage_of_first = (
            float(self.number_counter[0][1]) / self.total_pixels
        )
        print(self.percentage_of_first)
        if self.percentage_of_first > 0.5:
            print("Background color", self.number_counter[0][0])
            return self.number_counter[0][0]
        else:
            self.average_count()'''

        return self.number_counter[0][0]
"""


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

