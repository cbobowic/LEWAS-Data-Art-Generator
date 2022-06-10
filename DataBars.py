import pandas as pd
from PIL import Image, ImageDraw
from TemperatureCircle import ColorCalculator as cc

class DataBars:

    def __init__(self, filepath: str, canvas_width: int, canvas_height: int) -> None:
        self.width = canvas_width
        self.height = canvas_height
        self.filepath = filepath
        self.setup()

        self.data.apply(lambda row: self.plot_lines(pd.to_datetime(row['datetime']), row['value']), axis=1)

        self.img.show()
    

    def setup(self):
        try:
            self.data = pd.read_csv(self.filepath, usecols=['value','datetime'])
        except FileNotFoundError:
            print("Error: File Not Found!")
            quit()
        self.data = self.data.dropna()

        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')
        self.min_val = self.data.min()['value']
        self.max_val = self.data.max()['value']
        self.min_date = pd.Timestamp(self.data.min()['datetime'])
        self.max_date = pd.Timestamp(self.data.max()['datetime'])
        self.date_diff = self.max_date - self.min_date
        # print(self.min_date, " ", self.max_date)
        # print(self.date_diff)
        print(self.date_diff)


    def plot_lines(self, datetime: pd.Timestamp, value: float):
        x1= self.width/4
        x2= self.width*3/4

        # Calculating y val

        percent_date = (datetime - self.min_date).total_seconds() / self.date_diff.total_seconds()
        y1 = 1/6*self.height + percent_date*self.height*4/6
        y2 = y1

        percent_val = (value-self.min_val)/(self.max_val-self.min_val)

        color = cc.calculate_color(self, percent_val, (0,0,255), (255,0,0))
        ImageDraw.Draw(self.img).line((x1,y1,x2,y2),fill=color)


