import math
import numpy
import matplotlib.pyplot as plt

mm = 1000
M_A = 1108.394
R_A = 1045.064
R_B = 2035/6 #339.2N
R_C = 4565/6 #760.8N
R_D = 5.6*9.81

y = 75/2
RL = 900

def M(z): 
    if 0<=z<=750:
        return (R_A*(z))/1000 - M_A
    elif 750<z<=1950:
        return (R_A*(z) - R_B*(z - 750))/1000 - M_A
    elif 1950<z<=2250:
        return (R_A*(z) - R_B*(z - 750) - R_C*(z - 1950))/1000 - M_A

def I_xx(z,ReinforceLength):

    I_reinforce = 0
    I_web = 0.8*(75**3)/12
    I_stringerVertical = 4 * ( (0.8*(20**3)/12 + 0.8*20*(0.8**2)) )
    I_plate = 2* ( (40.8*(0.8**3))/12 + (40.8*0.8*(75.4**2)))

    #n represents number of reinforcements (where n=1 is the first layer)
    if z < ReinforceLength:
        n = 2
    elif ReinforceLength <= z <= 2250:
        n = 1
    
    for i in range(0,n):
        I_reinforce += ( (19.2)*(0.8**3)/12 + (19.2)*(0.8)  * ( (75-0.4-1.8*(i-1))**2 )  ) *4 
    
    print("Web: " + str(I_web) + " || Stringer: " + str(I_stringerVertical) + " || plate: " + str(I_plate) + " || Horizontal things: " + str(I_reinforce))

    return I_reinforce+I_web+I_stringerVertical + I_plate

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
    #RL is reinforcement length
    for z in range(0,2250):
        stress.append(( 1000*M(z) * y ) / I_xx(z,RL))
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



#def BoltSpacing():


#def interRivetBuckling();