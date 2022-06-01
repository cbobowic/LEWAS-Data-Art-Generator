import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import random

filepath = "C:\LEWAS\michelle-colden-art-generator\testcsv.csv"
canvas_height = 1000
canvas_width = 1200

data = pd.read_csv(filepath_or_buffer='testcsv.csv', index_col='id', usecols=['id','value','datetime'])
print(data)

# print(data['value'].iloc(1))


def basicArt():
    img = Image.new(mode='RGB', size=(canvas_width,canvas_height), color='black')
    for i in data:
        print(data.iloc(i))
        # draw = ImageDraw.Draw(img)
        # draw.ellipse((50,50,50), random.random*10, random.random*10)

    # img.show()

# basicArt()
