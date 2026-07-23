import multiprocessing as mp
import numpy as np
from time import perf_counter
print(mp.cpu_count())

def f(x):
  x = np.radians(x) 
  return x**2

with mp.Pool(processes=mp.cpu_count()) as pool:
  for i in pool.imap(f, range(10)):
    print(i)

import DataMaker.src.SimEnv as sv
from scipy.stats.qmc import LatinHypercube as lhc

sampler = lhc(2, strength = 1, seed = 42)
samples = sampler.random(n = 100)

samples[:,0] = samples[:,0]*8+4
samples[:,1] = samples[:,1]*60-30

sim_test = sv.SimEnv(omega = 44.5163679, U = 12.520228472, yaw = 15, skew = 15)

sim_test.print()

start_para = perf_counter()
df1 = sim_test.para_data_maker(list(samples[:,1]), list(samples[:,0]), 72, export = False)
stop_para = perf_counter()

start_seq = perf_counter()
df2 = sim_test.data_maker(list(samples[:,1]), list(samples[:,0]), 72, export = False)
stop_seq = perf_counter()

print(f"Para_perf : {stop_para-start_para : .3f}\n\nSeq_perf : {stop_seq-start_seq : .3f}")
x = 0