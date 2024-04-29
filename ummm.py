#import E06G_WingOptimisation as F

bolt_tau_max = 311e6

sigma_ult = 483e6
sigma_y = 345e6
E = 71.7e9
rho = 2780

K_s = 8.1


# safety factors
sf_bending = sf_buckling = 1.5



# variables: 3 spacings, reinf 1 length,
# other than that default config from manual

# z in cm, reinf_lengths in cm as well
def I_xx(z, n_reinf, reinf_lengths):
    I_res = 0

    I_web = 0.8*(148.4**3)/12
    I_stringer_vertical = 4 * ( (1.5*(20**3)/12 + 1.5*20*(64.2**2)))
    I_stringer_h = ((18.5) * (1.5 ** 3) / 12 + (18.5) * (1.5) * ((74.2 - 0.75) ** 2)) * 4
    I_flanges = 2*(40*(0.8**3)/12 + 40*0.8*(74.6)**2)

    # print(I_web)
    # print(I_stringer_vertical)
    # print(I_stringer_h)
    # print(I_flanges)

    I_res = I_web + I_stringer_h + I_stringer_vertical + I_flanges

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            I_res += ( (18.5)*(1.5**3)/12 + (18.5)*(1.5) * ((74.2-0.75-1.5*(i+1))**2)) *4

    return I_res # mm4

#print(I_xx(1000, 0, []))

def Q_NA(z, n_reinf, reinf_lengths):

    Q_web = 0.8 * 74.2 * 37.1
    Q_stringer_vertical = 2 * (20 * 1.5 * 64.2)
    Q_stringer_h = (18.5 * 1.5 * (74.2-0.75)) * 2
    Q_flange = (40 * 0.8 * 74.6)

    Q_res = Q_web + Q_stringer_h + Q_stringer_vertical + Q_flange

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            Q_res += (148.4-2*1.5-0.8) * 1.5 * (74.2-0.75/2-1.5*(i+1))

    return Q_res  # mm3


def eval_bending_stress(M_int, I_xx_mm4):
    s = M_int * 75*1e-3/(I_xx_mm4*1e-12)
    return s * sf_bending < sigma_y

def eval_shear_buckling(V_int, Q_mm3, I_xx_mm4):
    b = 110 # height-2*height_stringer (less strict on stringers)
    t = 0.8
    tau_crit = K_s * E * (t/b)**2
    tau_int = V_int * Q_mm3 / (I_xx_mm4*1e-12)
    print("tau int: ", tau_int)
    #tau = VQ/It
    return tau_crit * 1.5

print("Q:", Q_NA(1000, 0, [])*1e-9)


#eval_bending_stress(M(1),I_xx(1, 0, []))
#eval_shear_buckling()



# bending stress
# shear buckling
#


