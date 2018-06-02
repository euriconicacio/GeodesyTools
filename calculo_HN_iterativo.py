# UFPR - PPGCG - LARAS 
# 08/04/2018
# Script to compute normal heights by iterative method using orthometric
# heights and terrestrial gravity observations 

import numpy as np

# Input file full path - CHANGE!
inp = input("Insert the input file full path: ")
#inp = "/home/usuario/modelo_input.dat"

# Read data file
data = np.loadtxt(inp)

# GRS80 parameters - Hofmann-Wellenhof e Moritz (2005)
a = 6378137 # semimajor axis of the ellipsoid (m)
b = 6356752.3141 # semiminor axis of the ellipsoid (m)
f = 0.00335281068118 # flattening
nge = 9.7803267715 # normal gravity on the equator (m/s2)
ngp = 9.8321863685 # normal gravity on the pole (m/s2)
m = 0.00344978600308 # m = w^2*a^2 * (b/GM)

# Number rows (n) of the data matrix
n = data.shape[0]

# Loop to compute normal heights (iterative method)
# Initialize zeros matrix --> will be used to store the iterations number
countm = np.zeros((n,1))
ng0 = np.zeros((n,1))
HNor = np.zeros((n,1))
C = np.zeros((n,1))

for i in range(n):
    # Normal gravity on the ellipsoid (Somigliana formula)
    ng0[i][0] = (a * nge * (np.cos(np.deg2rad(data[i][1])))**2 + b * ngp * (np.sin(np.deg2rad(data[i][1])))**2) / (a**2 * (np.cos(np.deg2rad(data[i][1])))**2 + b**2 * (np.sin(np.deg2rad(data[i][1])))**2)**0.5
    # Input initial value for normal height (HN0)
    HN0 = data[i][3]
    dif = 1e+10
    count = 0
    gn=0
    HN=0

    #% simple Bouguer anomaly - calculated once for each point
    deltagB = (data[i][4] + 0.1967*data[i][3]-ng0[i][0]*100000)/100000

    # Iterate while dif is not zero (by point)
    while (abs(dif) > 1e-12):
        # Mean normal gravity compute
        gn = ng0[i][0] * (1 - (HN0/a) * (1 + f + m -(2*f) * (np.sin(np.deg2rad(data[i][1])))**2) + (HN0/a)**2)
        # Normal height compute
        HN = data[i][3]*(1-deltagB/gn)
        # Difference between the previous and the current height
        dif = HN0 - HN
        HN0 = HN
        # count the number of iterations by point
        count = count + 1
    HNor[i][0] = HN
    C[i][0]=HN*gn*0.1

data_H = np.append(data, HNor, axis=1)
data_H = np.append(data_H, C, axis=1)

# Output file full path - CHANGE!
out = input("Insert the output file full path: ")
#out = "/home/usuario/modelo_output2.dat"

np.savetxt(out, data_H, fmt='%d %.10f %.10f %.10f %.10f %.10f %.10f')

print("DONE! Matrix saved to ", out)