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
        self.data = data[(data.value < 25)]
        self.width = canvas_width
        self.height = canvas_height
        self.cool_color = cool_color
        self.warm_color = warm_color

        self.setup()
        beginplot = time.time()
        self.plotpoint()
        endplot = time.time()
        print('PLOTPOINT: ', endplot - beginplot)
        # self.img.show()


    def setup(self):
        '''Sets up the image and centerpoint and calculates the min and max value of the data'''
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')
        init_radius = 5
        ImageDraw.Draw(self.img).ellipse(xy=(self.width/2-init_radius,
                                             self.height*2/5-init_radius,
                                             self.width/2+init_radius,
                                             self.height*2/5+init_radius),
                                         fill='white')
        # calculate minval and maxval of the DataFrame
        self.min_val = self.data.min()['value']
        self.max_val = self.data.max()['value']


    def plotpoint(self):
        '''This method iteratively loops through the DataFrame and plots each 
        point on the image.'''
        # for i, row in self.data.iterrows():
        #     ts = pd.to_datetime(row.datetime)
        #     xy = (self.calculate_point_vals(ts, row.value)[0], 
        #           self.calculate_point_vals(ts, row.value)[1])
        #     rgb = (self.calculate_point_vals(ts, row.value)[2], 
        #            self.calculate_point_vals(ts, row.value)[3], 
        #            self.calculate_point_vals(ts, row.value)[4])
        #     ImageDraw.Draw(self.img).point(xy, fill=rgb)

        


        '''
        # Test circle to see where points are plotted
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-01-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='red')

        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-02-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='orange')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-03-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='yellow')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-04-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='green')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-05-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='blue')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-06-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='purple')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-07-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-08-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-09-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-10-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-11-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        circle_xy = (self.calculate_point_vals(pd.Timestamp('2017-12-01'), 3.66))
        ImageDraw.Draw(self.img).ellipse((circle_xy[0],circle_xy[1],circle_xy[0]+5,circle_xy[1]+5), fill='white')
        '''

    def plot_point_apply():


    def calculate_point_vals(self, row_date: pd.Timestamp, row_val: float) -> tuple:
        '''This method calculates the position and color values of a data point given
        a timestamp and a value.
        :param pd.Timestamp  row_date: the timestamp associated with a given data point.
        :param float row_val: the scalar value associated with the given data point.
        :return tuple: A tuple in the format (x,y,r,g,b)'''

        # calculating theta based off of seconds into the year
        secondcount = row_date.second + 60*row_date.minute + 3600*row_date.hour + \
                      86400*(row_date.day-1) + 2678400*(row_date.month-1)
        max_seconds = 3.154e7
        theta = secondcount/max_seconds * 2 * math.pi

        #calculating radius based off of value col
        min_radius = 0
        max_radius = self.height/2
        percentage = (row_val - self.min_val) / (self.max_val - self.min_val)
        scaled_radius = (max_radius - min_radius) * percentage + min_radius

        origin = (self.width/2,self.height*2/5)
        x = scaled_radius*math.cos(theta-math.pi/2)
        y = scaled_radius*math.sin(theta-math.pi/2)
        position = (origin[0] + x, origin[1] + y)
        color = self.calculate_color(percentage, self.cool_color, self.warm_color)
       
        return position + color

    def calculate_color(self, per: float, cool_color: tuple, warm_color: tuple) -> tuple:
        '''This method takes any two RGB tuples and plots a radial gradient from the cool
        color (inside) to warm color (outside).
        :param float per: the percent the color is between the cool and warm color (0-1)
        :param tuple cool_color: the (R,G,B) for the color for the inside of the circle
        :param tuple warm_color: the (R,G,B) for the color for the outside of the circle
        '''
        inverse = 1 - per
        r = int(cool_color[0] * inverse + warm_color[0] * per)
        g = int(cool_color[1] * inverse + warm_color[1] * per)
        b = int(cool_color[2] * inverse + warm_color[2] * per)
        return (r,g,b)



