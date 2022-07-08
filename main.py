import re
import sys
import time
import pandas as pd
import random as rnd
from PIL import Image, ImageDraw

from DataBars import DataBars
from LineGraph import LineGraph
from TemperatureCircle import TemperatureCircle

# Set the initial canvas dimensions
CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 1500
RGB_REGEX = "^\((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))\)$"


def drawPoints():
    img = Image.new(mode='RGB', size=(CANVAS_WIDTH, CANVAS_HEIGHT), color='black')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # DISTANCE AMONG POINTS
    step = 10
    for n in range(step, w, step):
        for x in range(step, h - step, step):
            ran = rnd.uniform(0.0, 40.0)
            a = n + ran
            b = x + ran
            if a > CANVAS_WIDTH:
                a = n
            if b > CANVAS_HEIGHT:
                b = x
            draw.point((a, b), fill="yellow")
    img.show()


def help():
    print('\nART GENERATOR USAGE:')
    print('--help               print this usage information')
    print('--TemperatureCircle  create a radial color circle')
    print('--LineGraph          create an graph of lines representing changes in data values')
    print('--DataBars           create 1, 2, or 3 bars representing data values\n')

def inputColor(prompt: str) -> tuple:
    while True:
        colorIn = input(prompt)
        if colorIn == 'q':
            quit()
        colorIn = colorIn.replace(' ','')
        if re.search(RGB_REGEX,colorIn):
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
        elif fileIn.endswith('.csv\"') or fileIn.endswith('.csv\''):
            fileIn = fileIn[1:-1]
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
        elif ( saveIn == 'y' or saveIn == 'Y' or saveIn == 'yes' or saveIn == 'Yes' ):
            filepath = input("Enter File Path : ")
            if ( filepath.endswith('.jpg\'') or filepath.endswith('.jpg\"') or 
                 filepath.endswith('.png\'') or filepath.endswith('.png\"') ):
                filepath = filepath[1:-1]
            elif not ( filepath.endswith('.jpg') or filepath.endswith('.png') ):
                print("ERROR: File must be of type *.jpg or *.png!\n")
                continue
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
        # start = time.time()
        TemperatureCircle(data, CANVAS_WIDTH, CANVAS_HEIGHT, coolColor, warmColor, saveLoop())
        # print("Total Time : " , round((time.time()-start),4) , ' seconds')
        print()
        quit()
    # start = time.time()
    # TemperatureCircle(pd.read_csv('LEWAS_data\Cleaned_data\cleaned_temp.csv', usecols=['datetime','value']), canvas_width, canvas_height, (0,0,255), (255,120,0), None)
    # TemperatureCircle(pd.read_csv('s.csv',usecols=['datetime','value']), canvas_width, canvas_height, (0,0,255), (255,120,0), None)
    # print("Total Time : " , round((time.time()-start),4) , ' seconds')

    
            
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
        DataBars(CANVAS_WIDTH, CANVAS_HEIGHT, numBars, 
                 datas[0], colors[0][0], colors[0][1],
                 datas[1], colors[1][0], colors[1][1],
                 datas[2], colors[2][0], colors[2][1],
                 saveLoop())
        print()
        quit()

def dot_graph():
    while True:
        data1 = inputFile('\nPlease Enter CSV Filepath 1 : ')
        data2 = inputFile('\nPlease Enter CSV Filepath 2 : ')
        print('\nPlease Enter Cool Color')
        coolColor = inputColor('Cool Color RGB Tuple : ')
        print('\nPlease Enter Warm Color')
        warmColor = inputColor('Warm Color RGB Tuple : ')

        LineGraph(data1, data2, CANVAS_WIDTH, CANVAS_HEIGHT, coolColor, warmColor, saveLoop())
        print()
        quit()

if __name__ == "__main__":
    if ( len(sys.argv) < 2 ):
        help()
    elif (sys.argv[1] == "--TemperatureCircle"):
        print("\nWelcome to Temperature Circle! To quit at any time, press \'q\'!")
        temperature_circle()
    elif (sys.argv[1] == "--LineGraph"):
        print("\nWelcome to Line Graph! To quit at any time, press \'q\'!")
        dot_graph()
    elif (sys.argv[1] == "--DataBars"):
        print("\nWelcome to Data Bars! To quit at any time, press \'q\'!")
        dataBars()
    else:
        help()
    
