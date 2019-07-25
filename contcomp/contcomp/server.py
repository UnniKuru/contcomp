from bottle import route, run, template, debug, request,TEMPLATE_PATH
from simulation import First_Order, Model,Simulation,PID_No_Windup
import json



TEMPLATE_PATH.insert(0,'C:\\Users\\unni.kurumbail\\Documents\\Personal\\coding\\controls_analysis\\contcomp\\contcomp\\web')


@route('/home')
def index():
	output = template('home.tpl')
	return output

@route('/testPOST',method='POST')
def testPOST():
	postdata = request.body.read()
	print(postdata)
	return {'item1':'testitem1field'}

@route('/api/POST',method='POST')
def handle_post():
	postdata=request.body.read()
	user_params = json.loads(postdata)
	return run_simulation(user_params)
def run_simulation(user_params):
	Kc = float([i['value'] for i in user_params if i['name'] == 'kc'][0])
	tI = float([i['value'] for i in user_params if i['name'] == 'ti'][0])
	tD = float([i['value'] for i in user_params if i['name'] == 'td'][0])
	Kp = float([i['value'] for i in user_params if i['name'] == 'kp'][0])
	tP = float([i['value'] for i in user_params if i['name'] == 'tp'][0])
	fO = First_Order(Kp,tP)
	model = Model(fO)
	algorithm = PID_No_Windup(Kc,tI,tD)
	sim = Simulation(model,algorithm,const_sp=30)
	sim.initialize()
	t,PV,U,SP,e,P,I,D = sim.simulate()
	return {'t':t.tolist(),'PV':PV.tolist(),'U':U.tolist(),'SP':SP.tolist(),'e':e.tolist(),'P':P.tolist(),'I':I.tolist(),'D':D.tolist()}

run(reloader=True)