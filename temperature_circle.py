from turtle import color
from PIL import Image, ImageDraw
import pandas as pd
from pandas import DataFrame, Series

class Temperature_Circle:



    def __init__(self, data: DataFrame, canvas_width: int, canvas_height: int) -> None:
        self.data = data
        self.width = canvas_width
        self.height = canvas_height
        self.setup()
        self.plotpoint()
        img.show()


    def setup(self):
        '''Sets up the image and starting circle'''
        global img
        img = Image.new(mode='RGB', size=(self.width,self.height), color='black')
        radius = 300
        ImageDraw.Draw(img).ellipse(xy=(self.width/2-radius,self.height/2-radius,self.width/2+radius,self.height/2+radius))
    
    def plotpoint(self):

        for i in self.data.iterrows():
            # ImageDraw.Draw(img).point((self.calculate_position(i)), self.calculate_color())

            # Test circle to see where points are plotted
            circle_xy = (self.calculate_position(i), self.calculate_position(i)[0]+5, self.calculate_position(i)[1]+5)
            ImageDraw.Draw(img).ellipse(circle_xy, fill='white')
            
        

    def calculate_position(self, row: Series) -> tuple:
        # radians = 

        return (100,100)

    def calculate_color(self):
        pass