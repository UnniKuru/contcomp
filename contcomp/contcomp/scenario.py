

class Scenario():
	def __init__(self, model: Model, control_alg:Algorithm, timescale=None):
		self.model = model
		self.control_alg = control_alg
		if timescale is None:
			self.timescale = estimate_timescale(Model)
		else:
			self.timescale = timescale

	def calculate_output(self):
		pass

	
