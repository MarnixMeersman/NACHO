import os
import numpy as np
import pandas as pd
from thermal_model import get_temperature

df = pd.read_csv("data.csv", sep=",")