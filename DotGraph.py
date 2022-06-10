import math
from random import random
import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, filein: str, canvas_width: int, canvas_height: int, step: int) -> None:
        self.filein = filein
        self.width = canvas_width
        self.height = canvas_height
        self.step = step

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
        self.count = int(self.width * self.height)/(math.pow(self.step,2))
        self.data.resample()
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')

    def plot_points(self):
        count = 0
        for i in range(1, self.width, self.step):
            for j in range(1, self.height, self.step):
                rand = random()*self.step/2
                xy_rgb = self.calculate_values()
                ImageDraw.Draw(self.img).ellipse((i, j, i+rand, j+rand), fill='white')
    
    def calculate_values(self, val: float):
        pass