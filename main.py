import re
import sys
import time
from tkinter import N
from turtle import st
import pandas as pd
import random as rnd
from PIL import Image, ImageDraw
from DataBars import DataBars
from DotGraph import DotGraph

from TemperatureCircle import TemperatureCircle

# Set the initial canvas dimensions
canvas_width = 2000
canvas_height = 1500
rgb_regex = "^\((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))\)$"


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


# if __name__ == "__main__":
#     starttime = time.time()

#     # error checking
#     if len(sys.argv) > 4:
#         print("Error: Too Many Arguments")
#     elif len(sys.argv) < 2:
#         print("Error: Input filepath is required")
#     elif not sys.argv[1].endswith('.csv'):
#         print("Error: Argument filename must be of file type *.csv")
#     else:
#         filepath = sys.argv[1]
#         filepath2 = None
#         filepath3 = None
#         if ( len(sys.argv) == 3 or len(sys.argv) == 4 ): 
#             filepath2 = sys.argv[2]
#         if ( len(sys.argv) == 4 ): filepath3 = sys.argv[3]
#         # basicArt()
#         # drawPoints()
#         # TemperatureCircle(filepath,canvas_width,canvas_height, (0,0,255), (255,0,0))
#         # DotGraph(filepath,canvas_width,canvas_height,step=10)

#         DataBars(canvas_width, canvas_height, filepath, filepath2, filepath3)
        
#         print("Total Time: ", time.time() - starttime)


def help():
    print('ART GENERATOR USAGE:')
    print('--help               print this usage information')
    print('--TemperatureCircle  create a radial color circle')
    print('--DotGraph           create an graph of points representing data values')
    print('--DataBars           create 1, 2, or 3 bars representing data values')

def inputColor(prompt: str) -> tuple:
    while True:
        colorIn = input(prompt)
        if colorIn == 'q':
            quit()
        colorIn = colorIn.replace(' ','')
        if re.search(rgb_regex,colorIn):
            colorIn = colorIn[1:-1]
            rgbIn = colorIn.split(',')
            return (int(rgbIn[0]),int(rgbIn[1]),int(rgbIn[2]))
        else:
            print("ERROR: Invalid RGB Tuple")
            print("Please enter a tuple in the form ([0-255], [0-255], [0-255])")

def inputFile(prompt: str):
    while True:
        fileIn = input(prompt)
        if fileIn == 'q':
            quit()
        elif not fileIn.endswith('.csv'):
            print('ERROR: File must be of type *.csv!\n')
            continue
        try:
            data = pd.read_csv(fileIn, usecols=['value','datetime'])
        except FileNotFoundError:
            print("ERROR: File Not Found!\n")
            continue
        return data

def saveLoop():
    while True:
        saveIn = input('\nSave Image? [y/n] : ')
        if ( saveIn == 'q' ):
            quit()
        if ( saveIn == 'y' or saveIn == 'Y' or saveIn == 'yes' or saveIn == 'Yes' ):
            filepath = input("Enter File Path : ")
            if not ( filepath.endswith('.jpg') or filepath.endswith('.png') ):
                print("ERROR: File must be of type *.jpg or *.png!\n")
                continue
            else:
                return filepath
        elif ( saveIn == 'n' or saveIn == 'N' or saveIn == 'no' or saveIn == 'No' ):
            return None
        else:
            print("ERROR: Please enter yes (y) or no (n)")

def temperature_circle():
    while True:
        data = inputFile('\nPlease Enter CSV Filepath : ')
        print('\nPlease Enter Cool Color')
        coolColor = inputColor('Cool Color RGB Tuple : ')
        print('\nPlease Enter Warm Color')
        warmColor = inputColor('Warm Color RGB Tuple : ')
        TemperatureCircle(data, canvas_width, canvas_height, coolColor, warmColor, saveLoop())
        quit()
            
def dataBars():
    while True:
        numBars = input('\nPlease enter a number of data bars to display [1-3] : ')
        if numBars == 'q':
            break
        if not re.search('[1-3]', numBars):
            print('ERROR: Please input a number of bars [1-3]')
        
        numBars = int(numBars)
        datas = [None] * 3 # List of dataframes
        colors = [(None,None)] * 3 # List of tuples of tuples: (cool, warm)

        for i in range(numBars):
            prompt = 'Enter Path for CSV File ' + str(i+1) + ' : '
            print()
            datas[i] = inputFile(prompt)
            print()
            colors[i] = (inputColor('Input Cool Color Tuple: '),
                         inputColor('Input Warm Color Tuple: '))
        DataBars(canvas_width, canvas_height, numBars, 
                 datas[0], colors[0][0], colors[0][1],
                 datas[1], colors[1][0], colors[1][1],
                 datas[2], colors[2][0], colors[2][1],
                 saveLoop())
        quit()

def dot_graph():
    DotGraph(pd.read_csv('wt.csv', usecols=['value','datetime']), pd.read_csv('s.csv', usecols=['value','datetime']), canvas_width, canvas_height)


if __name__ == "__main__":
    if ( len(sys.argv) < 2 ):
        help()
    elif (sys.argv[1] == "--help"):
        help()
    elif (sys.argv[1] == "--TemperatureCircle"):
        print("Welcome to Temperature Circle! To quit at any time, press \'q\'!")
        temperature_circle()
    elif (sys.argv[1] == "--DotGraph"):
        print("Welcome to Dot Graph! To quit at any time, press \'q\'!")
        dot_graph()
    elif (sys.argv[1] == "--DataBars"):
        print("Welcome to Data Bars! To quit at any time, press \'q\'!")
        dataBars()


