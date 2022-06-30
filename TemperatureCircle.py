import time
from PIL import Image, ImageDraw
import pandas as pd
import math


class ColorCalculator:
    def calculate_color(per: float, cool_color: tuple, warm_color: tuple) -> tuple:
        """This method takes any two RGB tuples and plots a radial gradient from the cool
        color (inside) to warm color (outside).

        :param float per: the percent the color is between the cool and warm color (0-1)
        :param tuple cool_color: the (R,G,B) for the color for the inside of the circle
        :param tuple warm_color: the (R,G,B) for the color for the outside of the circle
        :return tuple: the (R,G,B) tuple of the output color
        """
        inverse = 1 - per
        r = int(cool_color[0] * inverse + warm_color[0] * per)
        g = int(cool_color[1] * inverse + warm_color[1] * per)
        b = int(cool_color[2] * inverse + warm_color[2] * per)
        return (r, g, b)


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

        self.data.apply(
            lambda row: self.plot_point(pd.to_datetime(row["datetime"]), row["value"]),
            axis=1,
        )

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
        self.min_val = self.data.min()["value"]
        self.max_val = self.data.max()["value"]

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
