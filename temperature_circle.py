import math
from sqlite3 import Timestamp
from turtle import color
from PIL import Image, ImageDraw
from pandas import DataFrame, Series
import datetime as dt

class Temperature_Circle:



    def __init__(self, data: DataFrame, canvas_width: int, canvas_height: int) -> None:
        self.data = data
        self.width = canvas_width
        self.height = canvas_height

        self.setup()
        self.plotpoint()
        # img.show()


    def setup(self):
        '''Sets up the image and starting circle'''
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')
        init_radius = 300
        ImageDraw.Draw(self.img).ellipse(xy=(self.width/2-init_radius,self.height/2-init_radius,self.width/2+init_radius,self.height/2+init_radius))

        # calculate minval and maxval of the DataFrame
        self.min_val = self.data.min()['value']
        self.max_val = self.data.max()['value']

        

    def plotpoint(self):

        for i in self.data.index:
            # ImageDraw.Draw(img).point((self.calculate_position(i)), self.calculate_color())
            
            self.calculate_position(self.data.iat[i,2], self.data.iat[i,1])

            # Test circle to see where points are plotted
            # circle_xy = (self.calculate_position(i), self.calculate_position(i)[0]+5, self.calculate_position(i)[1]+5)
            # ImageDraw.Draw(img).ellipse(circle_xy, fill='white')
            
        

    def calculate_position(self, row_date: Timestamp, row_val: float) -> tuple:
        # need theta and radius
            # theta will result from the months + days
            # radius will result from the value (scaled)

        # calculating theta
        secondcount = row_date.second + 60*row_date.minute + 3600*row_date.hour + 86400*row_date.day + 2678400*row_date.month
        max_seconds = 60*1 + 60*60 + 3600*24 + 86400*31 + 3.154e7
        theta = secondcount/max_seconds * 2 * math.pi

        #calculating radius
        min_radius = 100
        max_radius = self.height - 100
        
        val = (self.max_val - self.min_val)



        return (100,100)

    def calculate_color(self):
        pass