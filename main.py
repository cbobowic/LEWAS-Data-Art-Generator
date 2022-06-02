from argparse import ArgumentError, ArgumentTypeError
import sys
from time import time
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import datetime as dt

from temperature_circle import Temperature_Circle

# Set the initial canvas dimensions
canvas_width = 1200
canvas_height = 1000

def basicArt():
    '''This is a basic example of using data to create a visual.'''
    img = Image.new(mode='RGB', size=(canvas_width,canvas_height), color='black')
    for i in data['value']:
        draw = ImageDraw.Draw(img)
        xy = (100, 100, 800, 200 * i)
        draw.line(xy, fill='green', width=1)

    img.show()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise ArgumentError("Error: Too Many Arguments")
    elif len(sys.argv) < 2:
        raise ArgumentError("Error: Input File Required")
    elif not sys.argv[1].endswith('.csv'):
        raise ArgumentTypeError("Error: Argument filename must be of file type *.csv")
    else:
        filepath = sys.argv[1]
        # csv parser
        data = pd.read_csv(filepath_or_buffer=filepath, index_col='id', usecols=['id','value','datetime'])
        # basicArt()
        data['datetime'] = pd.to_datetime(data.datetime)
        
        # print(data.datetime.dt.month)
        # print('working')


        Temperature_Circle(data,canvas_width,canvas_height)
