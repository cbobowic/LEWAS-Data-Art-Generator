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
        self.width = canvas_width
        self.height = canvas_height
        self.cool_color = cool_color
        self.warm_color = warm_color

        self.setup()

        df = self.calculate_values(data)
        df.apply(lambda row: 
        ImageDraw.Draw(self.img).ellipse((row['pos_x']-1,row['pos_y']-1, 
                                          row['pos_x']+1,row['pos_y']+1),
        fill=(cc.calculate_color(row['percent'], self.cool_color, self.warm_color))),
        axis=1
        )

        self.img.show()

        if ( savePath != None ):
            try:
                self.img.save(savePath)
            except FileNotFoundError:
                print('\nERROR: No such file or directory. Image failed to save.\n')

    def setup(self):
        """Sets up the image and centerpoint"""
        # Chicago Maroon : (100,47,64)
        # Burnt Orange : (194,74,43)
        self.img = Image.new(mode="RGB", size=(self.width, self.height), color=(194,74,43))
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

    def calculate_values(self, df: pd.DataFrame):
        df = df[(df["value"] < 25)]  # Data cleaning
        min_val = df.min()["value"]
        max_val = df.max()["value"]

        df['datetime'] = pd.to_datetime(df["datetime"])
        df['secondcount'] = df['datetime'].dt.second \
                     + 60 * df['datetime'].dt.minute \
                   + 3600 * df['datetime'].dt.hour \
                 + 86400 * (df['datetime'].dt.day - 1) \
               + 2678400 * (df['datetime'].dt.month - 1)
        max_seconds = 3.154e7

        df['theta'] = df['secondcount'] / max_seconds * 2 * math.pi

        min_radius = 0
        max_radius = self.height / 2
        origin = (self.width / 2, self.height * 2 / 5)

        df['percent'] = (df['value'] - min_val) / (max_val - min_val)
        df['radius'] = (max_radius - min_radius) * df['percent'] + min_radius
        df['pos_x'] = (origin[0] + df['radius'] * np.cos(df['theta'] - math.pi / 2)).astype('int')
        df['pos_y'] = (origin[1] + df['radius'] * np.sin(df['theta'] - math.pi / 2)).astype('int')

        return df.drop(columns=['value','radius','theta','secondcount','datetime'])


