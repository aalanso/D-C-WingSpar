import math
import numpy
import matplotlib.pyplot as plt
import ummm as A
mm = 1000
M_A = 1108.394
R_A = 1045.064
R_B = 2035/6 #339.2N
R_C = 4565/6 #760.8N
R_D = 5.6*9.81

y = 75/2
RL = 900



def V(z):
    if 0<=z<=750: return R_A
    elif 750<z<=1950: return R_A - R_B
    elif 1950<z<=2250: return R_A - R_B - R_C



def M(z): 
    if 0<=z<=750: return (R_A*(z))/mm - M_A
    elif 750<z<=1950: return (R_A*(z) - R_B*(z - 750))/mm - M_A
    elif 1950<z<=2250: return (R_A*(z) - R_B*(z - 750) - R_C*(z - 1950))/mm - M_A

def totalMoment():
    moment = []
    pos = []
    for i in range(0,2250):
        moment.append(M(i))
        pos.append(i)
    fig, ax = plt.subplots()
    ax.plot(pos,moment)
    plt.show()

def Bending():
    stress = []
    pos = []
    #RL is reinforcement length, 300mm seems to be best?
    for z in range(0,2250):
        stress.append(( 1000*M(z) * y ) / A.I_xx(z, 1, [300]))
        pos.append(z)
    fig, az = plt.subplots()
    az.plot(pos,stress)
    plt.show()
#Bending()

#totalMoment()
def ShearBuckling(z,ReinforceLength):
    K = 8.1
    b = 40/mm
    E = 71700
    #Thickness is a function of z position
    if z<= ReinforceLength:
        t=0.8*2 /mm
    elif ReinforceLength<z<=2250:
        t = 0.8 /mm
    return K*E*(t/b)**2

def ShearBucklingGraph():
    #Critical Tau
    T_cr = []
    pos = []
    
    for z in range(0,2250):
        T_cr.append(ShearBuckling(z,RL))
        pos.append(z)
    fig, az = plt.subplots()
    az.plot(pos,T_cr)
    plt.show()
#ShearBucklingGraph()

def shearStress_NA():
    t = 1.5
    tau = []
    pos = []
    for z in range(0,2250):
        tau.append( ( V(z) * A.Q_NA(z,1,[900]) ) / ( t * A.I_xx(z,1,[900]) ) )
        pos.append(z)
    fig, az = plt.subplots()
    az.plot(pos,tau)
    plt.show()
shearStress_NA()


def shearStress_Bolts():
    t = 1.5
    tau = []
    pos = []
    for z in range(0,2250):
        tau.append( ( V(z) * A.Q_NA(z,1,[900]) ) / ( t * A.I_xx(z,1,[900]) ) )
        pos.append(z)
    fig, az = plt.subplots()
    az.plot(pos,tau)
    plt.show()
