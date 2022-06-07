import sys
import time
import pandas as pd
import random as rnd
from PIL import Image, ImageDraw
from DotGraph import DotGraph

from TemperatureCircle import TemperatureCircle

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

def drawPoints():
    img = Image.new(mode='RGB', size=(canvas_width, canvas_height), color='black')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # DISTANCE AMONG POINTS
    step = 10
    for n in range(step, w, step):
        for x in range(step, h - step, step):
            ran = rnd.uniform(0.0, 40.0)
            a = n + ran
            b = x + ran
            if a > canvas_width:
                a = n
            if b > canvas_height:
                b = x
            draw.point((a, b), fill="yellow")
    img.show()

if __name__ == "__main__":
    starttime = time.time()

    # error checking
    if len(sys.argv) > 2:
        print("Error: Too Many Arguments")
    elif len(sys.argv) < 2:
        print("Error: Input filepath is required")
    elif not sys.argv[1].endswith('.csv'):
        print("Error: Argument filename must be of file type *.csv")
    else:
        filepath = sys.argv[1]
        # basicArt()
        # drawPoints()
        # TemperatureCircle(filepath,canvas_width,canvas_height, (0,0,255), (255,0,0))
        DotGraph(filepath,canvas_width,canvas_height)
        print("Total Time: ", time.time() - starttime)

