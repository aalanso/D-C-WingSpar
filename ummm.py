bolt_tau_max = 311e6

# variables: 3 spacings, reinf 1 length,
# other than that default config from manual

# z in cm, reinf_lengths in cm as well
def I_xx(z, n_reinf, reinf_lengths):
    I_res = 0

    I_web = 0.8*(75**3)/12
    I_stringer_vertical = 4 * ( (0.8*(20**3)/12 + 0.8*20*(65**2)) )
    I_stringer_h = ((19.2) * (0.8 ** 3) / 12 + (19.2) * (0.8) * ((75 - 0.4) ** 2)) * 4
    I_flanges = 2*(40.8*(0.8**3)/12 + 40.8*0.8*(75.4)**2)

    # print(I_web)
    # print(I_stringer_vertical)
    # print(I_stringer_h)
    # print(I_flanges)

    I_res = I_web + I_stringer_h + I_stringer_vertical + I_flanges

    for i in range(0, n_reinf):
        if z < reinf_lengths[i]:
            I_res += ( (19.2)*(0.8**3)/12 + (19.2)*(0.8) * ((75-0.4-0.8*(i+1))**2)) *4

    return I_res # mm4

#print(I_xx(1000, 0, []))


#def eval_setup(spacing_1, spacing_2, spacing_3, reinf_1_len):

# bending stress
# shear buckling
#


