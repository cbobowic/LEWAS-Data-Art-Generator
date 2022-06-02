import math
from sqlite3 import Timestamp
import time
from turtle import color
from PIL import Image, ImageDraw
from pandas import DataFrame, Series
import datetime as dt
import matplotlib

class Temperature_Circle:

# TODO: List of Potential improvements:
    # Cleaning? How does that work?
    # Randomization -- is it necessary? To what degree
    # Negative values -- are they intentional
    # Gap -- is this caused by the negative and near-zeros?
    # Color -- work in a function that gets the gradient between any two colors
    # 


    def __init__(self, data: DataFrame, canvas_width: int, canvas_height: int, cool_color: color, warm_color: color) -> None:
        self.data = data[data.value < 25]
        self.width = canvas_width
        self.height = canvas_height
        self.cool_color = cool_color
        self.warm_color = warm_color

        self.setup()
        self.plotpoint()
        self.img.show()


    def setup(self):
        '''Sets up the image and starting circle'''
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')
        init_radius = self.height/4
        ImageDraw.Draw(self.img).ellipse(xy=(self.width/2-init_radius,
                                             self.height/2-init_radius,
                                             self.width/2+init_radius,
                                             self.height/2+init_radius))

        # calculate minval and maxval of the DataFrame
        self.min_val = self.data.min()['value']
        self.max_val = self.data.max()['value']

        

    def plotpoint(self):
        for i, row in self.data.iterrows():
            xy = (self.calculate_point_vals(row.datetime, row.value)[0], 
                  self.calculate_point_vals(row.datetime, row.value)[1])
            rgb = (self.calculate_point_vals(row.datetime, row.value)[2], 
                   self.calculate_point_vals(row.datetime, row.value)[3], 
                   self.calculate_point_vals(row.datetime, row.value)[4])
            ImageDraw.Draw(self.img).point(xy, fill=rgb)


            # # Test circle to see where points are plotted
            # circle_xy = (xy, xy[0]+5, xy[1]+5)
            # ImageDraw.Draw(self.img).ellipse(circle_xy, fill='white')
            
        

    def calculate_point_vals(self, row_date: Timestamp, row_val: float) -> tuple:
        # need theta and radius
            # theta will result from the months + days
            # radius will result from the value (scaled)

        # calculating theta
        secondcount = row_date.second + 60*row_date.minute + 3600*row_date.hour + 86400*row_date.day + 2678400*row_date.month
        max_seconds = 60*1 + 60*60 + 3600*24 + 86400*31 + 3.154e7
        theta = secondcount/max_seconds * 2 * math.pi

        #calculating radius
        min_radius = 0
        max_radius = self.height/2
        percentage = (row_val - self.min_val) / (self.max_val - self.min_val)
        scaled_radius = (max_radius - min_radius) * percentage + min_radius

        origin = (self.width/2,self.height/2)
        # x = r*cos(theta)
        # y = r*sin(theta)
        position = (origin[0] + scaled_radius*math.cos(theta), origin[1] + scaled_radius*math.sin(theta))
        color = self.calculate_color(percentage, self.cool_color, self.warm_color)
       
        return position + color

    def calculate_color(self, per: float, cool_color: color, warm_color: color) -> tuple:
        # r = int(255*per)
        # g = 0
        # b = int(255-255*per)

        matplotlib.colors.to_rgb()

        inverse = 1 - per
        print(cool_color[0])
        # r = int(cool_color[0] * inverse + warm_color[0] * per)
        # g = int(cool_color[1] * inverse + warm_color[1] * per)
        # b = int(cool_color[2] * inverse + warm_color[2] * per)
        # return (r,g,b)
        return (255,0,0)



