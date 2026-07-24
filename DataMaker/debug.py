import src.SimEnv as sv 
import bemol as bem
import matplotlib.pyplot as plt
from scipy.stats.qmc import LatinHypercube as lhc
import pathlib as p
import pandas as pd
import numpy as np

sampler = lhc(2, strength = 1, seed = 42)
samples = sampler.random(n = 100)

tsrs = samples[0:5,0]*8 + 4
yaws = samples[0:5,1]*60 - 30

corrections = [
    bem.secondary.hubTipLoss.Prandtl,
    bem.secondary.skewAngle.Burton,
    bem.secondary.turbulentWakeState.Buhl,
    bem.secondary.yawModel.IFPEN
]

sim_test = sv.SimEnv(omega = 44.5163679, U = 12.520228472, yaw = 15, skew = 15)

#path_forces = p.Path("/home/arthur/Documents/GitHub/BEM_2_Vortex-/data/100/raw/fichier_forces.csv")
#path_20mai = p.Path('bem_data.csv')
#df_20mai = pd.read_csv(path_20mai)

seq  = sim_test.data_maker(yaws, tsrs, 10, export = False)
#para = sim_test.para_data_maker(yaws, tsrs, 72, export = False)

x = 0