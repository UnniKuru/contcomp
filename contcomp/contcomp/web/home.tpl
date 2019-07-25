<!DOCTYPE html>
	<html>
		<head>
			<title> Controls Simulation </title>
			<script src="https://code.jquery.com/jquery-1.10.2.js"></script>
			<script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
		</head>

		<body>
			<div id = "header"> 
				<h1> Controls Simulation </h1>
			</div>

			<div id = "model">
				<h3> Model: First-Order </h3>
				<form METHOD="POST" id = "model_params">
					<table style="width:50%">
						<tr>
							<th align="center"> Kp </th>
							<th align="center"> TauP </th>
						</tr>
						<tr>
							<td align="center"> <INPUT TYPE="number" name="kp" id="kp" SIZE="25" value=5> </td>
							<td align="center"> <INPUT TYPE="number" name="tp" id="tp" SIZE="25" value=3> </td>
						</tr>
					</table>
				</form>
			</div>

			<div id = "algorithm">
				<h3> Algorithm: PID With Bounds </h3>
				<form METHOD="POST" id = "algorithm_params">
					<table style="width:50%">
						<tr>
							<th align="center"> Kc </th>
							<th align="center"> TauI </th>
							<th align="center"> TauD </th>
						</tr>
						<tr> 
							<td align="center"> <INPUT TYPE="number" name="kc" id="kc" SIZE="25" value=0.4> </td>
							<td align="center"> <INPUT TYPE="number" name="ti" id="ti" SIZE="25" value=1.5> </td>
							<td align="center"> <INPUT TYPE="number" name="td" id="td" SIZE="25" value=0> </td>
						</tr>
					</table>
				</form>
			</div>
			<div id = "submit_button">
				<button id="submit">Submit Parameters</button>
			</div>
			<div id = "charts">
				<canvas id="pid_no_windup_chart"></canvas>
			</div>

		</body>
		<script type="text/javascript">
			document.getElementById("submit").addEventListener('click', sendPOST);
			function sendPOST(){
				var params = $('form').serializeArray();
				fetch('../api/POST', {
					method: 'POST',
					body:JSON.stringify(params)
				}).then((res) => res.json())
				.then((data) => genChart(data))
				.catch((err)=>console.log(err)); 

			function genChart(data){

				var xy = [];
				for (var i=0; i < data.t.length; i++){
					var new_el = {x: data.t[i],y: data.PV[i]}
					xy.push(new_el)
				}
				var ctx = document.getElementById('pid_no_windup_chart').getContext('2d');
				var scatterChart = new Chart(ctx, {
				    type: 'scatter',
				    data: {
				        datasets: [{
				            label: 'Scatter Dataset',
				            data: xy
				        }]
				    },
				    options: {
				        scales: {
				            xAxes: [{
				                type: 'linear',
				                position: 'bottom'
				            }]
				        }
				    }
				});
			}
				
			};
		</script>
	</html>

