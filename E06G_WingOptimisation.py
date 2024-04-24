import math
import numpy
import matplotlib.pyplot as plt

M_A = 1108.394
R_A = 1045.064
R_B = 2075/3
R_C = 925/3
R_D = 5.6*9.81

y = 75/2

def M(z): 
    if 0<=z<=750:
        return (R_A*(z))/1000 - M_A
    elif 750<z<=1950:
        return (R_A*(z) - R_B*(z - 750))/1000 - M_A
    elif 1950<z<=2250:
        return (R_A*(z) - R_B*(z - 750) - R_C*(z - 1950))/1000 - M_A

def I_xx(z):
    I_reinforce = 0
    I_web = 0.8*(75**3)/12
    I_stringerVertical = 4 * ( (0.8*(20**3)/12 + 0.8*20*(0.8**2)) )
    if z <= 750:
        I_reinforce = 0
        n = 2
    elif 750< z <=1950:
        I_reinforce = 0
        n = 1
    elif 1950 < z <= 2250:
        n=0
        I_reinforce = ( (19.2)*(0.8**3)/12 + (19.2)*(0.8)  * ( (75-0.4)**2 )  ) *4
    for i in range(0,n):
        I_reinforce += ( (19.2)*(0.8**3)/12 + (19.2)*(0.8)  * ( (75-0.4-1.8*i)**2 )  ) *4 
    return I_reinforce+I_web+I_stringerVertical

def totalMoment():
    moment = []
    pos = []
    for i in range(0,2250):
        moment.append(M(i))
        pos.append(i)
    fig, ax = plt.subplots()
    ax.plot(pos,moment)
    plt.show()

#totalMoment()
#def ShearBuckling():

def Bending():
    stress = []
    pos = []
    for z in range(0,2250):
        stress.append(( 1000*M(z) * y ) / I_xx(z))
        pos.append(z)
    fig, az = plt.subplots()
    az.plot(pos,stress)
    plt.show()
Bending()

#def BoltSpacing():


#def interRivetBuckling();