import src.SimEnv as sv 
import bemol as bem
import matplotlib.pyplot as plt
corrections = [
    bem.secondary.hubTipLoss.Prandtl,
    bem.secondary.skewAngle.Burton,
    bem.secondary.turbulentWakeState.Buhl,
    bem.secondary.yawModel.IFPEN
]

sim_test = sv.SimEnv(omega = 44.5163679, U = 12.520228472, yaw = 15, skew = 15)

sim_test.print()

yaws = [-15., -10, -5., 0., 5., 10., 15., 20., 25., 30.]
tsrs = [8]

df_se = sim_test.data_maker(yaws, tsrs, 36, export = False)
fig = sv.easy_plot(df_se, 'theta', 'Fn')

plt.show()

x = 0