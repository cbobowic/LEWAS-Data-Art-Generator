import pandas as pd
import sys

def write_csv(filein: str, fileout: str):
    '''This method reads a csv, converts the 'datetime' column to pandas Timestamp,
    and resamples the data to result in the hourly average. This saves significant
    processing time when generating (and testing) different art classes.
    
    :param str filein : the relative path of the input file to be processed.
    :param str fileout : the relative path and name of the output file.'''
    try:
        df = pd.read_csv(filein,usecols=['id','value','datetime'], index_col=['datetime'])
    except FileNotFoundError:
        print("Error: CSV File Not Found")
        quit()
    
    df.index = pd.to_datetime(df.index, utc=True)
    # Uncomment to resample the values to average each hour
    df = df.resample('H')[['value']].mean()
    
    df.to_csv(fileout)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Error: Please include an input and output path!")
    elif not (sys.argv[1].endswith('.csv') and sys.argv[2].endswith('.csv')):
        print("Error: Argument filenames must both be of file type *.csv")
    else:
        filein = sys.argv[1]
        fileout = sys.argv[2]
        write_csv(filein, fileout)