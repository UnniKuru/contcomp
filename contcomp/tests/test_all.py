# Sample Test passing with nose and pytest
import unittest
import sys
sys.path.append('../')
from contcomp.simulation import First_Order, Model,Simulation,PID_No_Windup

Kp = 2
tP = 3
y0 = 3
U = 2
t = 3
y = 2
Kc = 3
tI = 4
tD = 2
time_scale = 10
fO = First_Order(Kp,tP,y0=y0)
model = Model(fO)
algorithm = PID_No_Windup(Kc,tI,tD)
sim = Simulation(model,algorithm,time_scale)
sim.initialize()

class TestModels(unittest.TestCase):	

	def test_first_order(self):
		params = model.gen_params(U)
		dydt = fO.run(y,t,params)
		self.assertEqual(dydt,(-2/3 + 2*2/3))

	def test_model(self):
		params = model.gen_params(U)
		self.assertTrue(params==(2,2,3))

	def test_pid_no_windup(self):
		#testing step 0 
		sim.e[0] = 1
		self.assertTrue(algorithm.update_output(0,sim) == 3)

		#testing step 1
		sim.e[1] = 1
		sim.PV[1] = 0.01
		dt = sim.delta_t
		dpv = sim.PV[1]/ dt
		ie = sim.e[1]*dt
		self.assertTrue(algorithm.update_output(1,sim) == (3 + 0.75*ie-6*dpv))

		#testing lower bound
		sim.PV[1] = 10
		self.assertTrue(algorithm.update_output(1,sim) == 0)

		#testing upper bound
		sim.PV[1] = -10
		self.assertTrue(algorithm.update_output(1,sim) == 10)
		
if __name__ == '__main__':
	unittest.main()