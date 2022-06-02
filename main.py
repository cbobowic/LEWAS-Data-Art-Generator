from argparse import ArgumentError, ArgumentTypeError
import sys
import time
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import datetime as dt

from temperature_circle import Temperature_Circle

# Set the initial canvas dimensions
canvas_width = 2000
canvas_height = 1500

def basicArt():
    '''This is a basic example of using data to create a visual.'''
    img = Image.new(mode='RGB', size=(canvas_width,canvas_height), color='black')
    draw = ImageDraw.Draw(img)
    for i in data['value']:
        xy = (100, 100, 800, 200 * i)
        draw.line(xy, fill='green', width=1)

    img.show()


if __name__ == "__main__":
    starttime = time.time()
    # error checking
    if len(sys.argv) > 2:
        print("Error: Too Many Arguments")
    elif len(sys.argv) < 2:
        print("Error: Input File Required")
    elif not sys.argv[1].endswith('.csv'):
        print("Error: Argument filename must be of file type *.csv")
    else:
        filepath = sys.argv[1]
        # csv parser
        csvparse = time.time()
        try:
            data = pd.read_csv(filepath_or_buffer=filepath, 
                               usecols=['id','value','datetime'], 
                               parse_dates=['datetime'])
        except FileNotFoundError:
            print("Error: File Not Found!")
        else:
            # basicArt()
            print("CSV Parse Time: ", time.time()-csvparse)
            Temperature_Circle(data,canvas_width,canvas_height, (0,0,255), (255,0,0))
            print("Total Time: ", time.time() - starttime)

