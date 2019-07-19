import unittest
import sys
sys.path.append('../')
from contcomp.simulation import First_Order, Model,Simulation,PID_No_Windup
import matplotlib.pyplot as plt

Kp = 5
tP = 3
Kc = 2 / Kp 
tI = tP / 2
tD = 0
time_scale = 10

fO = First_Order(Kp,tP)
model = Model(fO)
algorithm = PID_No_Windup(Kc,tI,tD,upper_bound=20)
sim = Simulation(model,algorithm,time_scale,const_sp=30)
sim.initialize()
t,PV,U,SP,e,P,I,D = sim.simulate()
plt.plot(t,PV,label='PV')
plt.plot(t,e,label='e')
plt.plot(t,U,label='U')
plt.plot(t,P,label='P')
plt.plot(t,I,label='I')
plt.plot(t,D,label='D')
plt.legend()
plt.show()