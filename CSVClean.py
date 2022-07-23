import pandas as pd

class CSVCleaner:

    def __init__(self, data: pd.DataFrame, fileout: str, resample: bool):
        self.df = data
        self.fileout = fileout
        self.resample = resample
        self.write_csv()

    def write_csv(self):
        self.df.index = pd.to_datetime(self.df.index, utc=True)
        # Uncomment to resample the values to average each hour
        if ( self.resample ):
            self.df = self.df.resample('H')[['value']].mean()

        self.df.to_csv(self.fileout)
