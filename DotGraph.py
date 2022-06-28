import math
from random import random
from re import L
import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, canvas_width: int, canvas_height: int) -> None:
        self.data = data
        self.data2 = data2
        self.width = canvas_width
        self.height = canvas_height

        self.img = Image.new(mode="RGB", size=(self.width, self.height), color="black")

        self.merged = pd.merge(self.data, self.data2, how='outer', on='datetime')
        
        self.min_x_val = self.merged['value_x'].min()
        self.max_x_val = self.merged['value_x'].max()
        self.min_y_val = self.merged['value_y'].min()
        self.max_y_val = self.merged['value_y'].max()
        # print(self.min_x_val, self.max_y_val)
        print(self.merged.head())

        # self.merged.apply(lambda row: self.plot_point(row), axis=1)