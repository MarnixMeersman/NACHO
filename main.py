import os
import numpy as np
import pandas as pd
from thermal_model import get_temperature

def get_albedos(dataframe):
    albedo_lst = []
    for i in range(dataframe.shape[0]):
        D = dataframe.at[i, "diameter"]
        H = dataframe.at[i, "H"]
        bedo = (1329 / D) * 10 ** (-0.2 * H)
        albedo_lst.append(bedo)
    return albedo_lst


# Constants
epsilon = 0.965

# Import dataframe
df = pd.read_csv("/Users/marnixmeersman/Documents/GitHub/NACHO/data.csv", sep=",")

# Computed albedos
albedos = get_albedos(df)
df = df.assign(albedo_computed = albedos)

# Execute thermal model on all csv files and append to dataframe
temperatures = []
j = 0
for filename in os.listdir('/Users/marnixmeersman/Documents/GitHub/NACHO/ephemerides'):
    file = os.path.join('/Users/marnixmeersman/Documents/GitHub/NACHO/ephemerides', filename)
    for i in range(2557): # number of datapoints per asteroid
        A = df.at[j+i, "albedo_computed"]
        diameter = df.at[j+i, "diameter"] * 1000
        R = df.at[j+i, "distance"] * 1000

        T = get_temperature(file, A, diameter, epsilon)[:, 2:][i, 2]
        print(j, i, j+i, df.at[j+1, "date"], T, df.at[j+1, "Name"], filename)
        temperatures.append(T)
    j += 2557

df = df.assign(temperature = temperatures)
df.to_csv('/Users/marnixmeersman/Documents/GitHub/NACHO/all_with_temps')
print(df)
