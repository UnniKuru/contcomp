import numpy as np 
from scipy.integrate import odeint

def first_order(kp,tp,u,timescale=2*tp,num_pts=100):
	'''kp: float, process gain
	   tp: float, process time constant
	   u: function of time, input function (ex. step function, constant, etc.)
	   timescale: float, the timescale to evaluate over'''
	def model(y,t):
		dydt = (kp*u(t)-y)/tp
		return dydt

	y0 = 0 #deviation variable
	t = np.linspace(0,timescale,num_pts)
	return odeint(model,y0,t)

	#TODO: error handling on the integrator
