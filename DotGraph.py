import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, filein: str, canvas_width: int, canvas_height: int) -> None:
        self.filein = filein
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.setup()

        [self.plot_dots(i) for i in self.data['value']]


    def setup(self):
        try:
            self.data = pd.read_csv(filepath_or_buffer=self.filepath, 
                               usecols=['value','datetime'])
        except FileNotFoundError:
            print("Error: File Not Found!")
            quit()
        self.img = Image.new(mode='RGB', size=(self.width,self.height), color='black')

    def plot_dots(self, val: float):
        pass
