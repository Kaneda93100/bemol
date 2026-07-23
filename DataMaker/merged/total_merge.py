import pandas as pd
import pathlib as p

path_new_forces = p.Path('DataMaker/merged/forces_new.csv')
path_new_speeds = p.Path('DataMaker/merged/vitesses_new.csv')

path_old_forces = p.Path('/home/arthur/Documents/GitHub/BEM_2_Vortex-/data/100/raw/fichier_forces.csv')
path_old_speeds = p.Path('/home/arthur/Documents/GitHub/BEM_2_Vortex-/data/100/raw/fichier_vitesses.csv')


df_f = pd.read_csv(path_new_forces)
df_v = pd.read_csv(path_new_speeds)

df_f_old = pd.read_csv(path_old_forces)
df_v_old = pd.read_csv(path_old_speeds)

total_v = pd.concat([df_v, df_v_old])
total_v.to_csv("/home/arthur/Documents/GitHub/BEM_2_Vortex-/full_data200.csv")

x = 0

