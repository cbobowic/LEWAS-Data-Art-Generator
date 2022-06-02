import math
import time
from PIL import Image, ImageDraw, ImageColor
import pandas as pd
import datetime as dt

class Temperature_Circle:

# TODO: List of Potential improvements:
    # Cleaning? How does that work?
    # Randomization -- is it necessary? To what degree
    # Negative values -- are they intentional
    # Gap -- is this caused by the negative and near-zeros?
    # Color -- work in a function that gets the gradient between any two colors
    # 


    def __init__(self, data, canvas_width: int, canvas_height: int, cool_color: tuple, warm_color: tuple) -> None:
        self.data = data[(data.value < 25) & (data.value > 2)]
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
        init_radius = 5
        ImageDraw.Draw(self.img).ellipse(xy=(self.width/2-init_radius,
                                             self.height/2-init_radius,
                                             self.width/2+init_radius,
                                             self.height/2+init_radius),
                                         fill='white')

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
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-01-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='red')


        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-02-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='orange')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-03-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='yellow')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-04-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='green')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-05-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='blue')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-06-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='purple')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-07-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-08-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-09-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-10-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-11-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        # circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-12-01'), 3.66))
        # ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        
        
            
        

    def calculate_point_vals(self, row_date: pd.Timestamp, row_val: float) -> tuple:
        # need theta and radius
            # theta will result from the months + days
            # radius will result from the value (scaled)

        # calculating theta
        secondcount = row_date.second + 60*row_date.minute + 3600*row_date.hour + \
                      86400*(row_date.day-1) + 2678400*(row_date.month-1)
        max_seconds = 3.154e7
        theta = secondcount/max_seconds * 2 * math.pi

        #calculating radius
        min_radius = 0
        max_radius = self.height/2
        percentage = (row_val - self.min_val) / (self.max_val - self.min_val)
        scaled_radius = (max_radius - min_radius) * percentage + min_radius

        origin = (self.width/2,self.height/2)
        x = scaled_radius*math.cos(theta-math.pi/2)
        y = scaled_radius*math.sin(theta-math.pi/2)
        position = (origin[0] + x, origin[1] + y)
        color = self.calculate_color(percentage, self.cool_color, self.warm_color)
       
        return position + color

    def calculate_color(self, per: float, cool_color: tuple, warm_color: tuple) -> tuple:
        inverse = 1 - per
        r = int(cool_color[0] * inverse + warm_color[0] * per)
        g = int(cool_color[1] * inverse + warm_color[1] * per)
        b = int(cool_color[2] * inverse + warm_color[2] * per)
        return (r,g,b)



