import re
import sys
import pandas as pd

from DataBars import DataBars
from LineGraph import LineGraph
from SalinityCircle import SalinityCircle
from TemperatureCircle import TemperatureCircle
from Resampler import Resampler

# Set the initial canvas dimensions
CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 1500
RGB_REGEX = "^\((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])),(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))\)$"

def help():
    print('\nART GENERATOR USAGE:')
    print('--help               print this usage information')
    print('--TemperatureCircle  create a radial color circle')
    print('--SalinityCircle     create a radial color circle very similar to TemperatureCircle with presets adjusted for salinity data')
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
        except ValueError:
            print("ERROR: CSV Must contain a \'datetime\' and a \'value\' column.\n")
            continue
        return data

def outputFile(prompt: str):
    while True:
        fileOut = input(prompt)
        if fileOut == 'q':
            quit()
        elif fileOut.endswith('.csv\"') or fileOut.endswith('.csv\''):
            fileOut = fileOut[1:-1]
        elif not fileOut.endswith('.csv'):
            print('ERROR: File must be of type *.csv!\n')
            continue
        return fileOut

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
        TemperatureCircle(data, CANVAS_WIDTH, CANVAS_HEIGHT, coolColor, warmColor, saveLoop())
        print()
        quit()

def salinity_circle():
    while True:
        data = inputFile('\nPlease Enter CSV Filepath : ')
        print('\nPlease Enter Cool Color')
        coolColor = inputColor('Cool Color RGB Tuple : ')
        print('\nPlease Enter Warm Color')
        warmColor = inputColor('Warm Color RGB Tuple : ')
        SalinityCircle(data, CANVAS_WIDTH, CANVAS_HEIGHT, coolColor, warmColor, saveLoop())
        print()
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
        DataBars(CANVAS_WIDTH, CANVAS_HEIGHT, numBars, 
                 datas[0], colors[0][0], colors[0][1],
                 datas[1], colors[1][0], colors[1][1],
                 datas[2], colors[2][0], colors[2][1],
                 saveLoop())
        print()
        quit()

def line_graph():
    data1 = inputFile('\nPlease Enter CSV Filepath 1 : ')
    data2 = inputFile('\nPlease Enter CSV Filepath 2 : ')
    print('\nPlease Enter Cool Color')
    coolColor = inputColor('Cool Color RGB Tuple : ')
    print('\nPlease Enter Warm Color')
    warmColor = inputColor('Warm Color RGB Tuple : ')

    LineGraph(data1, data2, CANVAS_WIDTH, CANVAS_HEIGHT, coolColor, warmColor, saveLoop())
    print()

def csv_cleaner():
    while True: # Input REPL
        fileIn = input('\nPlease Enter Input CSV Filepath: ')
        if fileIn == 'q':
            quit()
        elif fileIn.endswith('.csv\"') or fileIn.endswith('.csv\''):
            fileIn = fileIn[1:-1]
        elif not fileIn.endswith('.csv'):
            print('ERROR: File must be of type *.csv!\n')
            continue
        try:
            data = pd.read_csv(fileIn, usecols=['value','datetime'])
            break
        except FileNotFoundError:
            print("ERROR: File Not Found!\n")
            continue
        except ValueError:
            print("ERROR: CSV Must contain a \'datetime\' and a \'value\' column.\n")
            continue

    fileOut = outputFile('\nPlease Enter Output CSV Filepath: ') # Output REPL

    while True: # Resample REPL
        r = input('\nResample to Hourly Averages? [y/n] : ')
        if ( r == 'q' ):
            quit()
        elif ( r == 'y' or r == 'Y' or r == 'yes' or r == 'Yes' ):
            resample = True
            print('Resampling to Hourly Averages!')
            break
        elif ( r == 'n' or r == 'N' or r == 'no' or r == 'No' ):
            resample = False
            print('Not Resampling!')
            break
        else:
            print("ERROR: Please enter yes (y) or no (n)")

    print('\nCSV Cleaned!')        
    Resampler(data, fileOut, resample)
    

if __name__ == "__main__":
    if ( len(sys.argv) < 2 ):
        help()
    elif ( sys.argv[1] == "--TemperatureCircle" ):
        print("\nWelcome to Temperature Circle! To quit at any time, press \'q\'!")
        temperature_circle()
    elif ( sys.argv[1] == "--SalinityCircle" ):
        print("\nWelcome Salinity Circle! To quit at any time, press \'q\'!")
        salinity_circle()
    elif ( sys.argv[1] == "--LineGraph" ):
        print("\nWelcome to Line Graph! To quit at any time, press \'q\'!")
        line_graph()
    elif ( sys.argv[1] == "--DataBars" ):
        print("\nWelcome to Data Bars! To quit at any time, press \'q\'!")
        dataBars()
    elif ( sys.argv[1] == "--CSVCleaner" ):
        print("\nWelcome to the CSV Cleaner! To quit at any time, press \'q\'!")
        csv_cleaner()
    else:
        help()
    
