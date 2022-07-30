import math
import pandas as pd
from PIL import Image, ImageDraw
from ColorCalculator import ColorCalculator as cc

class LineGraph:
    def __init__(
        self,
        data: pd.DataFrame,
        data2: pd.DataFrame,
        canvas_width: int,
        canvas_height: int,
        cool_color: tuple,
        warm_color: tuple,
        savePath: str
    ) -> None:
        self.width = canvas_width
        self.height = canvas_height
        self.cool_color = cool_color
        self.warm_color = warm_color
        self.prev = (self.width / 2, self.height / 2)

        self.img = Image.new(mode="RGB", size=(self.width, self.height), color="black")
        df = self.findDifferences(data, data2)

        df.apply(lambda x: self.plot_point(x), axis=1)

        self.img.show()

        if ( savePath != None ):
            try:
                self.img.save(savePath)
            except FileNotFoundError:
                print('\nERROR: No such file or directory. Image failed to save.\n')


    def findDifferences(self, data: pd.DataFrame, data2: pd.DataFrame):
        
        df = pd.merge(data, data2, how="outer", on="datetime")
        df["diff_x"] = df["value_x"].diff()
        df["diff_y"] = df["value_y"].diff()
        df = df.drop(columns=["value_x", "value_y"])

        origin = (self.width / 2, self.height / 2)

        df["pos_x"] = origin[0] + (
            df["diff_x"] / (df["diff_x"].max() - df["diff_x"].min()) * (self.width - 500)
        )
        df["pos_y"] = origin[1] - (
            df["diff_y"] / (df["diff_y"].max() - df["diff_y"].min()) * (self.height - 500)
        )

        # Dropping cols and casting vals to ints
        df = (
            df.drop(columns=["diff_x", "diff_y"])
            .dropna()
            .astype({"pos_x": "int", "pos_y": "int"})
        )

        return df

    def plot_point(self, row):
        x = row["pos_x"]
        y = row["pos_y"]

        ImageDraw.Draw(self.img).line(
            (x, y, self.prev[0], self.prev[1]), fill=self.lineColor(x, y), width=2)

        self.prev = (row["pos_x"], row["pos_y"])


    def lineColor(self, x: int, y: int):

        try:
            slope = (y - self.prev[1]) / (x - self.prev[0])
            percent = (math.degrees(math.atan(slope))) / 90
        except ZeroDivisionError:
            percent = 1

        if percent > 0:
            return cc.calculate_color(percent, (255, 255, 255), self.cool_color)
        else:
            percent = abs(percent)
            return cc.calculate_color(percent, (255, 255, 255), self.warm_color)
