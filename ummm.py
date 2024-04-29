# import E06G_WingOptimisation as F
import matplotlib.pyplot as plt
bolt_tau_max = 311e6

sigma_ult = 483e6
sigma_y = 345e6
E = 71.7e9 
rho = 2780 #kg/m^3

K_s = 8.1

# ========= stolen
M_A = 1108.394
R_A = 1045.064
R_B = 2035 / 6  # 339.2N
R_C = 4565 / 6  # 760.8N
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


# variables: 3 spacings, reinf 1 length,
# other than that default config from manual

def mass(no_reinf, reinf_len):
    volume_f = 2*40*0.8*2250 * (mm)**3 #mm**3 is for unit conversion to meters^3
    volume_w = 0.8*148.4*2250 *(mm)**3
    volume_sv = 4*1.5*20*2250 * (mm)**3
    volume_sh = 4*18.5*1.5 * (mm)**3
    volume_tot = volume_f+volume_sh+volume_sv+volume_w
    for i in  range(no_reinf): volume_tot += 4*18.5*0.8*reinf_len[i] * (mm)**3 
    return volume_tot

#print(mass(1, [900]))
#print(mass(1, [900]) * rho)

# z in cm, reinf_lengths in cm as well
def I_xx(z, n_reinf, reinf_lengths):
    I_res = 0

    I_web = 0.8 * (148.4 ** 3) / 12
    I_stringer_vertical = 4 * ((1.5 * (20 ** 3) / 12 + 1.5 * 20 * (64.2 ** 2)))
    I_stringer_h = ((18.5) * (1.5 ** 3) / 12 + (18.5) * (1.5) * ((74.2 - 0.75) ** 2)) * 4
    I_flanges = 2 * (40 * (0.8 ** 3) / 12 + 40 * 0.8 * (74.6) ** 2)

    I_res = I_web + I_stringer_h + I_stringer_vertical + I_flanges

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            I_res += ( (18.5)*(0.8**3)/12 + (18.5)*(0.8) * ((74.2-0.75-0.8*(i+1))**2)) *4

    return I_res  # mm4


# print(I_xx(1000, 0, []))

def Q_NA(z, n_reinf, reinf_lengths):
    Q_web = 0.8 * 74.2 * 37.1
    Q_stringer_vertical = 2 * (20 * 1.5 * 64.2)
    Q_stringer_h = (18.5 * 1.5 * (74.2 - 0.75)) * 2
    Q_flange = (40 * 0.8 * 74.6)

    Q_res = Q_web + Q_stringer_h + Q_stringer_vertical + Q_flange

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            Q_res += 2 * ((74.2 - 1.5 - 0.4 - 0.8 * i) * (18.5 * 0.8))

    return Q_res  # mm3


def Q_Bolt(z, n_reinf, reinf_lengths):
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


def get_tau_int(z):
    print(get_shear_buckling(1045, Q_NA(1, 0, []), I_xx(1, 0, [])))


tau_int = []
sigma_bending = []
zz = range(0, 1000)

for z in range(0, 1000):
    I_here = I_xx(z, 0, [])
    tau_int.append(get_shear_buckling(V(z), Q_NA(z, 0, []), I_here))
    sigma_bending.append(get_bending_stress(M(z), I_here))

fig, ax = plt.subplots()
ax.plot(tau_int, sigma_bending)
plt.show()
