import pandas as pd
from PIL import Image, ImageDraw
from TemperatureCircle import ColorCalculator as cc


class DataBars:
    def __init__(
        self,
        canvas_width: int,
        canvas_height: int,
        numBars: int,
        data1: pd.DataFrame,
        ccolor1: tuple,
        wcolor1: tuple,
        data2=None,
        ccolor2=None,
        wcolor2=None,
        data3=None,
        ccolor3=None,
        wcolor3=None,
        savePath=None
    ) -> None:
        self.width = canvas_width
        self.height = canvas_height
        self.numBars = numBars
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.ccolor1 = ccolor1
        self.wcolor1 = wcolor1
        self.ccolor2 = ccolor2
        self.wcolor2 = wcolor2
        self.ccolor3 = ccolor3
        self.wcolor3 = wcolor3

        self.img = Image.new(mode="RGB", size=(self.width, self.height), color="black")

        self.firstBar()
        if ( self.numBars >= 2 ):
            self.secondBar()
            if ( self.numBars == 3 ):
                self.thirdBar()

        self.img.show()
        
        if ( savePath != None ):
            try:
                self.img.save(savePath)
            except FileNotFoundError:
                print('\nERROR: No such file or directory. Image failed to save.\n')


    def firstBar(self):

        self.data1 = self.data1.dropna()

        self.min_val = self.data1.min()["value"]
        self.max_val = self.data1.max()["value"]
        self.min_date = pd.Timestamp(self.data1.min()["datetime"])
        self.max_date = pd.Timestamp(self.data1.max()["datetime"])
        self.date_diff = self.max_date - self.min_date

        if self.numBars == 1:
            x1 = self.width / 4
            x2 = 3 / 4 * self.width
        elif self.numBars == 2:
            x1 = self.width / 7
            x2 = self.width * 3 / 7
        elif self.numBars == 3:
            x1 = self.width / 10
            x2 = self.width * 3 / 10

        self.data1.apply(
            lambda row: self.plot_lines(
                pd.to_datetime(row["datetime"]),
                row["value"],
                x1,
                x2,
                self.ccolor1,
                self.wcolor1,
            ),
            axis=1,
        )

    def secondBar(self):

        self.data2 = self.data2.dropna()

        self.min_val = self.data2.min()["value"]
        self.max_val = self.data2.max()["value"]
        self.min_date = pd.Timestamp(self.data2.min()["datetime"])
        self.max_date = pd.Timestamp(self.data2.max()["datetime"])
        self.date_diff = self.max_date - self.min_date

        if self.numBars == 2:
            x1 = self.width * 4 / 7
            x2 = self.width * 6 / 7
        elif self.numBars == 3:
            x1 = self.width * 4 / 10
            x2 = self.width * 6 / 10

        self.data2.apply(
            lambda row: self.plot_lines(
                pd.to_datetime(row["datetime"]),
                row["value"],
                x1,
                x2,
                self.ccolor2,
                self.wcolor2,
            ),
            axis=1,
        )

    def thirdBar(self):

        self.data3 = self.data3.dropna()

        self.min_val = self.data3.min()["value"]
        self.max_val = self.data3.max()["value"]
        self.min_date = pd.Timestamp(self.data3.min()["datetime"])
        self.max_date = pd.Timestamp(self.data3.max()["datetime"])
        self.date_diff = self.max_date - self.min_date

        x1 = self.width * 7 / 10
        x2 = self.width * 9 / 10
        self.data3.apply(
            lambda row: self.plot_lines(
                pd.to_datetime(row["datetime"]),
                row["value"],
                x1,
                x2,
                self.ccolor3,
                self.wcolor3,
            ),
            axis=1,
        )

    def plot_lines(
        self,
        datetime: pd.Timestamp,
        value: float,
        x1: int,
        x2: int,
        cool_color: tuple,
        warm_color: tuple,
    ):

        percent_date = (
            datetime - self.min_date
        ).total_seconds() / self.date_diff.total_seconds()

        percent_val = (value - self.min_val) / (self.max_val - self.min_val)

        # Calculating y val
        y1 = 1 / 6 * self.height + percent_date * self.height * 4 / 6
        y2 = y1

        color = cc.calculate_color(percent_val, cool_color, warm_color)
        ImageDraw.Draw(self.img).line((x1, y1, x2, y2), fill=color)
