from random import randint
import time
from turtle import pos
import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, canvas_width: int, canvas_height: int) -> None:
        self.width = canvas_width
        self.height = canvas_height
        self.prev = (self.width/2,self.height/2)
        self.count = 0

        self.img = Image.new(mode="RGB", size=(self.width, self.height), color="black")

        df = self.findDifferences(data, data2)

        print("Starting apply")
        start = time.time()
        df.apply(lambda x: self.plot_point(x), axis=1)
        end = time.time()
        print('Time to apply : ' , (end - start))
        self.img.show()

 
    def findDifferences(self, data: pd.DataFrame, data2: pd.DataFrame):
        merged = pd.merge(data, data2, how='outer', on='datetime')
        
        merged['diff_x'] = merged['value_x'].diff()
        merged['diff_y'] = merged['value_y'].diff()
        df = merged.drop(columns=['value_x', 'value_y'])

        origin = (self.width/2, self.height/2)

        df['pos_x'] = origin[0] \
                         + (df['diff_x'] 
                         / ( df['diff_x'].max() - df['diff_x'].min() )
                         * self.width)

        df['pos_y'] = origin[1] \
                         + (df['diff_y']
                         / ( df['diff_y'].max() - df['diff_y'].min() )
                         * self.height)
        df = df.drop(columns=['diff_x', 'diff_y']).dropna().astype({'pos_x': 'int', 'pos_y': 'int'})

        return df


    def plot_point(self, row):
        x = row['pos_x']
        y = row['pos_y']
        # n = int(randint(0,255))
        try:
            n = ((y - self.prev[1]) / (x - self.prev[0]))
            print(n)
        except ZeroDivisionError:
            n=255
        r = 0
        g = 0
        b = 255

        # ImageDraw.Draw(self.img).point((x, y), fill='white')

        ImageDraw.Draw(self.img).line((x, y, self.prev[0], self.prev[1]), fill=(r,g,b))
        self.prev = (row['pos_x'], row['pos_y'])

        # ImageDraw.Draw(self.img).ellipse((x,y,x+1,y+1),fill=(r,g,b))



