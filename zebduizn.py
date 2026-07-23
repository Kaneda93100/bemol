import bemol as bem
import numpy as np
import pandas as pd
import regex as re



rotor_mex = bem.rotor.Rotor("/home/arthur/Documents/GitHub/bemol/bemol/rotors/mexico")

x = 0

R = rotor_mex.sections[-1].radius

normalized_rad = []

for i in range(len(rotor_mex.sections)) : 
    normalized_rad.append((rotor_mex.sections[i].radius/R))
print(normalized_rad)

with open('mexico.csv', 'r') as f :
    lines = f.readlines()

for i, line in enumerate(lines) :
    line = re.sub(r'\s+', ',', line)
    lines[i] = line + '\n'

with open('mexico.csv', 'w') as f :
    f.writelines(lines)

df = pd.read_csv('mexico.csv', sep = ',')

R = 2.25
print(list((df['POS_[m]'].values/R)))

"""
blade_dat = pd.read_csv('bemol/rotors/mexico/blade.dat', sep = '\s+')

df['POS_[m]'] = blade_dat['radius']
df['CHORD_[m]'] = blade_dat['chord']
df['TWIST_[deg]'] = blade_dat['twist']

df = df.drop(columns =['Unnamed: 8'])
df = df.drop(index = [34, 35])

df.to_csv('mexico.csv', index = False)

"""

"""
with open('mexico.csv', 'r') as f :
    lines = f.readlines()

for i, line in enumerate(lines) :
    line = re.sub(r'\s+', ',', line)
    lines[i] = line + '\n'

with open('mexico.csv', 'w') as f :
    f.writelines(lines)
"""

x = 0
    