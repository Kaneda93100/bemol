import sys
import os

import bemol as bem
import numpy as np
import pandas as pd
import pathlib as p
import matplotlib.pyplot as plt


## Définir des variables par défaut pour plus de lisibilité
rho = 1.191
rotor_dir_vortex = '/home/arthur/Documents/GitHub/bemol/bemol/rotors/mexico_vortex'
rotor_vortex = bem.rotor(rotor_dir_vortex)
corrections = [
    bem.secondary.HubTipLoss.Prandtl,
    bem.secondary.SkewAngle.Burton,
    bem.secondary.TurbulentWakeState.Buhl,
    bem.secondary.YawModel.IFPEN
]
solver_yawOn = bem.ning.NingUncoupled(rotor_vortex, rho, corrections)


class SimEnv :

    ## Paramètres mécaniques et relatif à la géométrie
    precone : float
    tilt : float
    rotor_path : str
    rotor : bem.rotor
    omega : float

    ## Paramètres métérologiques (pour l'instant un seul, mais à enrichir)
    U : float
    rho : float
    yaw : float
    skew : float

    ## Paramètres de simulations
    Nbr_rev : float
    tsr : float
    tStep : float

    ## Solveur BEM (seul NingUncoupled est supporté pour l'instant)
    solver : bem.ning.NingUncoupled
    corrections : list
    

    def __init__(self, 
                 omega, U, yaw, skew,tsr, corrections:list,
                 rotor_dir:str = rotor_dir_vortex,
                 rho = 1.191, Nbr_rev = 1.0, tStep = 0,precone = 0, tilt = 0,
                 ) :
        
        ## Charger les paramètres mécaniques
        self.precone = precone
        self.tilt = tilt
        self.rotor = bem.rotor.Rotor(rotor_dir)
        self.rotor_dir = rotor_dir
        self.omega = omega

        ## Charger les paramètres métérologiques
        self.U       = U
        self.rho     = rho
        self.yaw     = yaw
        self.skew    = skew

        ## Charger les paramètres de simulations
        self.Nbr_rev = Nbr_rev
        self.tsr     = tsr
        self.tStep   = tStep

        ## Charger le solver
        self.corrections = corrections
        self.solver = bem.ning.NingUncoupled(self.rotor, self.rho, corrections)

    def print(self):

        print("#"*20)
        print("\t"*3+"Affichage des paramètres de la simulation"+"\t"*3)
        print("#"*20)

        print("\n\n")

        print("#"*20)
        print('------- Paramètres mécaniques/géométriques -------\n')
        print(f"----> Precone : {self.precone}\n")
        print(f"----> Tilt : {self.tilt}\n")
        print(f"----> Vitesse de rotation (omega) : {self.omega}\n")
        print(f"----> Rotor (chemin) : {self.rotor_dir}\n")
        print("#"*20)

        print("#"*20)
        print('------- Paramètres métérologiques -------\n')
        print(f"----> Vitesse du vent (U) : {self.U}\n")
        print(f"----> densité de l'air : {self.rho}\n")
        print(f"----> yaw : {self.yaw}\n")
        print(f"----> skew : {self.skew}\n")
        print("#"*20)

        print("#"*20)
        print('------- Paramètres de simulation -------\n')    
        print(f"----> Nombre de révolution : {self.nbr_rev}\n")
        print(f"----> Tsr : {self.tsr}\n")
        print(f"----> tStep : {self.tStep}")
        print("#"*20)        

        print("#"*20)
        print('------- Paramètres du solver -------\n')
        print(f"----> Géométrie utilisé : {self.rotor_dir}\n")
        print(f"----> Corrections : {self.corrections}") 
        print("#"*20)

        return                                                       
    
    def data_maker(self, yaws:list, tsrs:list, nbr_az, export = True) :
        az = np.linspace(0,360, nbr_az, endpoint = False)
        rad_azs = np.radians(az)
        
        attr = ['r', 'theta', 'yaw', 'V_eff', 'alpha', 'Fn', 'Ft']
        data_list = []

        for yaw in yaws :
            for i, az in enumerate(rad_azs) :
                for j in range(len(self.rotor.sections)) :
                    
                    ## Calculer les efforts normaux et les inductions
                    velocities = bem.tools.calculateVelocity(wind = self.U, omega = self.omega, rad = self.rotor.sections[j].radius, azi = rad_azs[i],
                                                    yaw = yaw, tilt = self.tilt,
                                                    precone = self.precone)                
                    fn,ft,ai,at = self.solver.solve(self.rotor.sections[j], az[i], pitch = self.rotor.pitch,
                                                velocity = velocities, angles = [yaw, self.tilt])

            angle = self.rotor.sections[j].twist + self.pitch
            _, aoa = compute_inflow_aoa(self.solver, velocities[0], velocities[1], angle)
            V_eff = np.sqrt((self.U*(1-ai))**2 + (self.omega*self.rotor.sections[j].radius*(1+at))**2)                             

            data_list.append({
                    'yaw': yaw,
                    'r': self.rotor.sections[j].radius,
                    'theta': np.degrees(az[i]).round(1),  
                    'Fn': fn,
                    'Ft': ft,                    
                    'V_eff': V_eff,
                    'Alpha_deg': np.degrees(aoa)
                    })
        df = pd.DataFrame(data_list)

        ## Exporter les données calculées dans le dossier Data/
        if export == True :
            path_data = p.Path(os.path.join(os.path.direname(__file__), 'Data')).mkdir(exist_ok = True)
            df.to_csv(path_data/'bem_data.csv', index = False, sep = ',', quotechar = True)
            print(f"Données calculées pour yaws == [{yaws}] et tsrs == [{tsrs}].\nEnregistrées à l'adresse {path_data}")

        return df

