#This code draws heavily from: https://apmonitor.com/pdc/index.php/Main/ProportionalIntegralDerivative
import numpy as np
from scipy.integrate import odeint
def constant(i,const=10):
	return const

class Simulation():
	def __init__(self,model,algorithm,time_scale,num_pts=100,setpoint=constant,const_sp=10):
		self.model = model
		self.algorithm = algorithm
		self.setpoint = setpoint
		self.time_scale = time_scale
		self.num_pts = num_pts
		self.const_sp = const_sp

	def initialize(self):
		self.model.initialize(self.num_pts)
		self.algorithm.initialize(self.num_pts)
		self.t_vals = np.linspace(0,self.time_scale,self.num_pts)
		self.delta_t = self.t_vals[1]-self.t_vals[0]
		self.PV = np.zeros(self.num_pts+1)
		self.U = np.zeros(self.num_pts)
		self.SP = np.zeros(self.num_pts)
		self.e = np.zeros(self.num_pts)

	def sim_step(self,i):
		self.SP[i] = self.setpoint(i,const=self.const_sp)
		self.e[i] = self.SP[i]-self.PV[i]
		self.U[i] = self.algorithm.update_output(i,self)
		args=self.model.gen_params(self.U[i])
		self.PV[i+1] = odeint(self.model.process.run,self.PV[i],[0,self.delta_t],args=(args,))[-1]

	def simulate(self):

		self.PV[0] = self.model.y0
		for i in range(self.num_pts):
			self.sim_step(i)
			print("Step: {} SP: {} PV: {}".format(i,self.SP[i],self.PV[i]))
		return (self.t_vals,self.PV[:-1],self.U,self.SP,self.e) + self.algorithm.gen_returns()


class Model():
	def __init__(self,process):
		'''process: a function of t that also takes in optional params (a tuple)
		   params: a tuple'''
		self.process = process
		self.y0 = process.y0
	def gen_params(self,controller_output):
		return (controller_output,) + self.process.ret_params()
	def initialize(self,num_steps):
		pass 

class First_Order():
	def __init__(self,Kp,tP,y0=0):
		self.Kp = Kp
		self.tP = tP
		self.y0 = y0

	@staticmethod
	def run(y,t,params):
		u = params[0]
		Kp = params[1]
		tP = params[2]
		return -y/tP + u*(Kp/tP) #dydt

	def ret_params(self):
		return (self.Kp,self.tP)

	def initialize(self,num_steps):
		pass



class PID_No_Windup():
	def __init__(self,kc,ti,td,upper_bound=10,lower_bound=0):
		self.Kc = kc
		self.tI = ti
		self.tD = td
		self.ubound = upper_bound
		self.lbound = lower_bound

	def initialize(self,num_pts):
		self.ie = np.zeros(num_pts+1)
		self.dpv = np.zeros(num_pts+1)
		self.P = np.zeros(num_pts)
		self.I = np.zeros(num_pts)
		self.D = np.zeros(num_pts)

	def update_output(self,i,simulation):
		if i >= 1:  # calculate starting on second cycle
			self.dpv[i] = (simulation.PV[i]-simulation.PV[i-1])/simulation.delta_t
			self.ie[i] = self.ie[i-1] + simulation.e[i] * simulation.delta_t
		self.P[i] = self.Kc * simulation.e[i]
		self.I[i] = self.Kc/self.tI * self.ie[i]
		self.D[i] = - self.Kc * self.tD * self.dpv[i]
		U = simulation.U[0] + self.P[i] + self.I[i] + self.D[i]
		if U > self.ubound:
			if i > 0:
				self.ie[i] -= simulation.e[i] * simulation.delta_t
			return self.ubound
		elif U < self.lbound:
			if i > 0:
				self.ie[i] -= simulation.e[i] * simulation.delta_t
			return self.lbound
		else:
			return U

	def gen_returns(self):
		return (self.P,self.I,self.D)

		






			

			
		