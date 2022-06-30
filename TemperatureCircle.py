import ast
from re import M
import time
from PIL import Image, ImageDraw
import pandas as pd
import math
import numpy as np
from ColorCalculator import ColorCalculator as cc

pd.options.mode.chained_assignment = None  # default='warn'


class TemperatureCircle:
    def __init__(
        self,
        data: pd.DataFrame,
        canvas_width: int,
        canvas_height: int,
        cool_color: tuple,
        warm_color: tuple,
        savePath: str,
    ) -> None:
        self.data = data
        self.width = canvas_width
        self.height = canvas_height
        self.cool_color = cool_color
        self.warm_color = warm_color
        self.setup()

        self.img.show()

        if ( savePath != None ):
            try:
                self.img.save(savePath)
            except FileNotFoundError:
                print('\nERROR: No such file or directory. Image failed to save.\n')

    def setup(self):
        """Sets up the image and centerpoint and calculates the min and max value of the data"""

        self.img = Image.new(mode="RGB", size=(self.width, self.height), color="black")
        init_radius = 5
        ImageDraw.Draw(self.img).ellipse(
            xy=(
                self.width / 2 - init_radius,
                self.height * 2 / 5 - init_radius,
                self.width / 2 + init_radius,
                self.height * 2 / 5 + init_radius,
            ),
            fill="white",
        )

        self.data = self.data[(self.data["value"] < 25)]  # Data cleaning
        # calculate minval and maxval of the DataFrame
        min_val = self.data.min()["value"]
        max_val = self.data.max()["value"]

        df = self.data

        df['datetime'] = pd.to_datetime(df["datetime"])

        df['secondcount'] = df['datetime'].dt.second \
                     + 60 * df['datetime'].dt.minute \
                   + 3600 * df['datetime'].dt.hour \
                 + 86400 * (df['datetime'].dt.day - 1) \
               + 2678400 * (df['datetime'].dt.month - 1)
        max_seconds = 3.154e7


        # quit()

        df['theta'] = df['secondcount'] / max_seconds * 2 * math.pi
        # print(df.head())
        # quit()
       # calculating radius based off of value col
        min_radius = 0
        max_radius = self.height / 2

        df['percent'] = (df['value'] - min_val) / (max_val - min_val)


        df['radius'] = (max_radius - min_radius) * df['percent'] + min_radius
        
        origin = (self.width / 2, self.height * 2 / 5)

        # print(df['percent'].head())
        # quit()
        df['pos_x'] = (origin[0] + df['radius'] * np.cos(df['theta'] - math.pi / 2)).astype('int')
        df['pos_y'] = (origin[1] + df['radius'] * np.sin(df['theta'] - math.pi / 2)).astype('int')
        # ColorCalculator.calculate_color(df, df['percent'], self.cool_color, self.warm_color)
        df = df.drop(columns=['value','radius','theta','secondcount','datetime'])
        print(df)

        df.apply(lambda x: 
        ImageDraw.Draw(self.img).ellipse((x[1]-1,x[2]-1, x[1]+1,x[2]+1),
        fill=(cc.calculate_color(x[0], self.cool_color, self.warm_color))),
        # print(x[0],x[1],x[2],x[3],x[4])
        axis=1
        )

    def plot_point(self, datetime: pd.Timestamp, value: float):
        """Calls calculate_point_vals to plot the pixel representing each data point.

        :param pd.Timestamp datetime: the timestamp of the datapoint
        :param float value: the value of the given datapoint
        """
        xyrgb_tuple = self.calculate_point_vals(datetime, value)

        # For less sparse data, use this to draw singular pixels
        # ImageDraw.Draw(self.img).point(
        #     (xyrgb_tuple[0], xyrgb_tuple[1]),
        #     fill=(xyrgb_tuple[2], xyrgb_tuple[3], xyrgb_tuple[4]),
        # )

        # For more sparse data, use this to draw small circles instead of pixels
        ImageDraw.Draw(self.img).ellipse((xyrgb_tuple[0]-1, xyrgb_tuple[1]-1, \
                                          xyrgb_tuple[0]+1, xyrgb_tuple[1]+1), \
                                         fill=(xyrgb_tuple[2], xyrgb_tuple[3], xyrgb_tuple[4]))


    def calculate_point_vals(self, row_date: pd.Timestamp, row_val: float) -> tuple:
        """This method calculates the position and color values of a data point given
        a timestamp and a value.

        :param pd.Timestamp  row_date: the timestamp associated with a given data point.
        :param float row_val: the scalar value associated with the given data point.
        :return tuple: A tuple in the format (x,y,r,g,b)
        """
        # calculating theta based off of seconds into the year
        secondcount = (
            row_date.second
            + 60 * row_date.minute
            + 3600 * row_date.hour
            + 86400 * (row_date.day - 1)
            + 2678400 * (row_date.month - 1)
        )
        max_seconds = 3.154e7
        theta = secondcount / max_seconds * 2 * math.pi

        # calculating radius based off of value col
        min_radius = 0
        max_radius = self.height / 2
        percentage = (row_val - self.min_val) / (self.max_val - self.min_val)
        scaled_radius = (max_radius - min_radius) * percentage + min_radius

        origin = (self.width / 2, self.height * 2 / 5)
        x = scaled_radius * math.cos(theta - math.pi / 2)
        y = scaled_radius * math.sin(theta - math.pi / 2)

        position = (origin[0] + x, origin[1] + y)
        color = ColorCalculator.calculate_color(
            percentage, self.cool_color, self.warm_color
        )


        return position + color
