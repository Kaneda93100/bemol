import src.SimEnv as sv 
import bemol as bem

tsr = 8
omega = 44.5163679 
yaw = 15



sim_test = sv.SimEnv(omega = omega, U = 12.520228472, yaw = 15, skew = 15)

sim_test.print()