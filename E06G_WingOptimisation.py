import math
import numpy
import matplotlib.pyplot as plt

M_A = 1108.394
R_A = 1045.064
R_B = 2075/3
R_C = 925/3
R_D = 5.6*9.81

def M(z): 
    if 0<=z<=750:
        return (R_A*(z))/1000 - M_A
    elif 750<z<=1950:
        return (R_A*(z) - R_B*(z - 750))/1000 - M_A
    elif 1950<z<=2250:
        return (R_A*(z) - R_B*(z - 750) - R_C*(z - 1950))/1000 - M_A


moment = []
z = []

def totalMoment():
    for i in range(0,2250):
        moment.append(M(i))
        z.append(i)
    fig, ax = plt.subplots()
    ax.plot(z,moment)
    plt.show()
totalMoment()
#def ShearBuckling():

#stress = ( M(Z) * y ) / I_xx
#def Bending():


#def BoltSpacing():


#def interRivetBuckling();
    
