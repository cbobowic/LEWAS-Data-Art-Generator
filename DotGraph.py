import math
from random import random
import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, filein: str, canvas_width: int, canvas_height: int) -> None:
        self.filein = filein
        self.width = canvas_width
        self.height = canvas_height

        self.setup()

        self.plot_points()

        self.img.show()
        


    def setup(self):
        try:
            self.data = pd.read_csv(filepath_or_buffer=self.filein, 
                               usecols=['value','datetime'])
        except FileNotFoundError:
            print("Error: File Not Found!")
            quit()
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')

    def plot_points(self):
        for i in range(1, self.width, 16):
            for j in range(1, self.height, 16):
                rand = random()*12
                ImageDraw.Draw(self.img).ellipse((i, j, i+rand, j+rand), fill=(0, int(random()*255), int(random()*255)))