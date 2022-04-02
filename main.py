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
df.info()
# Execute thermal model on all csv files and append to dataframe
temperatures = []

filenames = ['1566 Icarus.csv', '1620 Geographos.csv', '1862 Apollo.csv', '1981 Midas.csv', '2101 Adonis.csv', '2102 Tantalus.csv', '2201 Oljato.csv', '2340 Hathor.csv', '3122 Florence.csv', '3200 Phaethon.csv', '3361 Orpheus.csv', '3362 Khufu.csv', '3671 Dionysus.csv', '3757 Anagolay.csv', '4015 Wilson-Harrington.csv', '4034 Vishnu.csv', '4179 Toutatis.csv', '4183 Cuno.csv', '4486 Mithra.csv', '4660 Nereus.csv', '4769 Castalia.csv', '5604.csv', '6489 Golevka.csv', '7335.csv', '7341.csv', '7482.csv', '7822.csv', '8014.csv', '8566.csv', '9856.csv', '10115.csv', '11500 Tomaiyowit.csv', '12538.csv', '12923 Zephyr.csv', '13651.csv', '14827 Hypnos.csv', '25143 Itokawa.csv', '29075.csv', '33342.csv', '35107.csv', '35396.csv', '39572.csv', '41429.csv', '52760.csv', '52768.csv', '53319.csv', '53789.csv', '65679.csv', '65803 Didymos.csv', '66391 Moshup.csv', '68216.csv', '68346.csv', '68548.csv', '68950.csv', '85182.csv', '85713.csv', '85774.csv', '85989.csv', '85990.csv', '86039.csv', '86819.csv', '88254.csv', '89830.csv', '89959.csv', '90075.csv', '90403.csv', '90416.csv', '99248.csv', '99942 Apophis.csv', '101955 Bennu.csv', '103067.csv', '111253.csv', '138127.csv', '140158.csv', '140288.csv', '141432.csv', '143624.csv', '152671.csv', '152754.csv', '152978.csv', '153201.csv', '153591.csv', '153814.csv', '154276.csv', '159857.csv', '161989 Cacus.csv', '162000.csv', '162116.csv', '162510.csv', '162567.csv', '162998.csv', '163132.csv', '163243.csv', '163348.csv', '163818.csv', '163899.csv', '164121.csv', '164207.csv', '168318.csv', '175706.csv', '185851.csv', '187040.csv', '194268.csv', '206378.csv', '207945.csv', '215588.csv', '217628 Lugh.csv', '221980.csv', '226554.csv', '230549.csv', '231937.csv', '234145.csv', '235756.csv', '242450.csv', '242643.csv', '243566.csv', '244977.csv', '250620.csv', '250680.csv', '250706.csv', '252399.csv', '263976.csv', '264357.csv', '265196.csv', '267221.csv', '267337.csv', '269690.csv', '277570.csv', '294739.csv', '297274.csv', '297300.csv', '297418.csv', '301844.csv', '303450.csv', '304330.csv', '307493.csv', '308635.csv', '310560.csv', '312070.csv', '333578.csv', '341843.csv', '349068.csv', '357022.csv', '357024.csv', '360191.csv', '363024.csv', '363027.csv', '363505.csv', '363599.csv', '363831.csv', '365071.csv', '365424.csv', '366774.csv', '367248.csv', '369264.csv', '371660.csv', '373135.csv', '377732.csv', '381906.csv', '385186.csv', '385343.csv', '386454.csv', '386847.csv', '387505.csv', '387746.csv', '389694.csv', '390725.csv', '391211.csv', '395207.csv', '398188 Agni.csv', '409836.csv', '410778.csv', '411165.csv', '414286.csv', '414287.csv', '416801.csv', '417634.csv', '418094.csv', '419472.csv', '419624.csv', '419880.csv', '422686.csv', '422699.csv', '423321.csv', '433953.csv', '434096.csv', '434633.csv', '436329.csv', '436671.csv', '441987.csv', '442037.csv', '443806.csv', '443880.csv', '444193.csv', '445305.csv', '451124.csv', '453707.csv', '454094.csv', '454100.csv', '455299.csv', '458436.csv', '459683.csv', '462238.csv', '468468.csv', '468727.csv', '469445.csv', '471241.csv', '477519.csv', '480936.csv', '483508.csv', '484402.csv', '488789.csv', '490581.csv', '496816.csv', '496817.csv', '499582.csv', '503941.csv', '504800.csv', '505657.csv', '506074.csv', '510055.csv', '511008.csv', '511684.csv', '523589.csv', '523664.csv', '523775.csv', '523816.csv', '529668.csv', '529753.csv', '533722.csv', '538212.csv']

i = 0
for filename in filenames:
    file = os.path.join('/Users/marnixmeersman/Documents/GitHub/NACHO/ephemerides', filename)
    T = get_temperature(file, df.at[i, "albedo_computed"], df.at[i, "diameter"] * 1000, epsilon)[:, 2:][:, 2]
    temperatures.append(T)
    print(len(T))
    print(df.at[i, "Name"])
    i += len(T)+1

temperatures = np.array(temperatures).flatten()
print(len(temperatures))
# for filename in filenames:
#     file = os.path.join('/Users/marnixmeersman/Documents/GitHub/NACHO/ephemerides', filename)
#     for i in range(2557): # number of datapoints per asteroid
#         A = df.at[j+i, "albedo_computed"]
#         diameter = df.at[j+i, "diameter"] * 1000
#         R = df.at[j+i, "distance"] * 1000
#
#         T = get_temperature(file, A, diameter, epsilon)[:, 2:][i, 2]
#         print(j, i, j+i, df.at[j+1, "date"], T, df.at[j+1, "Name"], filename)
#         temperatures.append(T)
#     j += 2557

df = df.assign(temperature = temperatures)
df.to_csv('/Users/marnixmeersman/Documents/GitHub/NACHO/all_with_temps')
print(df)
