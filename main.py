import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import math

filepath = "C:\LEWAS\michelle-colden-art-generator\testcsv.csv"

# Set the initial canvas dimensions
canvas_height = 1000
canvas_width = 1200

# csv parser
data = pd.read_csv(filepath_or_buffer='testcsv.csv', index_col='id', usecols=['id','value','datetime'])


def basicArt():
    '''This is a basic example of using data to create a visual.'''
    img = Image.new(mode='RGB', size=(canvas_width,canvas_height), color='black')
    for i in data['value']:
        draw = ImageDraw.Draw(img)
        xy = (100, 100, 800, 200 * i)
        draw.line(xy, fill='green', width=1)

    img.show()

basicArt()