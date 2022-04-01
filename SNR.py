import numpy as np
import pandas as pd
from scipy.integrate import quad

h = 6.62607004 * 10**-34 # Planck constant
c = 299792458 # m/s
integration_time = 1

def albedo(D, H):
    return (1329/D)*10**(-0.2*H)

def E_lamda(lamda, T, epsilon):
    #T = 250 #average between 200-300
    # emit 10-20 micron region
    c1 = 3.7418*10**8
    c2 = 14388
    return epsilon * ((c1/lamda**5) * (1/((np.exp(c2/(lamda*T))) - 1)))

# def S(D, diameter, R, wavelenghth_min, wavelenghth_max, T, epsilon, time, quantum_efficiency): # quantum efficiency, atmospheric stuff and instrument stiff all neglected.
#     temp1 = (D**2)*time*(2*np.pi*(diameter/2)**2)
#     temp2 = 4*h*c*R**2
#     temp3 = quad(lamda_E_lamda, wavelenghth_min, wavelenghth_max, args= (T, epsilon))
#     return ((temp1/temp2) * temp3[0])/quantum_efficiency

def S(D, t, theta, A0, R, wavelength, tau0, eff_q, E):
    temp1 = D**2 * t * np.cos(theta) * A0 * wavelength * tau0 * eff_q * E
    temp2 = 4 * R**2 * h * c
    return temp1 / temp2


def radiant_flux(D,  T0, Et):
        return (np.pi/4)*(D**2)*(T0*Et)



def main():
    df = pd.read_csv('data.csv', sep=",")

    albedo_lst = []
    for i in range(df.shape[0]):
        bedo = albedo(df.at[i, "diameter"], df.at[i, "H"])
        albedo_lst.append(bedo)
    df = df.assign(albedo_computed = albedo_lst)

    SNR_lst = []
    for i in range(df.shape[0]):
        D = 0.5
        diameter = df.at[i, "diameter"] #* 1000
        A = 2 * np.pi * (diameter / 2) ** 2
        R = df.at[i, "closest distance"] #* 1000
        q_e = 0.5 # avg efficiency of hubble
        T = 250 # assumption for now
        avg_wavel = 10#*10**-6 #microns
        epsilon = 0.975
        E = E_lamda(avg_wavel, T, epsilon)
        Signal = S(D, integration_time, 0.0, A, R, avg_wavel, 1.0, q_e, E)
        Noise = np.sqrt(Signal)
        SNR = Signal/Noise
        SNR_lst.append(SNR)

    df = df.assign(SNR = SNR_lst)

    pd.set_option('display.max_columns', None)
    print(df)

if __name__ == "__main__":
    main()

