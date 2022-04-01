import numpy as np
import pandas as pd
from thermal_model import get_temperature
# from scipy.integrate import quad

h = 6.62607004e-34 # Planck constant
c = 299792458 # m/s
integration_time = 60*60
wavelength_min = 8
wavelength_max = 12
avg_lamda = (wavelength_min + wavelength_max)/2
f = 1.6


def albedo(D, H):
    return (1329/D)*10**(-0.2*H)

def lamda_E_lamda(lamda, T, epsilon):
    #T = 250 #average between 200-300
    # emit 10-20 micron region
    c1 = 3.7418*10**8
    c2 = 14388
    # print (epsilon * (   (c1/lamda**4) * (1/((np.exp(c2/(lamda*T)))-1))   ))
    return epsilon * (   (c1/lamda**4) * (1/((np.exp(c2/(lamda*T)))-1))   )

def S(D, diameter, R, T, epsilon, time): # quantum efficiency, atmospheric stuff and instrument stiff all neglected.
    temp1 = (D**2)*time*(4*np.pi*(diameter/2)**2)
    temp2 = 4*h*c*R**2
    # temp3 = quad(lamda_E_lamda, wavelength_min, wavelength_max, args = (T, epsilon))
    #print(temp3[0])
    c1 = 3.7418*10**8
    c2 = 14388
    # print (epsilon * (   (c1/avg_lamda**5) * (1/((np.exp(c2/(avg_lamda*T)))-1))   ))
    return (temp1/temp2) * avg_lamda* epsilon * (   (c1/avg_lamda**4) * (1/((np.exp(c2/(avg_lamda*T)))-1))   ) # temp3[0]

def B(D, time, f):
    # det_area = 1.7689**10(-4) # From Cheops 13.3mm x 13.3mm
    return (np.pi/(4*h*c))*((D**2)/(f**2))*avg_lamda*(1.7689e-4)*time

# print(S(1, 1, 30767248000, 0, 20, 250, 1 ,10))
# def radiant_flux(D,  T0, Et):
#         return (np.pi/4)*(D**2)*(T0*Et)

df = pd.read_csv('data.csv', sep=",")

albedo_lst = []

for i in range(df.shape[0]):
    bedo = albedo(df.at[i, "diameter"], df.at[i, "H"])
    albedo_lst.append(bedo)
df = df.assign(albedo_computed = albedo_lst)

SNR_lst = []
for i in range(df.shape[0]):
    D = 0.5
    diameter = df.at[i, "diameter"] * 1000
    R = df.at[i, "closest distance"] * 1000
    T = 250
    epsilon = 0.965
    t = integration_time
    Signal = S(D, diameter, R, T, epsilon, t)
    f = 1.6
    Background = B(D, t, f)
    # print(Background)
    Noise = np.sqrt(Background + Signal)
    SNR = Signal/Noise
    SNR_lst.append(SNR)

df = df.assign(SNR = SNR_lst)
print(df.info())

pd.set_option('display.max_columns', None)
print(df)

