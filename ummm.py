# import E06G_WingOptimisation as F
import matplotlib.pyplot as plt
import numpy as np
bolt_tau_max = 311e6

sigma_ult = 483e6
sigma_y = 345e6
E = 71.7e9 
rho = 2780 #kg/m^3

K_s = 8.1

# ========= stolen
M_A = 1075.5
R_A = 1045.064
R_B = 4565 / 6 # 760.8N
R_C = 2035 / 6 # 339.2N
R_D = 5.6 * 9.81

y = 75 / 2
RL = 900


def V(z):
    if 0 <= z <= 750:
        return R_A
    elif 750 < z <= 1950:
        return R_A - R_B
    elif 1950 < z <= 2250:
        return R_A - R_B - R_C



def M(z):
    if 0 <= z <= 750:
        return (R_A * (z)) * mm - M_A
    elif 750 < z <= 1950:
        return (R_A * (z) - R_B * (z - 750)) * mm - M_A
    elif 1950 < z <= 2250:
        return (R_A * (z) - R_B * (z - 750) - R_C * (z - 1950)) * mm - M_A


# =======

mm = 1/1000

# safety factors
sf_bending = sf_buckling = 1.5


# 50cm of no flanges saves ~90g


def mass(no_reinf, reinf_len, no_flange_len_mm, n_bolts):
    volume_f = 2*40.8*0.8*(2250-no_flange_len_mm) * (mm)**3 #mm**3 is for unit conversion to meters^3
    volume_w = 0.8*148.4*2250 *(mm)**3
    volume_sv = 4*1.5*20*2250 * (mm)**3
    volume_sh = 4*18.5*1.5*2250 * (mm)**3
    # this overestimates wrt masses from reader by around 5%
    volume_tot = volume_f+volume_sh+volume_sv+volume_w
    for i in  range(no_reinf): volume_tot += 4*18.5*0.8*reinf_len[i] * (mm)**3
    return volume_tot*rho + n_bolts * 0.00139

#print(mass(1, [900]))
#print(mass(1, [900]) * rho)

# z in cm, reinf_lengths in cm as well
def I_xx(z, n_reinf, reinf_lengths, no_flange_len_mm):
    I_res = 0

    I_web = 0.8 * (148.4 ** 3) / 12
    I_stringer_vertical = 4 * ((1.5 * (20 ** 3) / 12 + 1.5 * 20 * (64.2 ** 2)))
    I_stringer_h = ((18.5) * (1.5 ** 3) / 12 + (18.5) * (1.5) * ((74.2 - 0.75) ** 2)) * 4

    if z < 2250-no_flange_len_mm:
        I_flanges = 2 * (40 * (0.8 ** 3) / 12 + 40 * 0.8 * (74.6) ** 2)
    else:
        I_flanges = 0

    I_res = I_web + I_stringer_h + I_stringer_vertical + I_flanges

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            I_res += ( (18.5)*(0.8**3)/12 + (18.5)*(0.8) * ((74.2-0.75-0.8*(i+1))**2)) *4

    return I_res  # mm4


# print(I_xx(1000, 0, []))

def Q_NA(z, n_reinf, reinf_lengths, no_flange_len_mm):
    Q_web = 0.8 * 74.2 * 37.1
    Q_stringer_vertical = 2 * (20 * 1.5 * 64.2)
    Q_stringer_h = (18.5 * 1.5 * (74.2 - 0.75)) * 2

    if z < 2250 - no_flange_len_mm:
        Q_flange = (40 * 0.8 * 74.6)
    else:
        Q_flange = 0

    Q_res = Q_web + Q_stringer_h + Q_stringer_vertical + Q_flange

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            Q_res += 2 * ((74.2 - 1.5 - 0.4 - 0.8 * i) * (18.5 * 0.8))

    return Q_res  # mm3


def Q_Bolt(z, n_reinf, reinf_lengths):
    for n in range(0, n_reinf):
        if n > 1:
            for i in range(0, n_reinf):
                if z > reinf_lengths[i]:
                    n_reinf -= 1
                    Q_Bolt_Res = (((150-(0.8+1.5*(n_reinf-1))/(2))*(148.4*0.8+1.5*(n_reinf-1))))
        elif n == 1:
            Q_Bolt_Res = (((150 - (0.8)/ (2)) * (148.4 * 0.8)))
        else:
            print("invalid amount of reinforcements")






def get_bending_stress(M_int, I_xx_mm4):
    s = M_int * 75 * 1e-3 / (I_xx_mm4 * 1e-12)
    return s


def get_shear_buckling(V_int, Q_mm3, I_xx_mm4):
    b = 108.4  # height-2*height_stringer (less strict on stringers)
    t = 0.8
    tau_crit = K_s * E * (t / b) ** 2
    tau_int = (V_int * Q_mm3 / (I_xx_mm4 * 0.8)) * 1e6
    # tau = VQ/It
    return tau_crit



def eval_setup(n_reinf, reinf_lengths, no_flange_len, n_bolts):
    tau_int = []
    sigma_bending = []
    I = []
    Q = []
    tau_crit = []
    V_int = []

    for z in range(0, 2250):
        I_here = I_xx(z, n_reinf, reinf_lengths, no_flange_len)
        Q_here = Q_NA(z, n_reinf, reinf_lengths, no_flange_len)
        tau_int.append(V(z) * Q_here * 1e6 / (I_here * 0.8))
        tau_crit.append(get_shear_buckling(V(z), Q_here, I_here))
        sigma_bending.append(get_bending_stress(M(z), I_here))
        I.append(I_here)
        Q.append(Q_here)
        V_int.append(V(z))



    print("Max bending stress: {}".format(max(sigma_bending)))
    print("Max internal shear stress: {}".format(max(tau_int)))

    fig, ax = plt.subplots()
    ax.plot(tau_int, label="int")
    ax.plot(tau_crit, label="crit")
    plt.legend()

    plt.ylabel("Tau Internal")
    plt.show()




    fig, ax = plt.subplots()
    ax.plot(sigma_bending, label="sigma bending")
    ax.plot(np.full((2250), sigma_y), label="sigma_y")
    plt.ylabel("Sigma Bending")
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(I)
    plt.ylabel("I_xx [mm4]")
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(Q)
    plt.ylabel("Q_NA [mm3]")
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(V_int)
    plt.ylabel("V_int [N]")
    plt.show()

    print(mass(n_reinf, reinf_lengths, no_flange_len, n_bolts))


eval_setup(0, [], 1500, 60)

#
# F_max_bolt = bolt_tau_max * 0.25*3.14159*(0.004**2)
# # commented away not true
# print("F_max_bolt [N]: {}".format(F_max_bolt))
# #print("Q: {} [mm3]".format(qqq))
# print("I_xx [mm4]: {}".format(I_xx(1, 0,[])))
# print("V_int [N]: {}".format(V(1)))
#
#
# s_max_irb = 0.8 * ( ( -(0.9*2.1*E) / get_bending_stress(M(1), I_xx(1, 0, [])) )**0.5)
# print("s_max_irb: [mm] {}".format(s_max_irb))

# def get_normal_flow_spacing(z):
#     sm = M(z)*75/I_xx(z, 0, [])
#     print(sm)
#     qs = M(z)*74.2*20/I_xx(z, 0, [])
#     qp = M(z)*75*20/I_xx(z, 0, [])
#     dq = qs - qp
#     dq = 1e6 * dq
#     F_max_bolt = bolt_tau_max * 0.25 * 3.14159 * (0.004 ** 2) # N
#
#     return F_max_bolt/dq
#
#
# print(get_normal_flow_spacing(1))


