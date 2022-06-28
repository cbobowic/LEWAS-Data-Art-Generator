import math
from random import random
import pandas as pd
from PIL import Image, ImageDraw

class DotGraph:

    def __init__(self, data: pd.DataFrame, canvas_width: int, canvas_height: int) -> None:
        self.data = data
        self.width = canvas_width
        self.height = canvas_height

    def setup():
        