def easy_plot(df, attr_x:str, attr_y:str, indexs:list = [4, 17, 30], savefig = False) :
    print(f"Affichage de {attr_y} en fonction de {attr_x}\n")

    if attr_y not in ['Fn', 'Ft', 'V_eff', 'Alpha_deg'] :
        raise ValueError(f"L'attribut {attr_y} n'est pas supporté pour l'affichage en ordonnée. Choisissez un dans ['Fn', 'Ft', 'V_eff', 'Alpha_deg'].")

    fig_dir = p.Path(p.Path(os.path.join(os.path.direname(__file__), 'figs')).mkdir(exist_ok = True))

    if attr_x == 'r' :
        """
        Dans ce cas, la liste indexs contient les indices des azimuts d'intérêts.
        Plot la distribution de la variable attr_y sur la pale. 
        """

        x = df[attr_x].to_numpy()
        fig = plt.figure(figsize = (15,12))
        
        for i in range(indexs) :
            plt.subplot(len(indexs), 1, i)

            y = df[attr_y][i*x.shape[0]:(i+1*x.shape[0])]
            plt.plot(x, y)
            plt.xlabel(attr_x)
            plt.ylabel(attr_y)
            plt.title(f"Azimut : {indexs}°")
            plt.grid()
    
    elif attr_x == 'theta' :
        """
        Dans ce cas, la liste indexs contient l'indice des rayons d'intérêts. 
        Plot la varibale attr_y en fonction des azimuts (sur [0,360]).
        """
        
        x = df[attr_x].to_numpy()
        nbr_az = x.shape[0]
        fig = plt.figure(figsize = (15,12))

        for i in range(indexs) :
            plt.subplot(len(indexs),1, i)

            ## Récupérer les données au bon endroit dans le DataFrame
            y = np.zeros((nbr_az))
            for j in range(nbr_az) : 
                y[j] = df.to_numpy()[indexs[i] + nbr_az*j]

            plt.plot(x,y)
            plt.xlabel(attr_x)
            plt.ylabel(attr_y)
            plt.title(f"Section de pale : {df['r'].to_numpy()[indexs[i]]} (d'indice {indexs[i]})")
            plt.grid()
    else : 
        raise ValueError(f"L'attribut {attr_x} n'est par supporté. Essayer avec un des attributs de ['r', 'theta'].")    

    if savefig == True : 
        fig_name = attr_x +'_'+attr_y
        for i in range(len(indexs)) : 
            fig_name += ('_'+str(indexs[i])+'_')
            fig.savefif(fig_dir/fig_name)

    return fig
    


def compute_inflow_aoa(solver, Ux, Uy, angle):
        uxRelative = Ux * (1.0 - solver._axial_induction)
        uthetaRelative = Uy * (1.0 + solver._tangential_induction)
        inflowAngle = np.arctan2(uxRelative, uthetaRelative)

        attackAngle = inflowAngle - angle

        return inflowAngle, attackAngle


## Implémenter divers tests unitaires pour détecter des incohérences dans les données